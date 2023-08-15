import os
import os.path as path
import sys
import inspect
import base64 
import re

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QAction, QIcon, Qt, QTextCharFormat, QColor,QKeyEvent, QImage, QPixmap 
from PySide6.QtWidgets import QSizePolicy, QApplication
from PySide6.QtWidgets import QListWidgetItem, QAbstractItemView, QComboBox

from ..icons import *

def start():
    app = QApplication(sys.argv)
    return app


def call(func: None = None, *args, **kwargs):
    if func != None:
        return lambda function: func(*args, **kwargs)

DEFAULT_WINDOW_TITLE = None
DEFAULT_WINDOW_ICON = icon_data['hand-drawn-icon']
DEFAULT_WINDOW_SIZE = (None, None)
DEFAULT_WINDOW_FIXED_SIZE = (None, None)
DEFAULT_WINDOW_STYLE = None
DEFAULT_WINDOW_GEOMETRY = None
DEFAULT_TAB_DISTANCE = 30


WIDGET_ID_SAFE = {}
ID_COUNT_DEFAULT = [0]
TOOLBAR_COUNT = []
LINK_ITEMS_INCLUDED = []

SIZE_POLICY_EXPAND = expand = 'expand'
SIZE_POLICY_FIXED = fixed = 'fixed'

circle = 'circle'
square = 'square'

# GRAB_WIDGET = 'GrabWidget'

DEFAULT_SEPARATOR_MARKER = '---'

ELEM_TYPE_ITEM = 'item'
ELEM_TYPE_SEPARATOR = 'separator'
ELEM_TYPE_COLUMN = 'column'
ELEM_TYPE_GROUP = 'group'
ELEM_TYPE_FIELDSET = 'fieldset'
ELEM_TYPE_EMPTY = 'empty'
ELEM_TYPE_BUTTON = 'button'
ELEM_TYPE_INPUT = 'input'
ELEM_TYPE_TEXT = 'text'
ELEM_TYPE_IMAGE = 'img'
ELEM_TYPE_CHECKBOX = 'checkbox'
ELEM_TYPE_RADIO_BUTTON = 'radio_button'
ELEM_TYPE_TEXTAREA = 'textarea'
ELEM_TYPE_LIST_WIDGET = 'list_widget'
ELEM_TYPE_LIST_ITEM = 'list_item'
ELEM_TYPE_SELECT = 'select'
ELEM_TYPE_OPTION = 'option'
ELEM_TYPE_PROGRESS_BAR = 'progress_bar'
ELEM_TYPE_SLIDER = 'slider'
ELEM_TYPE_DIAL = 'dial'
ELEM_TYPE_POPUP = 'popup'
ELEM_TYPE_TAB = 'tab'
ELEM_TYPE_TAB_WIDGET = 'tab_widget'
ELEM_TYPE_SCROLL_AREA = 'scrollarea'
ELEM_TYPE_STACKED = 'stack'
ELEM_TYPE_TABLE = 'table'


DEFAULT_VERTICAL_TYPES = ['vertical', 'v']
DEFAULT_HORIZONTAL_TYPES = ['horizontal', 'h']

vertical =DEFAULT_VERTICAL_TYPES[0]
horizontal = DEFAULT_HORIZONTAL_TYPES[0]

SET_HORIZONTAL = 'HORIZONTAL'
SET_VERTICAL = 'VERTICAL'

SET_NORMAL = normal = 'NORMAL'
SET_STATIC = static ='STATIC'

INPUT_TYPE_STANDARD = standard = 'STANDARD'
INPUT_TYPE_PASSWORD = password = 'PASSWORD'
INPUT_TYPE_NO_ECHO = noecho = 'NO_ECHO'


