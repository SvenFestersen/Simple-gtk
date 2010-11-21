#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       unbenannt.py
#       
#       Copyright 2009 Sven Festersen <sven@sven-laptop>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import gobject
import gtk
import pygtk


def show_simple_dialog(title, heading, message, buttons, stock_icon=None, parent=None, default_response=gtk.RESPONSE_ACCEPT):
    flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
    d = gtk.Dialog(title, parent, flags, buttons)
    d.set_default_response(default_response)
    
    hbox = gtk.HBox()
    hbox.show()
    content = d.get_content_area()
    content.pack_start(hbox, False, False)
    
    if stock_icon != None:
        img = gtk.image_new_from_stock(stock_icon, gtk.ICON_SIZE_DIALOG)
        img.show()
        vbox = gtk.VBox()
        vbox.show()
        vbox.pack_start(img, False, False)
        hbox.pack_start(vbox, False, False)
        hbox.set_spacing(12)
        
    vbox_label = gtk.VBox()
    vbox_label.show()
    vbox_label.set_spacing(12)
    hbox.pack_start(vbox_label, False, False)
        
    if heading:
        label = gtk.Label()
        label.set_markup("<b>%s</b>" % heading)
        label.set_line_wrap(True)
        label.set_alignment(0, 0.5)
        label.show()
        vbox_label.pack_start(label, False, False)
    
    
    label = gtk.Label("%s\n" % message)
    label.set_line_wrap(True)
    label.set_alignment(0, 0.5)
    label.show()
    vbox_label.pack_start(label)
    
    d.set_has_separator(False)
    d.set_border_width(6)
    
    response = d.run()
    d.destroy()
    return response


def dialog_yes_no(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_NO, gtk.RESPONSE_REJECT, gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, None, parent, gtk.RESPONSE_ACCEPT)
    return response == gtk.RESPONSE_ACCEPT

def dialog_yes_no_error(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_NO, gtk.RESPONSE_REJECT, gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, gtk.STOCK_DIALOG_ERROR, parent, gtk.RESPONSE_REJECT)
    return response == gtk.RESPONSE_ACCEPT

def dialog_yes_no_question(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_NO, gtk.RESPONSE_REJECT, gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, gtk.STOCK_DIALOG_QUESTION, parent, gtk.RESPONSE_ACCEPT)
    return response == gtk.RESPONSE_ACCEPT

def dialog_yes_no_warning(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_NO, gtk.RESPONSE_REJECT, gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, gtk.STOCK_DIALOG_WARNING, parent, gtk.RESPONSE_REJECT)
    return response == gtk.RESPONSE_ACCEPT

def dialog_ok_cancel(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, None, parent, gtk.RESPONSE_ACCEPT)
    return response == gtk.RESPONSE_ACCEPT

def dialog_ok_cancel_error(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, gtk.STOCK_DIALOG_ERROR, parent, gtk.RESPONSE_REJECT)
    return response == gtk.RESPONSE_ACCEPT

def dialog_ok_cancel_warning(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, gtk.STOCK_DIALOG_WARNING, parent, gtk.RESPONSE_REJECT)
    return response == gtk.RESPONSE_ACCEPT

