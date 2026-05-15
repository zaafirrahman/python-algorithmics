class Widget():
    #properties (fields)
    def __init__(self, title_text, x_num, y_num):
        self.title = title_text
        self.x = x_num
        self.y = y_num


    #methods
    def print_info(self):
        print('Label:', self.title)
        print('Location:', self.x, self.y)


class Button(Widget):
    def __init__(self, title_text, x_num, y_num, is_clicked_bool):
        super().__init__(title_text, x_num, y_num)
        self.is_clicked = is_clicked_bool
    def click(self):
        self.is_clicked = True
        print('You are signed up')


lotery_button = Button('Participate', 100, 100, False)
lotery_button.print_info()
answer = input('Want to sign up? (yes/no): ')
if answer == 'yes':
    lotery_button.click()
else:
    print("That's a shame!")
