import importlib
import importlib.util
import yaml
from pathlib import Path
from neuronautics.utils.helpers import file_path, load_yaml, app_path
from neuronautics.utils.singleton import Singleton


BASE_ANALYTICS = 'resources/analysis-base.yml'
EXTRA_ANALYTICS = file_path('analytics/extra.yml')


class Loader(metaclass=Singleton):
    def __init__(self):
        self.analysis_handle = None
        self.analysis_config = None

    def load(self):
        base = load_yaml(BASE_ANALYTICS, list())
        analysis = load_yaml(EXTRA_ANALYTICS, list())
        for b in base:
            if not any([b.get('name') == an.get('name') for an in analysis]):
                analysis.append(b)
        analysis = sorted(analysis, key=lambda an: an.get('name'))

        self.analysis_handle = {name: handle for name, handle in [Loader._instance_analysis(an) for an in analysis]}
        self.analysis_config = {config.get('name'): config for config in analysis}

    def get_analysis_path(self, name):
        path = self.analysis_config[name].get('path')
        if path:
            return file_path(path)
        return None

    @classmethod
    def _instance_analysis(cls, analysis):
        try:
            module = cls._get_module(analysis.get('module'), analysis.get('path'))
            dynamic_class = getattr(module, analysis.get('class'))()
            return analysis.get('name'), dynamic_class
        except Exception as e:
            raise e

    @classmethod
    def check_module(cls, analysis):
        try:
            name, instance = cls._instance_analysis(analysis)
            params_def = instance.get_input_params()
            params = {param['name']: param['default'] for param in params_def}
            instance.run(None, **params)
        except:
            return False
        return True

    def get_types(self):
        return {name: handle.type() for name, handle in self.analysis_handle.items()}

    @staticmethod
    def load_and_execute_class(module_name, class_name):
        try:
            module = Loader._get_module(module_name)
            dynamic_class = getattr(module, class_name)
            instance = dynamic_class()

            input_params_result = instance.get_input_params()
            execute_result = instance.execute()

            return input_params_result, execute_result
        except Exception as e:
            return f"Error: {e}", ""

    @staticmethod
    def _get_module(module_name, path=None):
        try:
            module = importlib.import_module(module_name)
        except:
            spec = importlib.util.spec_from_file_location(module_name, file_path(path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return module

    @classmethod
    def save(cls, config):
        cls.delete(config['name'])
        analysis = load_yaml(EXTRA_ANALYTICS, list())
        if Loader.check_module(config):
            analysis.append(config)
            cls._dump(analysis)

    @classmethod
    def delete(cls, name):
        analysis = load_yaml(EXTRA_ANALYTICS, list())
        analysis = [an for an in analysis if an.get('name').upper() != name.upper()]
        cls._dump(analysis)

    @classmethod
    def _dump(cls, analysis):
        with open(EXTRA_ANALYTICS, 'w') as stream:
            yaml.dump(analysis, stream)

