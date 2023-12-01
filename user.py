from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.imagelist import MDSmartTile
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image, AsyncImage
import time
import os
from ultralytics import YOLO
import cv2
from ultralytics.yolo.utils.plotting import Annotator
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Layer


clas_model_path = "./data/best.pt"
class_model = YOLO(clas_model_path)


def predict_image(image):
    results = model.predict(image, show_conf=True)
    return results


def Crop_types(results, image, model):
    types = {
        "shirts": [],
        "jeans": [],
        "jackets": [],
        "shoes": []}
    for r in results:
        annotator = Annotator(image)
        boxes = r.boxes
        for box in boxes:
            if (box.conf > 0.6):
                b = box.xyxy[0]
                c = box.cls
                top, left, bottom, right = map(int, b)
                cropped_image = image[left:right, top:bottom]
                types[model.names[int(c)]].append(cropped_image)
    return types


class L1Dist(Layer):
    def __init__(self, **kwargs):
        super(L1Dist, self).__init__(**kwargs)

    def call(self, anchor, validation):
        return tf.abs(anchor - validation)


siamese_model = tf.keras.models.load_model('./data/siamese_model.h5',
                                           custom_objects={'L1Dist': L1Dist})

image_size = (105, 105)


def preprocessingImage(image):
    image = cv2.resize(image, image_size)  # Resizing data into (105,105,3)
    image = image/255.0  # Normalizing the image
    image = image.reshape((1, 105, 105, 3))
    return image


def getSimilarImages(image, type):
    image_path = "./database/images/"  # Path of similar images
    image_info = "./database/info/"  # Info of similar images(store/price)
    anc_image = preprocessingImage(image)
    similar_images = []  # contains similar images and their info

    for img in os.listdir(image_path + type):
        ver_image = cv2.imread(image_path + type + "/" + img)
        ver_image_edited = preprocessingImage(ver_image)
        y_hat = siamese_model.predict([anc_image, ver_image_edited])
        if y_hat[0, 0] >= 0.8:
            file_name_without_extension = os.path.splitext(img)[0]
            file_path = image_info + type + "/" + file_name_without_extension + ".txt"
            with open(file_path, 'r') as file:
                # Read the entire content of the file into a string
                file_content = file.read()
            similar_images.append([ver_image, file_content])
    return similar_images


def multiTypeSimilarImages(types):
    similar_images_total = []  # All similar images for each type
    for type in types:
        for i in range(0, len(types[type])):
            image = types[type][i]
            similar_images_total.append(getSimilarImages(image, type))
    return similar_images_total


def getOutput(image_path):
    input_image = cv2.imread(image_path)
    yolo_results = class_model.predict(input_image, show_conf=True)
    types = Crop_types(yolo_results, input_image, class_model)
    similar_images = multiTypeSimilarImages(types)
    return similar_images

img = []
PATH = "./saved"
screen_helper = """
ScreenManager:
    MainScreen:
    UserScreen:
    CameraScreen:
    PhotoScreen:
    ResultScreen:

<MainScreen>:
    name: 'main'
    MDRectangleFlatButton:
        text: 'User'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_press: root.manager.current = 'user'

<UserScreen>:
    name: 'user'
    MDRectangleFlatButton:
        text: 'Camera'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_press: root.manager.current = 'camera'
    MDRectangleFlatButton:
        text: 'Photo'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_press: root.manager.current = 'photo'

<CameraScreen>:
    name: 'camera'
    Camera:
        id: cameras
        resolution: (640,480)
        play: True
    MDRaisedButton:
        text: 'Capture'
        on_release: root.Capture()
        pos_hint: {'center_x': 0.5}

<PhotoScreen>
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
    on_enter: root.click()
    ScrollView:
        id: scroll
        MDGridLayout:
            id: grid
            padding: 30, 30
            row_default_height: 300
            cols: 4
            spacing: dp(40)

"""

similar_images = None


class MainScreen(Screen):
    pass


class UserScreen(Screen):
    pass


directory = None


class CameraScreen(Screen):
    def Capture(self):
        global similar_images
        global sm
        timenow = time.strftime("%Y%m%d_%H%M%S")
        path = f"myimage_{timenow}.png"
        # Accessing the Camera widget using root.ids
        self.ids.cameras.export_to_png("myimage_{}.png".format(timenow))
        similar_images = getOutput(path)
        app = MDApp.get_running_app()
        app.root.current = 'result'


class PhotoScreen(Screen):
    def selected(self, filename):
        global similar_images
        global sm
        path = filename[0]
        similar_images = getOutput(path)
        for type in similar_images:
            cnt = 0
            for x in type:
                cnt += 1
                cv2.imwrite("./saved/" + str(cnt) + ".jpg", x[0])
        for i in os.listdir(PATH):
            if ".jpg" in i:
                img.append(PATH + "/" + i)
        app = MDApp.get_running_app()
        app.root.current = 'result'
        print(path)



class ResultScreen(Screen):
    def click(self):
        print("clicked")
        for im in img:
            print("Fff : "+im)
            self.ids.grid.add_widget(MDSmartTile(source=im))
    # def img(self):
    #     for im in os.listdir("./saved"):
    #         self.ids.grid.add_widget(MDSmartTile(
    #             source="./saved/"+im))


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))
sm.add_widget(UserScreen(name="user"))
sm.add_widget(CameraScreen(name="camera"))
sm.add_widget(PhotoScreen(name="photo"))
sm.add_widget(ResultScreen(name="result"))


class DemoApp(MDApp):
    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


DemoApp().run()