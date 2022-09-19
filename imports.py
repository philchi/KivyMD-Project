from datetime import datetime
import time as t
import pytz as pt
import kivy
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.clock import Clock
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.label import MDLabel
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.list import OneLineListItem
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.list.list import MDList
import winsound
from kivy.uix.gridlayout import GridLayout
import os
from kivymd.uix.list import OneLineAvatarIconListItem