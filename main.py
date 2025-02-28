try:
    import sys
    import json
    import os
    from PySide6 import QtCore, QtWidgets, QtGui
    from PySide6.QtWidgets import QGraphicsOpacityEffect
    import threading
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Please install the required modules using pip: 'pip install {str(e).split(' ')[3].replace("\'", "")}'")
    while True:
        pass

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to people.json relative to the script location
people_file = os.path.join(script_dir, 'people.json')

#Functions
class Timer:
    def __init__(self):
        self.timers = {}
        self.timer_id = 0
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
t = Timer()

def readFile(fileName):
    try:
        with open(fileName, 'r', encoding='utf-8') as filePreload:
            fileJson = json.load(filePreload)
            return fileJson
    except json.decoder.JSONDecodeError:
        return []
    
def save_person_to_file(save_data, pre_save_data):
    with open(people_file, "w") as file:
        pre_save_data.append(save_data)
        json.dump(pre_save_data, file)

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self) #Creates the layout for the entire widget. Anything being added gets added to this class

        self.new_person_screen_seletected = True
        self.user_index = 0
        
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

        #View person data
        self.name_label_viewer = QtWidgets.QLabel("Name:")
        self.age_label_viewer = QtWidgets.QLabel("Age:")
        self.phone_label_viewer = QtWidgets.QLabel("")

        self.name_value = QtWidgets.QLabel("")
        self.age_value = QtWidgets.QLabel("")
        self.previous_person = QtWidgets.QPushButton("Previous")
        self.next_person = QtWidgets.QPushButton("Next")

        self.success_message_person_viewer = QtWidgets.QLabel("")


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
            #Creates the grid for viewing all peoples information
        self.user_viewer_viewer = QtWidgets.QGridLayout()
        self.user_viewer_viewer.columnCount = 2
        self.user_viewer_viewer.rowCount = 5
        self.user_viewer_viewer.addWidget(self.name_label_viewer, 1, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_viewer.addWidget(self.name_value, 1, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_viewer.addWidget(self.age_label_viewer, 2, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_viewer.addWidget(self.age_value, 2, 2, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_viewer.addWidget(self.phone_label_viewer, 3, 1, 1, 2, QtGui.Qt.AlignmentFlag.AlignCenter)
        self.user_viewer_viewer.addWidget(self.previous_person, 4, 1, QtGui.Qt.AlignmentFlag.AlignLeft)
        self.user_viewer_viewer.addWidget(self.next_person, 4, 2, QtGui.Qt.AlignmentFlag.AlignRight)
        self.user_viewer_viewer.addWidget(self.success_message_person_viewer, 5, 1, 1, 2, QtCore.Qt.AlignmentFlag.AlignCenter)

        

        #Grid containers

        self.select_add_or_view = QtWidgets.QGroupBox("Select add user or view users")
        self.select_add_or_view.setFixedSize(400, 100)
        self.select_add_or_view.setLayout(self.selector_button_label_grid)

        self.information_input = QtWidgets.QGroupBox("Information input")
        self.information_input.setFixedSize(400, 200)
        self.information_input.setLayout(self.user_viewer_inputer_grid)

        self.person_viewer = QtWidgets.QGroupBox("Person Viewer")
        self.person_viewer.setFixedSize(400, 200)
        self.person_viewer.setLayout(self.user_viewer_viewer)
        self.person_viewer.hide()

        self.layout.addWidget(self.select_add_or_view)
        self.layout.addWidget(self.information_input)
        self.layout.addWidget(self.person_viewer)

        self.enter_data.clicked.connect(self.save_data)
        self.selector_button.clicked.connect(self.change_screen)

        self.previous_person.clicked.connect(self.previous_person_viewer)
        self.next_person.clicked.connect(self.next_person_viewer)

    

    @QtCore.Slot()
    def next_person_viewer(self):
        if self.user_index == len(readFile(people_file)) - 1:
            self.success_message_person_viewer.setText("No more people to display!")
            self.success_message_person_viewer.setStyleSheet("color: red;")
            t.setTimeout(self.hide_success_message, 3000)
            return
        self.user_index += 1
        self.update_person_viewer()
    
    def previous_person_viewer(self):
        if self.user_index == 0:
            self.success_message_person_viewer.setText("Already at the first person!")
            self.success_message_person_viewer.setStyleSheet("color: red;")
            t.setTimeout(self.hide_success_message, 3000)
            return
        self.user_index -= 1
        self.update_person_viewer()

    def update_person_viewer(self):
        people_data = readFile(people_file)
        self.name_value.setText(people_data[self.user_index]['name'])
        self.age_value.setText(str(people_data[self.user_index]['age']))
        self.phone_label_viewer.setText("They have a phone" if people_data[self.user_index]['phone'] else "They don\'t have a phone")
    def change_screen(self):
        if self.new_person_screen_seletected:
            people_data = readFile(people_file)
            if len(people_data) < 1:
                self.success_message.setText("No people data found!")
                self.success_message.setStyleSheet("color: red;")
                t.setTimeout(self.hide_success_message, 3000)
                return
            self.new_person_screen_seletected = False
            self.selector_button.setText("Add New Person")
            self.selector_title.setText("Displaying Person Data")
            self.information_input.hide()
            self.person_viewer.show()
            
            self.name_value.setText(people_data[self.user_index]['name'])
            self.age_value.setText(str(people_data[self.user_index]['age']))
            self.phone_label_viewer.setText("They have a phone" if people_data[self.user_index]['phone'] else "They don\'t have a phone")
        elif not self.new_person_screen_seletected:
            self.new_person_screen_seletected = True
            self.selector_button.setText("Show All")
            self.selector_title.setText("Collecting Person Data")
            self.information_input.show()
            self.person_viewer.hide()

    def save_data(self):
        if self.name_input.displayText().strip(" ") == "": 
            self.success_message.setText("You must input a name!")
            self.success_message.setStyleSheet("color: red;")
            t.setTimeout(self.hide_success_message, 3000)

            return
        self.success_message.setText("Data entered successfully!")
        self.success_message.setStyleSheet("color: green;")
        t.setTimeout(self.hide_success_message, 3000)
        save_data = {
            "name": self.name_input.displayText(),
            "age": self.age_input.value(),
            "phone": self.radio_button_phone_yes.isChecked()  # Returns True if yes, False if no
        }
        pre_save_data = readFile(people_file)
        save_person_to_file(save_data, pre_save_data)

        self.name_input.setText("")
        self.age_input.setValue(0)
        self.radio_button_phone_yes.setChecked(True)
        self.radio_button_phone_no.setChecked(False)

    def hide_success_message(self):
        self.success_message.setText("")
    
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    widget = MyWidget()
    widget.setFixedSize(420, 340)
    widget.setWindowTitle("User Information System")
    widget.show()

    sys.exit(app.exec())