class Title():
    def __init__(self, title_text, x_num, y_num):
        self.title = title_text
        self.x = x_num
        self.y = y_num
        self.appearance = True
    def hide(self):
        self.appearance = False
        print(self.title, '- hidden')
    def show(self):
        self.appearance = False
        print(self.title, '- displayed')
    def print_info(self):
        print('Button:', self.title)
        print('Position:', '(' + str(self.x) + ',' + str(self.y) + ')')
        print('Visibility:', self.appearance)


main_title = Title('Cari tahu pemenangnya sekarang!', 150, 50)
rules_title = Title('Hanya ada satu pemenang', 150, -100)
main_title.print_info()
rules_title.print_info()
rules_title.hide()
