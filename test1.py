#!/usr/bin/env python3
# coding: utf-8

from gi.repository import Gtk

def when_button_is_clicked(label):
    '''
    Quand le bouton est cliqué
    '''
    label.set_text('Hello world!')


builder = Gtk.Builder()
builder.add_from_file('hello.glade')  # Rentrez évidemment votre fichier, pas le miens!

window = builder.get_object('main_window')
# Peut se faire dans Glade mais je préfère le faire ici, à vous de voir
window.connect('delete-event', Gtk.main_quit)

# Le handler
handler = {'on_clicked': when_button_is_clicked}
builder.connect_signals(handler)

window.show_all()
Gtk.main()