GET_ELEM_TYPE_TEXTAREA = 'QTextEdit'
GET_ELEM_TYPE_LISTWIDGET = 'QListWidget'
GET_ELEM_TYPE_SELECT = 'QComboBox'
GET_ELEM_TYPE_PROGRESS_BAR = 'QProgressBar'
GET_ELEM_TYPE_SLIDER = 'QSlider'
GET_ELEM_TYPE_DIAL = 'QDial'
GET_ELEM_TYPE_TAB_WIDGET = 'QTabWidget'
GET_ELEM_TYPE_POPUP = 'QDialog'
GET_ELEM_TYPE_INPUT = 'QLineEdit'
GET_ELEM_TYPE_STACKED = 'QStackedWidget'
GET_ELEM_TYPE_COLOR_POPUP = 'QColorDialog'
# GET_ELEM_TYPE_SCROLLAREA = 'QScrollArea'

ITEM_SELECTION_MODE_EXTENDED = extended = 'extended'
ITEM_SELECTION_MODE_NO_SELECTION = noselection= 'no_selection'
ITEM_SELECTION_MODE_MULTI = multi = 'multi'
ITEM_SELECTION_MODE_SINGLE = single = 'single'


PRE_INIT_COPY = 'copy'
PRE_INIT_CUT = 'cut'
PRE_INIT_PASTE = 'paste'
PRE_INIT_UNDO = 'undo'
PRE_INIT_REDO = 'redo'


center = 'center'
right = 'right'
left = 'left'
top = 'top'
bottom = 'bottom'
hcenter = 'hcenter'
vcenter = 'vcenter'
justify = 'justify'


CUSTOM_TITLEBAR_HEIGHT = 5

CONTROL_BUTTON_CIRCLE = '10px'
CONTROL_BUTTON_SQUARE = '0'

DEFAULT_BUTTON_STYLE = 'circle'

OPEN_FILE_TYPE_SINGLE = 'single'
OPEN_FILE_TYPE_MULTI = 'multi'

DEFAULT_OPEN_FILE_TYPE = OPEN_FILE_TYPE_SINGLE

FILTER_SPLIT_MARKER = '&'

CONTROL_CLOSE = '⨯'

SYSTEM_PLATFORM_WINDOWS = windows = 'windows'
SYSTEM_PLATFORM_FUSION = fusion = 'fusion'
SYSTEM_PLATFORM_CURVE = curve = 'qtcurve'
SYSTEM_PLATFORM_OXYGEN = oxygen = 'oxygen'
SYSTEM_PLATFORM_BREEZE = breeze = 'breeze'

ICON_IMAGE_ID = '-clera_icon-'
TITLE_TEXT_ID = '-clera_title-'
MINIMIZE_BUTTON_ID = '-clera_minimize_button-'
MAXIMIZE_BUTTON_ID = '-clera_maximize_button-'
CLOSE_BUTTON_ID = '-clera_close_button-'

GRID_IDENTIFIER = '=grid'
BOX_IDENTIFIER = '=box'
# TAB_IDENTIFIER = 'tab('
SCROLL_AREA_IDENTIFIER = '=scrollarea'
# STACK_IDENTIFIER = '=stack'

SYSTEM_OS_PLATFORM = sys.platform.lower()


def FUSION_CONTROLS():
    global CONTROL_MINIMIZED, CONTROL_RESTORE, CONTROL_MAXIMIZED

    CONTROL_MINIMIZED = '-'
    CONTROL_RESTORE = '+'
    CONTROL_MAXIMIZED = '+'

    return CONTROL_MINIMIZED, CONTROL_RESTORE, CONTROL_MAXIMIZED


def WINDOWS_CONTROLS():
    global CONTROL_MINIMIZED, CONTROL_RESTORE, CONTROL_MAXIMIZED

    CONTROL_MINIMIZED = '–'
    CONTROL_RESTORE = '❒'
    CONTROL_MAXIMIZED = '◻'

    return CONTROL_MINIMIZED, CONTROL_RESTORE, CONTROL_MAXIMIZED


