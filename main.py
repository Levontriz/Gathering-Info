import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self) #Creates the layout for the entire widget. Anything being added gets added to this class
        
        #Label for what screen you are on and the button to change to the person viewer
        self.selector_title = QtWidgets.QLabel("Collecting Person Data")
        self.selector_button = QtWidgets.QPushButton("Show All")
        self.selector_button.setFixedSize(100, 30)

        #New person labels and input fields for name and age
        self.name_label = QtWidgets.QLabel("Name:")
        self.age_label = QtWidgets.QLabel("Age:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setValue(0)
        self.age_input.setMaximum(150)

        #Stuff for new users phones
        self.phone_label = QtWidgets.QLabel("Do you have a mobile phone?")
        self.radio_button_phone_yes = QtWidgets.QRadioButton("Yes")
        self.radio_button_phone_no = QtWidgets.QRadioButton("No")



        #grids
            #Creates the grid for the label of what screen you are on and the button to change to the person viewer
        self.selector_button_label_grid = QtWidgets.QGridLayout()
        self.selector_button_label_grid.columnCount = 2
        self.selector_button_label_grid.rowCount = 1
        self.selector_button_label_grid.addWidget(self.selector_title, 1, 1, QtGui.Qt.AlignmentFlag.AlignCenter)
        self.selector_button_label_grid.addWidget(self.selector_button, 1, 2, QtGui.Qt.AlignmentFlag.AlignCenter)
            #Creates the grid for entering new peoples information
        self.user_viewer_inputer_grid = QtWidgets.QGridLayout()
        self.user_viewer_inputer_grid.columnCount = 2
        self.user_viewer_inputer_grid.rowCount = 4
        self.user_viewer_inputer_grid.addWidget(self.name_label, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.name_input, 1, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.age_label, 2, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.age_input, 2, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.phone_label, 3, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.radio_button_phone_yes, 3, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.radio_button_phone_no, 4, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        

        #Grid containers

        self.select_add_or_view = QtWidgets.QGroupBox("Select add user or view users")
        self.select_add_or_view.setFixedSize(400, 100)
        self.select_add_or_view.setLayout(self.selector_button_label_grid)

        self.information_input = QtWidgets.QGroupBox("Information input")
        self.information_input.setFixedSize(400, 200)
        self.information_input.setLayout(self.user_viewer_inputer_grid)

        self.layout.addWidget(self.select_add_or_view)
        self.layout.addWidget(self.information_input)

        #self.button.clicked.connect(self.magic)
        #self.button2.clicked.connect(self.shiga)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
    def shiga(self):
        self.text.setText("Shiga Waga!")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setFixedSize(420, 320)
    widget.show()

    sys.exit(app.exec())