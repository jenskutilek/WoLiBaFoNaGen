from vanilla import Window, Button, TextBox

class WindowDemo:

    def __init__(self):
        self.w = Window((200, 70), "Window Demo")
        self.w.myButton = Button((10, 10, -10, 20), "My Button")
        self.w.myTextBox = TextBox((10, 40, -10, 17), "My Text Box")
        self.w.open()

WindowDemo()