def CLERA_CONTROLS():
    global CONTROL_MINIMIZED, CONTROL_RESTORE, CONTROL_MAXIMIZED

    CONTROL_MINIMIZED = '-'
    CONTROL_RESTORE = '+'
    CONTROL_MAXIMIZED = '+'

    return CONTROL_MINIMIZED, CONTROL_RESTORE, CONTROL_MAXIMIZED


def INIT_WIDGET(ID, widget):
    if ID == None or ID == '':
        ID = ID_COUNT_DEFAULT[0]
        ID_COUNT_DEFAULT[0] += 1

    WIDGET_ID_SAFE[ID] = widget
    return WIDGET_ID_SAFE[ID]


def INIT_ITEM(self, item):
    item_type, label, func, icon, tooltip, statustip, shortcut = item

    if icon != None:
        icon = init_image(icon)

    Action = QAction(QIcon(icon), label, self)
    Action.triggered.connect(func)

    Action.setStatusTip(statustip)
    Action.setToolTip(tooltip)
    if shortcut != None:
        Action.setShortcut(shortcut)

    return Action


def init_image(data):
    format = type(data)

    if format == bytes:
        image = QImage()
        byte_array = QByteArray.fromBase64(data)
        image.loadFromData(byte_array, 'PNG')
        return QPixmap.fromImage(image)
    elif format == str:
        return QPixmap(get_path(data))
    
def set_size_policy(widget, sizepolicy):
    policy = {
        'fixed'     : QSizePolicy.Fixed,
        'expand'    : QSizePolicy.Expanding
    }

    def init_single_policy(sizepolicy):
        if sizepolicy == SIZE_POLICY_EXPAND or sizepolicy == SIZE_POLICY_FIXED:
            return (policy[sizepolicy], policy[sizepolicy])

    if type(sizepolicy) == sample_tuple:
        if len(sizepolicy) == 2:
            horizontal_policy, vertical_policy = sizepolicy

            if horizontal_policy != None and vertical_policy != None:
                horizontal = horizontal_policy.lower()
                vertical = vertical_policy.lower()

                try:
                    vertical = policy[vertical]
                    horizontal = policy[horizontal]
                except:
                    raise ValueError(sizepolicy)
        elif len(sizepolicy) == 1:
            horizontal, vertical = init_single_policy(sizepolicy)
        else:
            ...
            # raise an error
    elif type(sizepolicy) == sample_string:
        horizontal, vertical = init_single_policy(sizepolicy)
    
    try:
        widget.setSizePolicy(horizontal, vertical)
    except:
        ...
        # raise an error

def set_widget(lyt, grid, widget, grid_pos_x, grid_pos_y):
    gridy, gridx = grid  # vertical (y) and horizontal (x) occupy rule for grid widgets

    if type(lyt) != sample_list and type(lyt) != sample_string:
        if grid_pos_x != None and grid_pos_y != None:
            if gridx != None and gridy != None:
                lyt.addWidget(widget, grid_pos_x, grid_pos_y, gridy, gridx)
            else:
                lyt.addWidget(widget, grid_pos_x, grid_pos_y)
        else:
            lyt.addWidget(widget)
    else:
        if len(lyt) == 2:
            lyt, _type = lyt

            if _type == 'addWidget':
                lyt.addWidget(widget)
            elif _type == 'addPermanentWidget':
                lyt.addPermanentWidget(widget)
            else:
                ...
        elif len(lyt) == 3:
            layout, pre_widget, _type = lyt
            if _type == 'replaceWidget':
                layout.replaceWidget(pre_widget, widget)


def make_alignment(widget, alignments):
    def alignCheck(widget_alignment):
        alignment = widget_alignment.lower()

        alignment_map = {
            center      : Qt.AlignCenter,
            right       : Qt.AlignRight,
            left        : Qt.AlignLeft,
            top         : Qt.AlignTop,
            bottom      : Qt.AlignBottom,
            hcenter     : Qt.AlignHCenter,
            vcenter     : Qt.AlignVCenter,
            justify     : Qt.AlignJustify
        }
        
        try:
            align = alignment_map[alignment]
        except:
            ...
            # raise an error

        return align

    align = alignCheck(alignments)
    widget.setAlignment(align)