def dialog_ok_info(title, heading, message, parent=None):
    buttons =  (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
    response = show_simple_dialog(title, heading, message, buttons, gtk.STOCK_DIALOG_INFO, parent, gtk.RESPONSE_ACCEPT)
    return response == gtk.RESPONSE_ACCEPT
    
    
    
class WorkingDialog(gtk.Dialog):
    
    __gsignals__ = {"cancelled": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [])}
    
    _working = True
    
    def __init__(self, title, heading, message, current_action, can_cancel, parent=None):
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        gtk.Dialog.__init__(self, title, parent, flags)
        
        self.connect("destroy", self._cb_destroy)
        self.connect("response", self._cb_response)
        self.set_border_width(6)
        self.set_has_separator(False)
        
        vbox = self.vbox
        vbox.set_spacing(6)
        
        if heading:
            label = gtk.Label()
            label.set_markup("<b>%s</b>" % heading)
            label.set_line_wrap(True)
            label.set_alignment(0, 0.5)
            vbox.pack_start(label, False, False)
            
        label = gtk.Label(message)
        label.set_line_wrap(True)
        label.set_alignment(0, 0.5)
        vbox.pack_start(label, False, False)
        
        self._progress = gtk.ProgressBar()
        self._progress.set_pulse_step(0.04)
        vbox.pack_start(self._progress, False, False)
        
        self._label_action = gtk.Label(current_action)
        self._label_action.set_line_wrap(True)
        self._label_action.set_alignment(0, 0.5)
        vbox.pack_start(self._label_action, False, False)
        
        if can_cancel:
            self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            
        vbox.show_all()
        
    def _cb_destroy(self, widget):
        self._working = False
        
    def _cb_response(self, widget, response):
        if response == gtk.RESPONSE_CANCEL:
            self.emit("cancelled")
        
    def _update(self):
        self._progress.pulse()
        return self._working
        
    def set_current_action(self, action):
        self._label_action.set_label(action)
        
    def run(self):
        gobject.timeout_add(40, self._update)
        res = gtk.Dialog.run(self)
        self.destroy()
        return res
    
    
class ProgressDialog(gtk.Dialog):
    
    __gsignals__ = {"cancelled": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [])}
    
    _working = True
    
    def __init__(self, title, heading, message, current_action, can_cancel, parent=None):
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        gtk.Dialog.__init__(self, title, parent, flags)
        
        self.connect("destroy", self._cb_destroy)
        self.connect("response", self._cb_response)
        self.set_border_width(6)
        self.set_has_separator(False)
        
        vbox = self.vbox
        vbox.set_spacing(6)
        
        if heading:
            label = gtk.Label()
            label.set_markup("<b>%s</b>" % heading)
            label.set_line_wrap(True)
            label.set_alignment(0, 0.5)
            vbox.pack_start(label, False, False)
            
        label = gtk.Label(message)
        label.set_line_wrap(True)
        label.set_alignment(0, 0.5)
        vbox.pack_start(label, False, False)
        
        self._progress = gtk.ProgressBar()
        vbox.pack_start(self._progress, False, False)
        
        self._label_action = gtk.Label(current_action)
        self._label_action.set_line_wrap(True)
        self._label_action.set_alignment(0, 0.5)
        vbox.pack_start(self._label_action, False, False)
        
        if can_cancel:
            self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            
        vbox.show_all()
        
    def _cb_destroy(self, widget):
        self._working = False
        
    def _cb_response(self, widget, response):
        if response == gtk.RESPONSE_CANCEL:
            self.emit("cancelled")
        
    def set_current_action(self, action):
        self._label_action.set_label(action)
        
    def set_progress(self, value):
        if value > 1.0:
            value = 1.0
        self._progress.set_fraction(value)
        if value >= 1.0:
            self.response(gtk.RESPONSE_OK)
            
    def get_progress(self):
        return self._progress.get_fraction()
        
    def run(self):
        res = gtk.Dialog.run(self)
        self.destroy()
        return res
    
    
