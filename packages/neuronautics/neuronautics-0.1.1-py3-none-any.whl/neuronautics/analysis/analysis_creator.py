from jinja2 import Template, Environment, FileSystemLoader
import yaml

from neuronautics.utils.helpers import file_path, load_yaml
from neuronautics.analysis.loader import Loader


# pyqt
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class AnalysisCreatorUi(QtWidgets.QDialog):
    def __init__(self):
        super(AnalysisCreatorUi, self).__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        uic.loadUi('ui/analysis-creation.ui', self)

        self.show()

    def create_analysis(self):
        name = self.analysisName.text()
        type = self.analysisType.currentText()

        path = AnalysisCreator.create(name, type)

        self.done(1)
        from neuronautics.utils.helpers import open_external_editor
        open_external_editor(path)


class AnalysisCreator:

    @classmethod
    def create(cls, name, type):
        # Create a Jinja environment with the specified template directory
        env = Environment(loader=FileSystemLoader('resources/templates'))

        # Load the template from the environment
        jinja_template = dict(
            graph='graph-analysis.jinja',
            bar='bar-analysis.jinja',
            line='line-analysis.jinja',
            image='image-analysis.jinja'
        ).get(type, 'base-analysis.jinja')
        template = env.get_template(jinja_template)

        # Sample values
        name_split = name.lower().split()
        filename = '_'.join(name_split)
        class_name = ''.join([n.capitalize() for n in name_split])

        # Render the template with the provided values
        filled_template = template.render(
            class_name=class_name,
            title=name
        )

        # Write the filled template to a .py file
        module = ['analysis', 'custom', 'scripts', type, filename]
        relative_path = '/'.join(module)+'.py'
        path = file_path(relative_path)
        with open(path, 'w') as file:
            file.write(filled_template)

        cls.save(name, relative_path, filename, class_name)

        print(f"Python script '{filename}' generated successfully.")
        return path

    @classmethod
    def save(cls, name, path, module, class_name):
        config = {
            'name': name,
            'module': module,
            'path': path,
            'class': class_name
        }
        print(config)
        Loader.save(config)
