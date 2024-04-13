"""Converter UI"""
import tkinter as tk

import time
from paho.mqtt import client as MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)
import socket
import json

import datetime


class CatUI(tk.Tk):
    """User Interface for a unit converter.

    The UI displays units and handles user interaction.  It invokes
    a UnitConverter object to perform actual unit conversions.
    """

    def __init__(self, mqtt_channal):
        """initialize ui"""
        super().__init__()
        self.mqtt_channal = mqtt_channal
        self.init_components()

    def check_wifi_connection(self):
        try:
            # Check WiFi connection
            socket.create_connection(("www.google.com", 80), timeout=2)
            return True
        except Exception as wifi_error:
            return self.check_wifi_connection(self)

    def check_mqtt_connection(self,MQTT_BROKER):
        try:
            # Check MQTT connection
            socket.create_connection((MQTT_BROKER, 1883), timeout=2)
            return True
        except Exception as mqtt_error:
            return self.check_mqtt_connection(self,broker_address)

    def connect(self):

        self.mqtt = MQTTClient(client_id="",
                          server=MQTT_BROKER,
                          user=MQTT_USER,
                          password=MQTT_PASS)

    def init_components(self):
        """Create components and layout the UI."""

        self.leftinput = tk.StringVar()
        self.rightinput = tk.StringVar()

        # left input field
        self.leftfield = tk.Entry(self, width=20, textvariable=self.leftinput)
        # label '='
        label = tk.Label(self, text="=")
        # right input field
        self.rightfield = tk.Entry(self, width=20, textvariable=self.rightinput)
        # Send button
        send_button = tk.Button(self, text="Send", command=self.send_handler)
        # clear button
        clear_button = tk.Button(self, text="Clear", command=self.clear_handler)

        # Enter bind
        self.leftfield.bind('<Return>', self.send_handler)
        self.rightfield.bind('<Return>', self.send_handler)

        # layout
        padding = {'padx': 10, 'pady': 10}
        # position & size the components
        self.leftfield.pack(side=tk.LEFT, **padding, expand=True, fill=tk.X)
        label.pack(side=tk.LEFT, **padding)
        self.rightfield.pack(side=tk.LEFT, **padding, expand=True, fill=tk.X)
        clear_button.pack(side=tk.RIGHT, **padding)
        send_button.pack(side=tk.RIGHT, **padding)

    def send_handler(self, *args):
        """An event handler for conversion actions.
        You should call the unit converter to perform actual conversion.
        """
        try:
            time = datetime.datetime(self.leftinput)
            cat = int(self.rightinput)
            data = {
                'time':time,
                'cat':cat
            }
            MQTTClient.single(self.mqtt_channal, data, hostname=broker_address, auth={'username': username, 'password': password})


        except ValueError:
            self.leftfield.configure(text='ERROR', fg='red')
            self.rightfield.configure(text='ERROR', fg='red')
            self.clear_handler()

    def do_nothing(self, *args):
        pass

    def clear_handler(self, *args):
        """clears both input fields"""
        self.leftinput.set("")
        self.rightinput.set("")

    def run(self):
        """start the app, wait for events"""
        self.mainloop()
