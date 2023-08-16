# -*- coding: utf-8 -*-
"""
Review configuration page.

This wizard page allows the user to see the current configuration as retrieved from the QSetting object. The user can
change any value and try the connection by pressing the corresponding button. If the user does not test the
connection, this will be anyhow tested when pressing next.
"""
# ----------------------------------------------------------------------------------------------------------------------
#  Copyright (c) 2022-2023. Antonio Bulgheroni.
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
import datetime
from pathlib import Path

import elog
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QCheckBox,
    QDoubleSpinBox,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QProgressDialog,
    QSpinBox,
    QWizard,
    QWizardPage,
)

from autologbook.autotools import encrypt_pass
from autologbook.elog_interface import AnalysisLogbook, ELOGConnectionParameters, elog_handle_factory
from expwizard.constants import WizardPage, default_settings
from expwizard.wizard_review_configuration_page_ui import Ui_ReviewConfigurationPage

__author__ = 'Antonio Bulgheroni'
__email__ = 'antonio.bulgheroni@gmail.com'


class ReviewConfigurationPage(QWizardPage, Ui_ReviewConfigurationPage):
    """Subclass of QWizardPage to implement a review configuration page."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.setPixmap(QWizard.LogoPixmap, QPixmap(':/expwizard/ec-logo.jpg'))
        if hasattr(parent, 'settings'):
            self.settings = parent.settings
        else:
            self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'ecjrc', 'experimentwizard')

        elog_handle_factory.set_connection_parameters(ELOGConnectionParameters.from_qsettings(self.settings))

        self.timeout = float(self.settings.value('elog_timeout', 10))
        self.password_needs_update = False
        self.connection_is_ok = False

    def _sleep_inputs(self, sleep: bool = True):

        for widget in [widget for widget in self.findChildren((QLineEdit, QDoubleSpinBox, QSpinBox, QCheckBox))
                       if not widget.objectName().startswith('qt_spinbox')]:
            widget.blockSignals(sleep)

    def initializePage(self) -> None:
        """
        Pre-fill the field values with the ones stored in setting.

        These parameters are stored in the settings instead that on Wizard fields because we want them to be persistent
        between following application executions.
        """
        self.elog_user_field.setText(self.settings.value('elog_user_name', 'log-robot', type=str))
        self.elog_password_field.setText(self.settings.value('elog_password', 'mTZtK2iFHhwqixkhJV0JkplSqMMu9ykWOhcNY'
                                                                              '/1WyL7', type=str))
        self.elog_hostname_field.setText(self.settings.value('elog_hostname', 'https://10.166.16.24', type=str))
        self.elog_port_field.setValue(self.settings.value('elog_port', 8080, type=int))
        self.elog_ssl_check_box.setChecked(self.settings.value('elog_use_ssl', True, type=bool))
        self.elog_timeout_spinbox.setValue(self.settings.value('elog_timeout', 12, type=float))

        self.protocol_list_logbook_field.setText(
            self.settings.value('protocol_list_logbook', 'Microscopy-Protocol', type=str))
        self.network_folder.setText(
            self.settings.value('network_folder', f'R:\\A226\\Results\\{datetime.datetime.now():%Y}', type=str))

        self.quattro_elog_logbook_field.setText(self.settings.value('quattro_logbook', 'Quattro-Analysis', type=str))
        self.quattro_local_path.setText(self.settings.value('quattro_local_folder', 'M:\\', type=str))

        self.versa_elog_logbook_field.setText(self.settings.value('versa_logbook', 'Versa-Analysis', type=str))
        self.versa_local_path.setText(self.settings.value('versa_local_folder', 'M:\\', type=str))

        self.vega_elog_logbook_field.setText(self.settings.value('vega_logbook', 'Vega-Analysis', type=str))
        self.vega_local_path.setText(self.settings.value('vega_local_folder', 'M:\\', type=str))

        self.xl40gb_elog_logbook_field.setText(self.settings.value('xl40gb_logbook', 'XL40-GB-Analysis', type=str))
        self.xl40gb_local_path.setText(self.settings.value('xl40gb_local_folder', 'M:\\', type=str))

        self.xl40cold_elog_logbook_field.setText(self.settings.value(
            'xl40cold_logbook', 'XL40-Cold-Analysis', type=str))
        self.xl40cold_local_path.setText(self.settings.value('xl40cold_local_folder', 'M:\\', type=str))

    def password_changed(self):
        """Slot connected to a change of password."""
        self.password_needs_update = True

    def search_folder(self):
        """Slot connected to the search folder."""
        lut = {
            'network_path_search_button': self.network_folder,
            'quattro_path_search_button': self.quattro_local_path,
            'versa_path_search_button': self.versa_local_path,
            'vega_path_search_button': self.vega_local_path,
            'xl40gb_path_search_button': self.xl40gb_local_path,
            'xl40cold_path_search_button': self.xl40cold_local_path,
        }
        button_name = self.sender().objectName()

        if button_name in lut.keys():
            field = lut[button_name]
            folder = QFileDialog.getExistingDirectory(self, 'Select a folder', str(Path(field.text())))
            if folder:
                field.setText(str(Path(folder)))

    def validatePage(self) -> bool:
        """
        Overload of the validatePage.

        Before validating  the page the settings are updated. If the connection was already tested ok,
        then it returns True, otherwise it returns the outcome of the connection test.

        Returns
        -------
        True if the page is validated.

        """
        self.update_settings()
        if self.connection_is_ok:
            return True
        else:
            return self.test_connection()

    def connection_to_be_retested(self):
        """
        Slot connected to a change in the GUI fields.

        This is to inform that the connection needs to be re-tested.
        """
        self.connection_test_label.setText('Parameters changed. Connection need to be re-tested')
        self.connection_is_ok = False

    def test_connection(self) -> bool:
        """
        Perform a connection test.

        This test will perform three checks for each logbook:
            1. read,
            2. write,
            3. delete

        Returns
        -------
        True if all tests are successful.
        """
        self.update_settings()
        logbook_to_be_tested = [self.protocol_list_logbook_field.text(),
                                self.quattro_elog_logbook_field.text(),
                                self.versa_elog_logbook_field.text(),
                                self.vega_elog_logbook_field.text(),
                                self.xl40gb_elog_logbook_field.text(),
                                self.xl40cold_elog_logbook_field.text()]

        operation_to_be_tested = ['read', 'write', 'delete']

        number_of_test = len(logbook_to_be_tested) * len(operation_to_be_tested)

        progress_dialog = QProgressDialog('Testing connection', 'Abort connection test', 0, number_of_test - 1, self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setWindowTitle('Progress...')

        for logbook in logbook_to_be_tested:
            if progress_dialog.wasCanceled():
                break
            logbook_instance = elog_handle_factory.get_logbook_handle(logbook)
            mid = -1
            if isinstance(logbook_instance, AnalysisLogbook):
                attrib = {
                    'Operator': self.elog_user_field.text(),
                    'Protocol ID': -1,
                    'Project': 'Test project',
                    'Customer': 'Test customer'
                }
            else:
                attrib = dict()

            for operation in operation_to_be_tested:
                progress_dialog.setValue(progress_dialog.value() + 1)
                progress_dialog.setLabelText(f'Checking {operation} operation on {logbook}')
                if progress_dialog.wasCanceled():
                    break
                try:
                    if operation == 'read':
                        logbook_instance.get_last_message_id(timeout=self.timeout)
                    elif operation == 'write':
                        mid = logbook_instance.post('Test message', attributes=attrib, timeout=self.timeout)
                    elif operation == 'delete':
                        logbook_instance.delete(mid)
                except elog.LogbookError:
                    QMessageBox.critical(self, 'Connection test',
                                         f'Test of type \'{operation}\' on logbook {logbook} failed!')
                    progress_dialog.close()
                    self.connection_is_ok = False
                    self.connection_test_label.setText('Connection test failed!')
                    return False

        self.connection_is_ok = True
        self.connection_test_label.setText('Connection test successful!')
        return True

    def nextId(self) -> int:
        """
        Overload of the nextId method

        Returns
        -------
        PageNewExperiment if this was selected, or PageSearchExperiment otherwise.
        """
        if self.field('new_experiment'):
            return WizardPage.PageNewExperiment
        else:  # open existing experiment
            return WizardPage.PageSearchExperiment

    def update_settings(self):
        """
        Update the setting object with the values in the GUI fields.

        Once the setting object is updated, the elog_handle_factory is also updated.

        """
        # for the password field we cannot take directly the value from the field
        self.settings.setValue('elog_password', self._encrypt_pass())

        # for all other parameters, just move the field content to the corresponding setting value.
        self.settings.setValue('elog_user_name', self.elog_user_field.text())
        self.settings.setValue('elog_hostname', self.elog_hostname_field.text())
        self.settings.setValue('elog_port', self.elog_port_field.value())
        self.settings.setValue('elog_use_ssl', self.elog_ssl_check_box.isChecked())
        self.settings.setValue('elog_timeout', self.elog_timeout_spinbox.value())

        self.settings.setValue('protocol_list_logbook', self.protocol_list_logbook_field.text())

        self.settings.setValue('quattro_logbook', self.quattro_elog_logbook_field.text())
        self.settings.setValue('versa_logbook', self.versa_elog_logbook_field.text())
        self.settings.setValue('vega_logbook', self.vega_elog_logbook_field.text())
        self.settings.setValue('xl40gb_logbook', self.xl40gb_elog_logbook_field.text())
        self.settings.setValue('xl40cold_logbook', self.xl40cold_elog_logbook_field.text())

        self.settings.setValue('network_folder', str(Path(self.network_folder.text())))
        self.settings.setValue('quattro_local_folder', str(Path(self.quattro_local_path.text())))
        self.settings.setValue('versa_local_folder', str(Path(self.versa_local_path.text())))
        self.settings.setValue('vega_local_folder', str(Path(self.vega_local_path.text())))
        self.settings.setValue('xl40gb_local_folder', str(Path(self.xl40gb_local_path.text())))
        self.settings.setValue('xl40cold_local_folder', str(Path(self.xl40gb_local_path.text())))

        elog_handle_factory.set_connection_parameters(ELOGConnectionParameters.from_qsettings(self.settings))

    def _encrypt_pass(self) -> str:
        """
        Encrypt the password.

        To avoid double encryption, this method is performed only if strictly needed.

        Returns
        -------
        The encrypted password.
        """
        if self.password_needs_update:
            self.elog_password_field.setText(encrypt_pass(self.elog_password_field.text()))
            self.password_needs_update = False
        return self.elog_password_field.text()

    def restore_defaults(self):
        """
        Restore all the fields to the default values.

        The default values are stored in the constants module.
        """
        # put the default values in the settings
        for key, value in default_settings.items():
            self.settings.setValue(key, value['value'])

        # transfer the settings to the GUI
        self.initializePage()

        # remember that the password is already encrypted
        self.password_needs_update = False
