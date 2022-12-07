#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit

from time import sleep

from PyQt4.QtCore import QTranslator

from PyQt4.QtGui import QApplication, QVBoxLayout
from PyQt4.QtGui import QMainWindow, QDialog, QFrame
from PyQt4.QtGui import QLabel, QRadioButton, QMessageBox

import bluetooth, functools

# Files generated with the pyuic4 command
from SMS import Ui_SMS
from SMS_Help import Ui_Help
from SMS_Send import Ui_SMSDetails


# In python, the 'self' key is used to make a variable
# available from anywhere in the class body.
# The self.tr method allows you to use the linguist utility
# to translate the application.

# A class to access to the help dialog
class Help(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        self.gui = Ui_Help()
        self.gui.setupUi(self)


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_SMS()
        self.ui.setupUi(self)

        # Create the signals needed; use the 'triggered' signal.
        self.ui.actionSend.triggered.connect(self.sendTriggered)
        self.ui.actionHelp.triggered.connect(self.helpTriggered)
        self.ui.actionInbox.triggered.connect(self.inboxTriggered)
        self.ui.actionRefresh.triggered.connect(self.refreshTriggered)

        # Layout to be set to the main widget
        self.widgetLayout = QVBoxLayout()

        # Socket object to make the bluetooth link
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        # address and channel to establish the connection
        self.address = ""
        self.channel = 0
        self.delay = 2

    # Look up for nearly devices
    def refreshDevices(self):
        self.devices = bluetooth.discover_devices(lookup_names=True)  # Store human name

    # Slot 'refreshTriggered' triggered with the actionRefresh action
    def refreshTriggered(self):
        try:
            self.refreshDevices()
        except bluetooth.BluetoothError, e:  # Throwed when Bluetooth is Off
            label = QLabel(self.tr(e.message))
            self.widgetLayout.addWidget(label)
            self.ui.scrollAreaWidgetContents.setLayout(self.widgetLayout)
            return

        # Refresh the widget element with the nearly devices
        if len(self.devices) > 0:
            self.clearLayout(self.widgetLayout)
            self.ui.actionSend.setEnabled(False)
            self.ui.actionInbox.setEnabled(False)
            message = QLabel(self.tr("Chose from the mobile devices below:"))

            self.widgetLayout.addWidget(message)

            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)

            self.widgetLayout.addWidget(separator)

            for address, name in self.devices:
                deviceName = QLabel("    " + address)
                radio = QRadioButton(name)

                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)

                # add components to layout
                self.widgetLayout.addWidget(radio)
                self.widgetLayout.addWidget(deviceName)
                self.widgetLayout.addWidget(separator)

                # Send the address to connect. The 'functools' module is used to
                radio.toggled.connect(functools.partial(self.radioToggled, address))

            self.ui.scrollAreaWidgetContents.setLayout(self.widgetLayout)
            self.widgetLayout.addStretch(1)  # Important to stetic :)
        else:
            message = self.tr("No devices found.\n\t")
            message += self.tr("Check that the device you are searching for\n\t")
            message += self.tr("has Bluetooth switched on and is set visible.")

            self.widgetLayout.addWidget(QLabel(message))
            self.ui.scrollAreaWidgetContents.setLayout(self.widgetLayout)

    # Slot 'radioToggled' triggered when the radio button is toggled
    def radioToggled(self, address):  # param address to connect
        self.ui.actionInbox.setEnabled(True)  # Enable the actionInbox action
        self.ui.actionSend.setEnabled(True)  # Enable the actionSend action
        self.address = address  # Setting the address to connect

    # Clear the widget layout
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    # Slot 'sendTriggered' triggered with the actionSend action
    def sendTriggered(self):
        self.lookUpForDUN()
        if self.channel == 0:
            return

        edit_sms = QDialog()
        aux = Ui_SMSDetails()  # Create a SMSDetails dialog
        aux.setupUi(edit_sms)  # Load the dialog

        r = edit_sms.exec_()  # Store response from dialog in r

        # The user accept to send the SMS message
        if r:
            # Get phone number from the QDialog
            phone_number = str(aux.lineEdit.text())
            sms_data = str(aux.plainTextEdit.toPlainText())
            for addr, name in self.devices:
                if addr == self.address:
                    try:
                        self.connectToDevice()
                    except bluetooth.BluetoothError, e:
                        message = self.tr(e.message)
                        QMessageBox.critical(self, "Error", message)
                        return

                    # Configure the mobile target, add 52 = Mexico code
                    mobile = '52' + phone_number  # ten digits

                    self.socket.send('AT+CMGF=1\r')  # Text mode again
                    sleep(self.delay)
                    print
                    self.socket.recv(1024)
                    command = 'AT+CMGS="+' + mobile + '"\r'  # Prepare command to send
                    print
                    "%r" % command
                    self.socket.send(command)  # Configure the mobile
                    sleep(self.delay)
                    print
                    self.socket.recv(1024)

                    self.socket.send(sms_data + chr(26))  # Send the message text with
                    # the Cotrol+Z = chr(26) commbination
                    sleep(self.delay)
                    print
                    self.socket.recv(1024)

                    sleep(self.delay)
                    self.socket.close()  # Close the socket connection

    # Look up for Dial-up networking is DUN
    def lookUpForDUN(self):
        # Look up for services offerted by the mobile device choosed
        services = bluetooth.find_service(address=self.address)
        # Sometimes there's no services offerted, so we need to know that
        if len(services) > 0:
            self.info = self.tr('Please wait ...\n')
            self.info += self.tr('Looking for Dial-up networking service...\n\n')
            for service in services:
                # The service name can be found in three ways
                name = service["name"]
                if name == "Dial-up networking" or name == "Dial-Up Networking" or name == "Dial-up Networking":
                    # Store the port
                    self.channel = service["port"]
                    self.info += self.tr("Found Dial-up networking at channel ")
                    self.info += self.channel
                    message_title = self.tr("Information")
                    QMessageBox.information(self, message_title, self.info)
                    break
        else:
            error = self.tr("No available services\nTry another device, please.")
            message_title = self.tr("Error message")
            QMessageBox.critical(self, message_title, error)
            return

        # There's no Dial-up networking
        if self.channel == 0:
            error = self.tr("No Dial-up networking service detected!\nTry another device, please.")
            message_title = self.tr("Error message")
            QMessageBox.critical(self, message_title, error)
            return

    # The connectToDevice method once the address and channel is ready
    def connectToDevice(self):
        self.socket.connect((self.address, self.channel))
        self.channel = 0

    # Slot 'inboxTriggered' triggered with the actionInbox action
    def inboxTriggered(self):
        # First look up for Dial-up networking
        self.lookUpForDUN()
        if self.channel == 0:
            return

        # Throw an exception when cannot connect
        try:
            self.connectToDevice()
        except bluetooth.BluetoothError, e:
            message = self.tr(e.message)
            QMessageBox.critical(self, "Error", message)
            return

        # Set the SMS mode (1 = text mode, 0 = PDU mode)
        self.socket.send('AT+CMGF=1\r')  # an at command!!!
        sleep(self.delay)  # Wait a second
        print
        self.socket.recv(1024)  # Show result

        # Does it support read
        self.socket.send('AT+CPMS=?')
        sleep(self.delay)
        print
        self.socket.revc(1024)  # Print response

        # Set the storage to read
        self.socket.send('AT+CPMS="SM"\r')  # SM = memoria SIM
        sleep(self.delay)
        self.socket.recv(1024)

        # Retrieve all messages from the storage specified
        self.socket.send('AT+CMGL="ALL"\r')
        sleep(self.delay)
        print
        self.socket.recv(1024)

        sleep(self.delay)
        self.socket.close()  # Close the socket

    # Slot 'helpTriggered' triggered with the actionHelp action
    def helpTriggered(self):
        aux = Help()
        aux.exec_()


# Here begin all
if __name__ == "__main__":  # Application Start point
    app = QApplication(argv)

    # Set the spanish translator ;)
    translator = QTranslator(app)
    translator.load("lang_es")
    app.installTranslator(translator)

    SMSMain = Main()
    SMSMain.show()
    exit(app.exec_())