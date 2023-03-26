import json
from io import BytesIO

import kivy
import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from navigation_screen_manager import NavigationScreenManager

# Variables globales
first_time = True
data = None

Builder.load_file("home.kv")
kivy.require('2.1.0')


class MyScreenManager(NavigationScreenManager):
    pass

class HomeScreen(AnchorLayout):
    pass

class InscriptionForm(BoxLayout):

    def get_inputs(self):
        inputs = []
        for child in self.children:
            if isinstance(child, kivy.uix.textinput.TextInput):
                print("Nom :", child.text)
                inputs.append(child.text)

        # inputs[0] - mot de passe
        # inputs[1] - email
        # inputs[2] - pseudo ou username
        # inputs[3] - prenom
        # inputs[4] - nom
        # data = {'name': inputs[4], 'username': inputs[3], 'firstname': inputs[2], 'email': inputs[1], 'mot_de_passe': inputs[0]}
        # json.dumps(data)
        # print(data)
        data = {'name': inputs[4], 'username': inputs[2], 'firstname': inputs[3], 'email': inputs[1]}

        myjson = {
            "username": "admin",
            "password": "admin"}
        url = 'http://127.0.0.1:8000/api/token/'
        r = requests.post(url, json=myjson).text
        tokens = json.loads(r)
        token = 'Bearer' + ' ' + str(tokens['access'])

        header = {'Authorization': token}
        url = 'http://127.0.0.1:8000/api/revendeurs/'
        response = requests.post(url, json=data, headers=header)
        print(response)
        print(response.json())
        # TODO 4 : Envoyé ces informations à l'API - input contient les informations à envoyé


class Connexion(AnchorLayout):
    pass