def get_parent(identifier):
    inspector = inspect.stack()[2][4]
    result = str(inspector).lower().replace(' ', '')

    if (identifier not in result and f"{ELEM_TYPE_TAB}({identifier.removeprefix('=')}" not in result and 
        ELEM_TYPE_SCROLL_AREA not in result and ELEM_TYPE_STACKED not in result):
        return True
    else:
        return False

def get_filter(value):
    # split_markers = ['), (', ') ,(', ') , (', '),(']
    # for split_marker in split_markers:
    #     if split_marker in value:
    #         value = value.replace(split_marker, FILTER_SPLIT_MARKER)
    # "(Python: *.py) , (Bash: *.sh, *.cmd)"
    # value = value.replace('(', '').replace(')', '')
    
    value = value.split(')')
    value = [item.split('(') for item in value]

    result = [
        item 
            for items in range(len(value)) 
                for item in value[items] 
                    if len(item) != 0 and item.strip() != ','
            ]
    value = FILTER_SPLIT_MARKER.join(result)
    
    def init_filter(filter):
        filter = filter.split(':')
        filter_type = filter[0].strip()
        extensions = filter[1]
        extensions = extensions.split(',')
        filter_extensions = ''
        for extension in extensions:
            filter_extensions += extension.strip() + ' '
        else:
            filter_extensions = filter_extensions[:-1]

        return f'{filter_type} ({filter_extensions})'

    if FILTER_SPLIT_MARKER in value:
        filters = value.split(FILTER_SPLIT_MARKER)
        file_filter = ''
        for filter in filters:
            filter = init_filter(filter)
            file_filter += filter + ' ;; '
        else:
            file_filter = file_filter[:-4]
    else:
        file_filter = init_filter(value)

    return file_filter


def check_func(property):
    # IMPROVE LATER
    if type(property) == type(list()):
        widget_type = property[0]
    elif type(property) == type(str()):
        widget_type = ''
    else:
        widget_type = property()[0]
        property = property()

    return widget_type, property


def process_request(allowed: list = None, widget_type: None = None):
    if type(allowed) == sample_list:
        for values in allowed:
            if values in widget_type:
                return True
        else:
            return False

    elif type(allowed) == sample_string:
        if allowed in widget_type:
            return True
        else:
            return False


def add_list_items(widget, list_items):

    for items in list_items:
        NotRequired, label, icon = items

        if icon != None:
            icon_path = init_image(icon)

        list_widget_item = QListWidgetItem(QIcon(icon_path), label)
        widget.addItem(list_widget_item)


def add_select_option(widget, options):
    for option in options:
        item_type = option[0].lower()

        if item_type == ELEM_TYPE_OPTION:
            option_value = str(option[1])
            option_icon = option[2]

            # print(type(option_value))

            if ELEM_TYPE_INPUT in str(type(option_value)).lower():
                widget.setLineEdit(option_value)
            else:
                widget.addItem(option_value)
                icon_index = widget.count()-1

                if option_icon != None:
                    widget.setItemIcon(
                        icon_index, QIcon(init_image(option_icon)))


def add_tabs(tab_widget, tabs):
    def init_tab(tab):
        elem_type, layout, name, icon = tab

        if elem_type == ELEM_TYPE_TAB:
            if icon != None:
                icon = QIcon(init_image(icon))
            else:
                icon = QIcon(icon)

            tab_widget.addTab(layout, icon, name)

    if type(tabs[0]) == sample_list:
        for tab in tabs:
            init_tab(tab)
    elif type(tabs[0]) == sample_string:
        init_tab(tabs)


def add_stacks(stack_widget, stacks):
    def init_stack(stack):
        widget, layout = stack
        stack_widget.addWidget(widget)
        
    if type(stacks[0]) == sample_list:
        for stack in stacks:
            init_stack(stack)
    else:
        init_stack(stacks)


def get_path(href):
    return path.abspath(href)


