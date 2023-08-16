# ----------------------------------------------------------------------------------------------------------------------
#  Copyright (c) 2023. Antonio Bulgheroni.
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to the following conditions:
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
#  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------------------------------------------------------
import yaml
from pathlib import Path

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWizard, QWizardPage

from expwizard.constants import WizardPage
from expwizard.wizard_new_experiment_page_ui import Ui_NewExperimentPage

unit_configuration_file = Path(__file__).parent / Path('conf') / Path('unit_list.yaml')


class NewExperimentPage(QWizardPage, Ui_NewExperimentPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self._unit_lut = dict()
        self.prepare_unit_combobox()
        self.parent = parent
        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))

        self.registerField('project_name*', self.project_name)
        self.registerField('project_responsible*', self.project_responsible)
        self.registerField('unit', self.unit_combobox, 'currentText', self.unit_combobox.currentIndexChanged)

        self.registerField('description', self.sample_description, 'plainText', self.sample_description.textChanged)
        self.registerField('number_of_samples', self.number_of_samples)
        self.registerField('microscope', self.microscope_combobox, 'currentText',
                           self.microscope_combobox.currentIndexChanged)
        self.registerField('operator', self.microscope_operator)

    def nextId(self) -> int:
        return WizardPage.PageCommitNewExperiment

    def prepare_unit_combobox(self):
        with open(unit_configuration_file, 'rt', encoding='utf-8') as file:
            yaml_dict = yaml.safe_load(file)

        self.unit_combobox.clear()
        self.unit_combobox.addItems([key for key in yaml_dict.keys()])
        for key in yaml_dict:
            long_name = yaml_dict[key].get('Long name', 'N/A')
            head = yaml_dict[key].get('Head', None)
            if head:
                long_name += f' ({head})'
            self._unit_lut[key] = long_name
        self.change_unit_name()

    def change_unit_name(self):
        long_name = self._unit_lut.get(self.unit_combobox.currentText(), 'N/A')
        self.unit_name.setText(long_name)
