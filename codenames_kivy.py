from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.textinput import TextInput

import codenames_v2

#energy = 100
#hours = 4

class Hello(FloatLayout):

    def __init__(self,**kwargs):
        self.default_label = 'HERE WE GO, SPIES.'
        self.count = 0
        super(Hello,self).__init__(**kwargs)

        self.main_label = Label(text=self.default_label,
                                size_hint=(1, .55),
                                pos_hint={'x':0, 'y':.7})

    #Main Buttons
        self.toggle_text_button = Button(text = "Toggle ",
                                         size_hint=(.3, .1),
                                         pos_hint={'x':.1, 'y':.1},
                                         background_color=(1,0,0,1),
                                         on_press=self.update)
        self.toggle_color_button = Button(text = "Toggle",
                                          size_hint=(.3, .1),
                                          pos_hint={'x':.6, 'y':.1},
                                          background_color=(1,0,0,1),
                                          on_press=self.callback)
        for i in range(10):
            button = Button(text='B' + str(i))
            self.ids.grid.add_widget(button)

        self.dropdown_menu = DropDown()
        for index in range(10):
            btn = Button(text='Value %d' % index, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown_menu.select(btn.text))
            self.dropdown_menu.add_widget(btn)
        self.main_dropdown = Button(text='Hopes/Dreams',
                                    pos_hint={'x':.2,'y':.5},
                                    size_hint=(None, .05))
        self.main_dropdown.bind(on_release=self.dropdown_menu.open)
    # Make them things.
        self.add_widget(self.main_label)

        self.add_widget(self.toggle_text_button)
        self.add_widget(self.toggle_color_button)
        self.add_widget(self.main_dropdown)

    def update(self,event):
        self.count += 1
        if self.count % 2 == 0:
            self.main_label.text = self.default_label
        else:
            self.main_label.text = "Buckle up. It's a long way."

    def update_button(self, event):
        print(event)
        event.text = 'welp event text'

    def modify(self, vector, change_vec):
        for i in range(0,len(vector)):
            vector[i] += change_vec[i]
        for i in range(0, len(vector)):
            vector[i] = vector[i]%2
        return vector

    def callback(self, value):
        print(value.background_color)
        value.background_color = self.modify(value.background_color, (1,0,1,0))


class Grid(GridLayout):
    def __init__(self, cols, label_text, padding, spacing):
        super().__init__()
        self.cols = cols
        self.padding = padding
        self.spacing = spacing

        self.create_labels_from(label_text)

    def update_tile_color(self, tile):
        tile.disabled = True
        tile.background_disabled_normal = ''
        tile.background_color = tile.disabled_color
        tile.disabled_color = (1,1,1,1)

    def create_labels_from(self, args):
        for tile in args:
            self.add_widget(Button(text=tile.value,
                                   background_normal = '',
                                   background_color=(.6,.5,.4,.5),
                                   disabled_color=tile.color,
                                   on_press=self.update_tile_color))

class MyApp(App):
    def __init__(self, board):
        super().__init__()
        self.board = board

    def build(self):
        labs = []
        [labs.append(i.value) for i in self.board]
        print(labs)
        return Grid(5, self.board, padding=(20,20,20,20), spacing=(2, 2))


def main():
    board = codenames_v2.board()

    #for i in board:
    #    print(i.value)
    #World().run()
    my_app = MyApp(board)
    my_app.run()

if __name__ == "__main__":
    main()