# PRE-DEFINED WIDGETS
PRE_DEFINED_WIDGETS = []
PRE_WIDGETS_COUNT = [0]

# All the Pre-Defined Widget Method List
METHOD_COPY = []
METHOD_CUT = []
METHOD_PASTE = []
METHOD_UNDO = []
METHOD_REDO = []


def PRE_INIT(MethodType, MethodItem):
    for item in MethodItem:
        try:
            item = item.split(':')
            pre_id = item[0]
            target_id = item[1]

            pre_widget = WIDGET_ID_SAFE[pre_id]
            target_widget = WIDGET_ID_SAFE[target_id]

            if pre_widget.isChecked():
                if MethodType == PRE_INIT_COPY:
                    pre_widget.clicked.connect(
                        target_widget.copy())
                elif MethodType == PRE_INIT_CUT:
                    pre_widget.clicked.connect(
                        target_widget.cut())
                elif MethodType == PRE_INIT_PASTE:
                    pre_widget.clicked.connect(
                        target_widget.paste())
                elif MethodType == PRE_INIT_UNDO:
                    pre_widget.clicked.connect(
                        target_widget.undo())
                elif MethodType == PRE_INIT_REDO:
                    pre_widget.clicked.connect(
                        target_widget.redo())
                pre_widget.toggle()
        except:
            if pre_widget.isChecked():
                pre_widget.toggle()


def action_copy():
    PRE_INIT(PRE_INIT_COPY, METHOD_COPY)


def action_cut():
    PRE_INIT(PRE_INIT_CUT, METHOD_CUT)


def action_paste():
    PRE_INIT(PRE_INIT_PASTE, METHOD_PASTE)


def action_undo():
    PRE_INIT(PRE_INIT_UNDO, METHOD_UNDO)


def action_redo():
    PRE_INIT(PRE_INIT_REDO, METHOD_REDO)


def pre_widget_process(widget_type):
    id = widget_type + str(PRE_WIDGETS_COUNT[0])
    PRE_WIDGETS_COUNT[0] += 1

    return ELEM_TYPE_BUTTON, id


def sample_func(): ...


sample_string = type(str())

sample_list = type(list())

sample_function = type(sample_func)

sample_integer = type(int())

sample_tuple = type(tuple())

if SYSTEM_OS_PLATFORM == 'linux':
    minimize_padding = ' padding: 1px 7px 2px 7px'
    maximize_padding = 'padding: 1px 6px 2px 6px'
    close_padding = 'padding: 1px 4px 2px 4px'
else:
    minimize_padding = 'padding: 1px 8px 3px 8px'
    maximize_padding = 'padding: 1px 6px 3px 6px'
    close_padding = 'padding: 1px 6px 3px 6px'


def fusion_style(minimize, maximize, close, control_button_style):
    minimize.style(f'''
        button [
            color: rgb(18, 18, 18);
            font-weight: bold;
            {minimize_padding};
            margin: 0 4px 0 5px;
            background: rgb(18, 18, 18);
            border-radius: {control_button_style};
            min-width: 0px;
            height: 17px;
        ]

        button:hover [
            color: white;
        ]
    ''')

    maximize.style(f'''
        button [
            color: rgb(18, 18, 18);
            font-weight: bold;
            {maximize_padding};
            margin-right: 4px;
            background: rgb(18, 18, 18);
            border-radius: {control_button_style};
            min-width: 0px;
            height: 17px;
        ]

        button:hover [
            color: white;
        ]
    ''')

    close.style(f'''
        button [
            color: rgb(18, 18, 18);
            margin-right: 8px;
            font-weight: bold;
            {close_padding};
            background: rgb(56, 109, 209);
            border-radius: {control_button_style};
            min-width: 0px;
            height: 17px;
        ]

        button:hover [
            color: white;
        ]
    ''')


