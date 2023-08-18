from jinja2 import Template

from ..utils.helpers import file_path
from ..analysis.loader import Loader
from ..recordings.config import (UI_ANALYSIS_CREATION, JINJA_BASE_ANALYSIS, JINJA_GRAPH_ANALYSIS, JINJA_BAR_ANALYSIS,
                                 JINJA_IMAGE_ANALYSIS, JINJA_LINE_ANALYSIS)


# pyqt
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt


class AnalysisCreatorUi(QtWidgets.QDialog):
    def __init__(self):
        super(AnalysisCreatorUi, self).__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        uic.loadUi(UI_ANALYSIS_CREATION, self)

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


        # Load the template from the environment
        jinja_template = dict(
            graph=JINJA_GRAPH_ANALYSIS,
            bar=JINJA_BAR_ANALYSIS,
            line=JINJA_LINE_ANALYSIS,
            image=JINJA_IMAGE_ANALYSIS
        ).get(type, JINJA_BASE_ANALYSIS)

        with open(jinja_template) as file_:
            template = Template(file_.read())
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
