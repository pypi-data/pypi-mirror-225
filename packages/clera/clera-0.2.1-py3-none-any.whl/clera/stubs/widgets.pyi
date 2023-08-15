from .handlers import *

def Column(widgets) -> list: ...

def column(widgets) -> Column: ...

def item(label: any, func: function, icon: str, tooltip: any | str, 
         statustip: any | str, shortcut: str) -> list: ...

def tab(layout, name: str, icon: str) -> list: ...
def option(value: any, icon: str) -> list: ...
def ListItem(label: any, icon: str) -> list: ...
def separator() -> list: ...
def empty() -> list: ...
def fieldset(label: any | str, widgets: list, id: str, orientation: str) -> list: ...
def Group(widgets: list, orientation: str) -> list: ...
def group(widgets: list, orientation: str) -> list: ...

class Button:
    def __init__(self, value: any, func: function, icon: str, id: any, disabled: bool, 
                 default: bool, grid: tuple, sizepolicy: tuple, checkable: bool,
                 checked: bool, hidden: bool, focus: bool, icon_size: int, 
                 statustip: any | str, tooltip: any | str, shortcut: str):
        '''
       
        '''
        ...

class button(Button): ...

class Input:
    def __init__(self, placeholder: any, id: any, value: any,
                 type: str, disabled: bool, readonly: bool,
                 maxlength: int, hidden: bool, font: str,
                 fontsize: int, text_changed: function, return_pressed: function,
                 editing_finished: function, text_edited: function,
                 selection_changed: function, sizepolicy: tuple, grid: tuple):
        '''
        
        '''
        ...

class input(Input): ...

class Text:
    def __init__(self, value: any, id: any, link: str,
                 hovered: function, clicked: function, buddy: str, alignment: str,
                 wordwrap: bool, grid: tuple,
                 sizepolicy: tuple, hidden: bool):
        '''
        
        '''

        ...
        
class text(Text): ...

class Image:
    def __init__(self, source: str, id: any, size: int, alignment: str, grid: tuple,
                 sizepolicy: tuple, hidden: bool):
        '''
        
        '''

        ...

class image(Image): ...

class CheckBox:
    def __init__(self, label: any, checked: bool, id: any,
                 state_changed: function, toggled: function, grid: tuple,
                 sizepolicy: tuple):
        '''
        
        '''
        ...

class checkbox(CheckBox): ...

class RadioButton:
    def __init__(self, label: any, checked: bool, id: any,
                 toggled: function, grid: tuple,
                 sizepolicy: tuple):
        '''
        
        '''
        ...

class radiobutton(RadioButton): ...

class Textarea:
    def __init__(self, id: any, placeholder: any,
                 hidden: bool, alignment: str, value: any,
                 disabled: bool, readonly: bool, text_changed: function,
                 selection_changed: function, undo_available: function,
                 redo_available: function, maxlength: int, font: str,
                 fontsize: int, sizepolicy: tuple,
                 grid: tuple, tabwidth: int,
                 wordwrap: bool):
        '''
        
        '''
        ...
class textarea(Textarea): ...

class ListWidget:
    def __init__(self, list_items: any, id: any, mode: str, grid: tuple,
                 sizepolicy: tuple, func: function):
        '''
        
        '''
        ...

class listwidget(ListWidget): ...

class Select:
    def __init__(self, options: list, id: any, placeholder: any, grid: tuple,
                 sizepolicy: tuple, current_text_changed: function, activated: function):
        '''
        
        '''

        ...

class select(Select): ...

class ProgressBar:
    def __init__(self, id: any,  min: int, max: int, value: int, orientation: str, 
                 grid: tuple, sizepolicy: tuple, text_visible: bool, inverted: bool,
                 value_changed: function):
        '''
       
        '''
        ...

class progressbar(ProgressBar): ...

class Slider:
    def __init__(self, id: any, min: int, max: int, value: int,
                 step: int, orientation: str, grid: tuple,
                 sizepolicy: tuple, value_changed: function):
        '''
        
        '''
        ...

class slider(Slider): ...

class Dial:
    def __init__(self, id: any, min: int, max: int, value: int,
                 tick_target: str, tick: bool, wrapping: bool, grid: tuple,
                 sizepolicy: tuple, value_changed: function):
        '''
        
        '''
        ...

class dial(Dial): ...