class ProductCatalog(Screen):

    def on_enter(self):
        global first_time
        if (first_time):
            first_time = False
            product_catalog_kv = ''' 
BoxLayout:
    id: myb
    orientation: "vertical"
    padding: "10dp"
    spacing: "10dp"
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0  # Couleur de fond noir
        Rectangle:
            pos: self.pos
            size: self.size

    FloatLayout:
        size_hint_y: 0.35

        Image:
            keep_ratio: False
            allow_stretch: True
            source: "Im/differents-cafes-1024x683-c-default.jpg"
            size_hint: 1, 1
            pos_hint: {"x": 0, "y": 0}

        Button:
            text: "< Retour"
            halign: "left"
            size_hint: 0.1, 0.15
            pos_hint: {"x": 0, "top": 1}
            background_color: 0.44, 0.26, 0.14, 1  # Couleur du bouton en dégradé de marron
            color: 0.96, 0.87, 0.70, 1  # Couleur du texte blanc
            on_press:
                app.manager.pop()

    ScrollView:
        id : my_scrollview
        size_hint_y: 0.65
        BoxLayout:
            id: product_list
            orientation: "vertical"
            size_hint_y: None
            height: self.minimum_height
'''

            self.add_widget(Builder.load_string(product_catalog_kv))
            for child in self.children:
                for child2 in child.children:
                    if isinstance(child2, kivy.uix.scrollview.ScrollView):
                        for child3 in child2.children:
                            if isinstance(child3, kivy.uix.boxlayout.BoxLayout):

                                # Ouverture du fichier JSON
                                with open('prod.json') as f:
                                    # Lecture du contenu du fichier
                                    global data
                                    data = json.load(f)

                                # Affichage des données chargées
                                #print(data[1]['id'])
                                # Nombre de produits
                                nb_product = len(data)

                                # print("LONGEUR DE LA CHAINE DU LABEL", len(detail2))
                                for i in range(nb_product):

                                    # Les clé qui serons utilisées
                                    id = data[i]['id']
                                    name = data[i]['name']
                                    description = data[i]['description']
                                    details = data[i]['details']
                                    price = data[i]['price']
                                    stock = data[i]['stock']

                                    child3.add_widget(self.add_product(str(id),"'"+name+"'", "'"+price+"'", "'"+description+"'", "'"+details+"'"))

    def add_product(self, id, name, price, detail, detail2):
        page_nom = "'"+"product_details_page_"+id+"'"
        print(page_nom)
        product_kv = '''
BoxLayout:
    orientation: "horizontal"
    size_hint_y: None
    size_hint_x: 1
    height: "150dp"
    spacing: "10dp"

    Image:
        keep_ratio: False
        allow_stretch: True
        size_hint_x: 0.3
        source: "Im/id_'''+id+'''_a.jpg"

    BoxLayout:
        orientation: "vertical"
        size_hint_x: 0.5
        Label:
            text: '''+name+'''
            font_size: '18sp'
            color: 0.96, 0.87, 0.70, 1  # Couleur du texte en dégradé de marron
            size_hint: 1, None
            height: self.texture_size[1]  # Hauteur du label basée sur la taille du contenu
            text_size: self.width, None  # Définit la largeur maximale pour le texte
            halign: 'left'  # Alignement horizontal du texte, peut être 'left', 'center' ou 'right'
            valign: 'middle'  # Alignement vertical du texte, peut être 'top', 'middle' ou 'bottom'
        Label:
            text: '''+detail+'''
            font_size: '16sp'
            color: 0.96, 0.87, 0.70, 1  # Couleur du texte en dégradé de marron
            size_hint: 1, None
            height: self.texture_size[1]  # Hauteur du label basée sur la taille du contenu
            text_size: self.width, None  # Définit la largeur maximale pour le texte
            halign: 'left'  # Alignement horizontal du texte, peut être 'left', 'center' ou 'right'
            valign: 'middle'  # Alignement vertical du texte, peut être 'top', 'middle' ou 'bottom'
        Label:
            size_hint_y: 0.6
    Label:
        text: '''+price+'''
        font_size: '18sp'
        color: 0.96, 0.87, 0.70, 1  # Couleur du texte en dégradé de marron
        size_hint_x: 0.1

    Button:
        text: "Détails"
        size_hint_x: 0.1
        background_color: 0.44, 0.26, 0.14, 1  # Couleur du bouton en dégradé de marron
        color: 0.96, 0.87, 0.70, 1  # Couleur du texte blanc
        on_press:
            app.build_detail(app.manager, '''+page_nom+''')
            app.manager.push('''+page_nom+''')
'''

        return Builder.load_string(product_kv)