def windows_style(minimize, maximize, close):
    minimize.style(f'''
        button [
            font-weight: bold;
            padding: 5.5px 17px 6.5px 17px;
            background: rgba(65, 63, 63, 0);
            border: 0px solid;
            min-width: 0px;
            color: white;
        ]

        button:hover [
            color: white;
            background: grey;
        ]
    ''')

    maximize.style(f'''
        button [
            font-weight: bold;
            padding: 5.5px 15px 6.5px 15px;
            background: rgba(65, 63, 63, 0);
            border: 0px solid;
            color: white;
            min-width: 0px;

        ]

        button:hover [
            color: white;
            background: grey;
        ]
    ''')

    close.style(f'''
        button [
            font-weight: bold;
            padding: 5.5px 15px;
            background: rgba(65, 63, 63, 0);
            border: 0px solid;
            color: white;
            min-width: 0px;
        ]

        button:hover [
            color: white;
            background: red;
        ]
    ''')


# def clera_style(minimize, maximize, close):
#     minimize.style(f'''
#         button [
#             color: rgb(206, 159, 5);
#             font-weight: bold;
#             margin-left: 4px;
#             padding: 0 7px 2px 7px;
#             background: rgb(206, 159, 5);
#             border-radius: {CONTROL_BUTTON_CIRCLE};
#         ]

#         button:hover [
#             color: rgb(122, 94, 0);
#         ]
#     ''')

#     maximize.style(f'''
#         button [
#             color: rgb(2, 141, 2);
#             font-weight: bold;
#             margin: 0 5px 0 4px;
#             padding: 1px 6px 1px 6px;
#             background: rgb(2, 141, 2);
#             border-radius: {CONTROL_BUTTON_CIRCLE};
#         ]

#         button:hover [
#             color: rgb(0, 41, 0);
#         ]
#     ''')

#     close.style(f'''
#         button [
#             color: rgb(172, 3, 3);
#             margin-left: 8px;
#             padding: 0 4px 1px 4px;
#             font-weight: bold;
#             background: rgb(172, 3, 3);
#             border-radius: {CONTROL_BUTTON_CIRCLE};
#         ]

#         button:hover [
#             color: rgb(61, 0, 0);
#         ]
#     ''')


def append_items(append_list, item):
    append_list.append(item)

COLORS = {
    'red'       : Qt.red,
    'black'     : Qt.black,
    'white'     : Qt.white,
    'gray'      : Qt.gray,
    'green'     : Qt.green,
    'blue'      : Qt.blue,
    'cyan'      : Qt.cyan,
    'magenta'   : Qt.magenta,
    'yellow'    : Qt.yellow,
}

def get_color(value):
    if 'rgb' in value:
        rgb = [0, 0, 0]
        new_color = value.lower()
        new_color = value.replace('(', '').replace(')', '')
        new_color = new_color.replace('rgba', 'rgb')
        color = new_color.removeprefix('rgb') 
        color = color.split(',')

        for _index in range(len(color)):
            if _index <= 2:
                rgb[_index] = int(color[_index])
        else:
            rgb = rgb[0:3]
            red, green, blue = rgb
            color = QColor(red, green, blue)
    else:
        try:
            color = COLORS[value]
        except:
            color = None

    return color


def INIT_FORMAT(elements):
    format = QTextCharFormat()
    KEYS = elements.keys()
    if 'color' in KEYS:
        color = get_color(elements['color'])
        if color != None:
            format.setForeground(color)

    if 'background' in KEYS:
        background = get_color(elements['background'])
        if background != None:
            format.setBackground(background)
            
    return format

def r(list: list = None):
    if list != None:
        return '|'.join([fr'\b{list[i]}\b' for i in range(len(list))])

def encode(path):
    path = str(path)
    
    if os.path.isfile(path):
        with open(path, 'rb') as image:
            BASE_64 = base64.b64encode(image.read())

        return BASE_64

def decode(byte, path: str = 'image.png', write: bool = False):
    BASE_64 = base64.b64decode(byte)
    
    if write == True:
        with open(path, 'wb') as image:
                image.write(BASE_64)

    return BASE_64