try:
    import sys
    import random
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtWidgets import QGraphicsOpacityEffect

    import threading
    import time
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Please install the required modules using pip: 'pip install {str(e).split(' ')[3].replace("\'", "")}'")
    while True:
        pass


#Functions
class Timer:
    def __init__(self):
        self.timers = {}
        self.timer_id = 0
    
    def setInterval(self, fn, time, *args):
        def interval_callback():
            fn(*args)
            if timer_id in self.timers:
                self.timers[timer_id] = threading.Timer(time/1000, interval_callback)
                self.timers[timer_id].start()

        timer_id = self.timer_id
        self.timer_id += 1
        self.timers[timer_id] = threading.Timer(time/1000, interval_callback)
        self.timers[timer_id].start()
        return timer_id

    def clearInterval(self, timer_id):
        if timer_id in self.timers:
            self.timers[timer_id].cancel()
            del self.timers[timer_id]

    def setTimeout(self, fn, delay, *args, **kwargs):
        def timer_callback():
            self.timers.pop(timer_id, None)
            fn(*args, **kwargs)
        
        timer_id = self.timer_id
        self.timer_id += 1
        t = threading.Timer(delay / 1000, timer_callback)
        self.timers[timer_id] = t
        t.start()
        return timer_id
    
    def clearTimeout(self, timer_id):
        t = self.timers.pop(timer_id, None)
        if t is not None:
            t.cancel()
t = Timer()

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
        self.radio_button_phone_yes.setChecked(True)
        self.radio_button_phone_no = QtWidgets.QRadioButton("No")


        #Finalize input button
        self.enter_data = QtWidgets.QPushButton("Enter Data")

        #Success message
        self.success_message = QtWidgets.QLabel("")


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
        self.user_viewer_inputer_grid.rowCount = 6
        self.user_viewer_inputer_grid.addWidget(self.name_label, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.name_input, 1, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.age_label, 2, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.age_input, 2, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.phone_label, 3, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.radio_button_phone_yes, 3, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.radio_button_phone_no, 4, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_inputer_grid.addWidget(self.enter_data, 5, 1, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.user_viewer_inputer_grid.addWidget(self.success_message, 6, 1, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)
        

        #Grid containers

        self.select_add_or_view = QtWidgets.QGroupBox("Select add user or view users")
        self.select_add_or_view.setFixedSize(400, 100)
        self.select_add_or_view.setLayout(self.selector_button_label_grid)

        self.information_input = QtWidgets.QGroupBox("Information input")
        self.information_input.setFixedSize(400, 200)
        self.information_input.setLayout(self.user_viewer_inputer_grid)

        self.layout.addWidget(self.select_add_or_view)
        self.layout.addWidget(self.information_input)

        self.enter_data.clicked.connect(self.save_data)

    

    @QtCore.Slot()
    def save_data(self):
        if self.name_input.displayText().strip(" ") == "": 
            self.success_message.setText("You must input a name!")
            self.success_message.setStyleSheet("color: red;")
            t.setTimeout(self.hide_success_message, 3000)

            return
        print(self.name_input.displayText())
        self.name_input.setText("")
        print(self.age_input.value())
        self.age_input.setValue(0)
        print("Does have a phone" if self.radio_button_phone_yes.isChecked() else "Does not have a phone")
        self.radio_button_phone_yes.setChecked(True)
        self.radio_button_phone_no.setChecked(False)

        self.success_message.setText("Data entered successfully!")
        self.success_message.setStyleSheet("color: green;")
        t.setTimeout(self.hide_success_message, 3000)

    def hide_success_message(self):
        self.success_message.setText("")
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setFixedSize(420, 340)
    widget.show()

    sys.exit(app.exec())