if __name__ == "__main__":
    import random
    lorem = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."
    
    def cb_show_yes_no(widget):
        res = dialog_yes_no("Test", "This is a test.", lorem)
        print res
    
    def cb_show_yes_no_error(widget):
        res = dialog_yes_no_error("Test", "This is a test.", lorem)
        print res
    
    def cb_show_yes_no_question(widget):
        res = dialog_yes_no_question("Test", "This is a test.", lorem)
        print res
    
    def cb_show_yes_no_warning(widget):
        res = dialog_yes_no_warning("Test", "This is a test.", lorem)
        print res
    
    def cb_show_ok_cancel(widget):
        res = dialog_ok_cancel("Test", "This is a test.", lorem)
        print res
    
    def cb_show_ok_cancel_error(widget):
        res = dialog_ok_cancel_error("Test", "This is a test.", lorem)
        print res
    
    def cb_show_ok_cancel_warning(widget):
        res = dialog_ok_cancel_warning("Test", "This is a test.", lorem)
        print res
    
    def cb_show_ok_info(widget):
        res = dialog_ok_info("Test", "This is a test.", lorem)
        print res
        
    def select_action(d):
        actions = ["doin cool things", "waiting", "idle", "doing nothing"]
        action = random.choice(actions)
        d.set_current_action(action)
        return True
        
    def cb_show_working(widget, cancel):
        d = WorkingDialog("Test", "Doing something", "Something really cool is done at this moment. This could take a long long time...", "doin' cool things", cancel)
        gobject.timeout_add(2000, select_action, d)
        res = d.run()
        print res
        
    def increase_progress(d):
        actions = ["doin cool things", "waiting", "idle", "doing nothing"]
        action = random.choice(actions)
        d.set_current_action(action)
        if d.get_progress() == 1.0:
            return False
        d.set_progress(d.get_progress() + 0.05)
        return True
    
    def cb_show_progress(widget, cancel):
        d = ProgressDialog("Test", "Doing something", "Something really cool is done at this moment. This could take a long long time...", "doin' cool things", cancel)
        gobject.timeout_add(1000, increase_progress, d)
        res = d.run()
        print res
    
    
    w = gtk.Window()
    w.connect("destroy", gtk.main_quit)
    w.set_title("Dialogs")
    vbox = gtk.VBox()
    vbox.set_spacing(6)
    vbox.set_border_width(12)
    w.add(vbox)
    
    label = gtk.Label("This is a list of the available dialogs:")
    label.set_alignment(0, 0.5)
    vbox.pack_start(label, False, False)
    
    button_yn = gtk.Button("Yes/No dialog")
    button_yn.connect("clicked", cb_show_yes_no)
    vbox.pack_start(button_yn)
    
    button_yne = gtk.Button("Yes/No dialog (error)")
    button_yne.connect("clicked", cb_show_yes_no_error)
    vbox.pack_start(button_yne)
    
    button_ynq = gtk.Button("Yes/No dialog (question)")
    button_ynq.connect("clicked", cb_show_yes_no_question)
    vbox.pack_start(button_ynq)
    
    button_ynw = gtk.Button("Yes/No dialog (warning)")
    button_ynw.connect("clicked", cb_show_yes_no_warning)
    vbox.pack_start(button_ynw)
    
    vbox.pack_start(gtk.HSeparator(), False, False)
    
    button_oc = gtk.Button("Ok/Cancel dialog")
    button_oc.connect("clicked", cb_show_ok_cancel)
    vbox.pack_start(button_oc)
    
    button_oce = gtk.Button("Ok/Cancel dialog (error)")
    button_oce.connect("clicked", cb_show_ok_cancel_error)
    vbox.pack_start(button_oce)
    
    button_ocw = gtk.Button("Ok/Cancel dialog (warning)")
    button_ocw.connect("clicked", cb_show_ok_cancel_warning)
    vbox.pack_start(button_ocw)
    
    vbox.pack_start(gtk.HSeparator(), False, False)
    
    button_oi = gtk.Button("Info dialog")
    button_oi.connect("clicked", cb_show_ok_info)
    vbox.pack_start(button_oi)
    
    vbox.pack_start(gtk.HSeparator(), False, False)
    
    button_work = gtk.Button("Working dialog")
    button_work.connect("clicked", cb_show_working, False)
    vbox.pack_start(button_work)
    
    button_workc = gtk.Button("Working dialog (with cancel button)")
    button_workc.connect("clicked", cb_show_working, True)
    vbox.pack_start(button_workc)
    
    button_progress = gtk.Button("Progress dialog")
    button_progress.connect("clicked", cb_show_progress, False)
    vbox.pack_start(button_progress)
    
    button_progressc = gtk.Button("Progress dialog (with cancel button)")
    button_progressc.connect("clicked", cb_show_progress, True)
    vbox.pack_start(button_progressc)
    
    w.show_all()
    gtk.main()
