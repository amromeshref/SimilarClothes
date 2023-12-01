from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import time
import os

screen_helper = """
ScreenManager:
    MainScreen:
    StoreScreen:
    StoreCameraScreen:
    PhotoScreen:
    ResultScreen:
    
<MainScreen>:
    name: 'main'
    MDRectangleFlatButton:
        text: 'Store'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press: root.manager.current = 'store'

<StoreScreen>:
    name: 'store'
    MDTextField:
        id: storename
        hint_text: "Store Name"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
    MDRaisedButton:
        text: 'Shirt'
        on_release: root.shirt()
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
    MDRaisedButton:
        text: 'Jeans'
        on_release: root.jeans()
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
    MDRaisedButton:
        text: 'Shoes'
        on_release: root.shoes()
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    MDRaisedButton:
        text: 'Jacket'
        on_release: root.jacket()
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}


<StoreCameraScreen>:
    name: 'storecamera'
    MDLabel:
        text: 'Capture 10 images'
        pos_hint: {'center_x': 0.5, 'center_y': 0}
    Camera:
        id: cameras
        resolution: (640,480)
        play: True
    MDRaisedButton:
        text: 'Capture'
        on_release: root.Capture()
        pos_hint: {'center_x': 0.5}

<PhotoScreen>:
    name: 'photo'
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size
    FileChooserIconView:
        id: filechooser
        path: "."
        on_selection: root.selected(filechooser.selection)
<ResultScreen>:
    name: 'result'
    MDLabel:
        text: 'this is result screen'
        halign: 'center'
        valign: 'center'
"""
class MainScreen(Screen):
    pass

directory = None


class StoreScreen(Screen):
    def shirt(self):
        global directory
        directory = "./" + self.ids.storename.text + "/shirts"
        os.makedirs(directory)
        os.mkdir(directory + "/anchor")
        os.mkdir(directory + "/pos")
        os.mkdir(directory + "/neg")
        app = MDApp.get_running_app()
        app.root.current = 'storecamera'

    def jeans(self):
        global directory
        directory = "./" + self.ids.storename.text + "/jeans"
        os.makedirs(directory)
        os.mkdir(directory + "/anchor")
        os.mkdir(directory + "/pos")
        os.mkdir(directory + "/neg")
        app = MDApp.get_running_app()
        app.root.current = 'storecamera'

    def shoes(self):
        global directory
        directory = "./" + self.ids.storename.text + "/shoes"
        os.makedirs(directory)
        os.mkdir(directory + "/anchor")
        os.mkdir(directory + "/pos")
        os.mkdir(directory + "/neg")
        app = MDApp.get_running_app()
        app.root.current = 'storecamera'

    def jacket(self):
        global directory
        directory = "./" + self.ids.storename.text + "/jacket"
        os.makedirs(directory)
        os.mkdir(directory + "/anchor")
        os.mkdir(directory + "/pos")
        os.mkdir(directory + "/neg")
        app = MDApp.get_running_app()
        app.root.current = 'storecamera'


class StoreCameraScreen(Screen):
    counter = 0

    def Capture(self):
        timenow = time.strftime("%Y%m%d_%H%M%S")
        # Accessing the Camera widget using root.ids
        if self.counter == 0:
            self.directory = directory + f"/anchor/myimage_{timenow}.png"
            self.ids.cameras.export_to_png(self.directory)
            self.counter += 1
        elif self.counter < 10:
            self.directory = directory + f"/pos/myimage_{timenow}.png"
            self.ids.cameras.export_to_png(self.directory)
            self.counter += 1
        else:
            self.counter = 0
            app = MDApp.get_running_app()
            app.root.current = 'result'


class PhotoScreen(Screen):
    def selected(self, filename):
        path = filename[0]
        app = MDApp.get_running_app()
        app.root.current = 'result'
        print(path)

class ResultScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))
sm.add_widget(StoreScreen(name="store"))
sm.add_widget(StoreCameraScreen(name="storecamera"))
sm.add_widget(ResultScreen(name="result"))

class DemoApp(MDApp):
    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


DemoApp().run()