class ProductDetails(Screen):

    def on_enter(self):
        print("j'entr dans "+self.name[len(self.name)-1])
        ids = self.name[len(self.name)-1]
        id = int(self.name[len(self.name)-1])
        name = "'" + data[id-1]['name']+ "'"
        description = "'" +data[id-1]['description']+ "'"
        details = "'" +data[id-1]['details']+ "'"
        stock = '"STOCKS : ' +str(data[id-1]['stock'])+'"'
        price = "'" +data[id-1]['price']+ "'"
        print (data[id-1])
        prod_Detail = '''
BoxLayout:
    orientation: "vertical"
    padding: "10dp"
    spacing: "10dp"

    BoxLayout:
        size_hint_y: 0.1
        Button:
            text: "< Retour"
            halign: "left"
            size_hint_x: 0.1
            background_color: 0.44, 0.26, 0.14, 1  # Couleur du bouton en dégradé de marron
            color: 0.96, 0.87, 0.70, 1 # Couleur du texte blanc
            on_press: app.manager.pop()
        Widget:
            size_hint_x: 0.9

    BoxLayout:
        orientation: "horizontal"
        spacing: "10dp"
        size_hint_y: 0.9
        Carousel:
            direction: 'right'
            size_hint_x: 0.5
            AsyncImage:
                source: "Im/id_'''+ids+'''_a.jpg"
                allow_stretch: True
            AsyncImage:
                source: "Im/id_'''+ids+'''_b.jpg"
                allow_stretch: True
            AsyncImage:
                source: "Im/id_'''+ids+'''_c.jpg"
                allow_stretch: True
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.5
            Label:
                id: product_name
                text: '''+name+'''
                font_size: "18dp"
                size_hint: 1, .3
                valign: 'top'
                color: 0.96, 0.87, 0.70, 1  # Couleur du texte marron foncé
            Label:
                id: product_description
                text: '''+details+'''
                color: 0.96, 0.87, 0.70, 1  # Couleur du texte marron foncé
                size_hint: 1, None
                height: self.texture_size[1]  # Hauteur du label basée sur la taille du contenu
                text_size: self.width, None  # Définit la largeur maximale pour le texte
                halign: 'left'  # Alignement horizontal du texte, peut être 'left', 'center' ou 'right'
                valign: 'middle'  # Alignement vertical du texte, peut être 'top', 'middle' ou 'bottom'
            BoxLayout:
                orientation: "horizontal"
                size_hint: 1, .2
                Label:
                    id: product_description
                    text: '''+stock+'''
                    size_hint: 1, 1
                    color: 0.96, 0.87, 0.70, 1  # Couleur du texte marron foncé
                Label:
                    id: product_description
                    text: '''+price+'''
                    size_hint: 1, 1
                    color: 0.96, 0.87, 0.70, 1  # Couleur du texte marron foncé
'''
        self.add_widget(Builder.load_string(prod_Detail))


class QRcode(Screen):

    def authentification(self, app_manager):
        labels = []
        for child in self.children:
            box_layout = child
            children2 = box_layout.children
            for child2 in children2:
                if isinstance(child2, kivy.uix.label.Label):
                    labels.append(child2)
        info_qrcode = labels[2].text

        if (len(info_qrcode) > 0):
            tokens = info_qrcode[info_qrcode.find("access") + 10:len(info_qrcode) - 3]
            print("token =", tokens)
            token = 'Bearer' + ' ' + str(tokens)
            header = {'Authorization': token}
            url = 'http://127.0.0.1:8000/api/products/'
            response = requests.get(url, json=data, headers=header)
            products = response.json()
            products = json.dumps(products)
            print(products)
            with open("prod.json", "w") as outfile:
                outfile.write(str(products))

            # TODO Birane 1 : La variable token contient la clé d'acces
            # vvvvv  fonction pour passer au screen suivant
        productD = app_manager.get_screen("product_catalog_page")
        print(productD.ids)
        print(productD)
        app_manager.push("product_catalog_page")


# TODO Abro 1 : Fonction AR
# TODO Abro 2 : Fonction Affichage des produits
# TODO Abro 3 : Fonction qui prend en argument l'id du produit

class PayTonKawaApp(App):
    manager = ObjectProperty(None)

    def build(self):
        self.manager = MyScreenManager()
        productC = ProductCatalog()
        productC.name = "product_catalog_page"
        self.manager.add_widget(productC)
        productD = ProductDetails()
        productD.name = "product_details_page"
        self.manager.add_widget(productD)
        return self.manager

    def build_detail(self, app_manager, nom_page):
        print(" PRODUCT DETAIL ")
        productD = ProductDetails()

        productD.name = nom_page

        app_manager.add_widget(productD)

PayTonKawaApp().run()

# url = "http://54.221.230.111:8000/api/products/"
# response = requests.get(url)
# data = json.loads(response.text)
# test = 12
# b = 2.00
# dr = "Salut j'ai {} ans et j'ai {} billes".format(test,b)
# print(dr)
# print(r.json())
# myobj = { "name": input[4],"username": input[3],"firstname": input[2],"email": input[1],"mot_de_passe": input[0]}
# x = requests.post(url, myobj)

# response = requests.get(url)
# data = json.loads(response.text)
# print(data)



# Parcourir les données et afficher chaque donnée



