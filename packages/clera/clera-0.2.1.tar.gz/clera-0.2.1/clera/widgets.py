from .utils import *


from PySide6.QtGui import QIcon, QFont, QPixmap, QTextCursor
from PySide6.QtWidgets import QPushButton, QLabel, QLineEdit, QRadioButton, QCheckBox, QTextEdit, QListWidget
from PySide6.QtWidgets import QComboBox, QProgressBar, QSlider, QDial, QWidget, QScrollArea
from PySide6.QtWidgets import QColorDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import QSize


def Column(widgets):
    type = ELEM_TYPE_COLUMN
    return [type, widgets]


def column(*args, **kwargs):
    return Column(*args, **kwargs)


def item(label: any = '', func: None = None, icon: None = None,
         tooltip: None = None, statustip: None = None, shortcut: None = None):
    type = ELEM_TYPE_ITEM
    return [type, label, func, icon, tooltip, statustip, shortcut]


def tab(layout: None = None, name: None = None, icon: None = None):
    type = ELEM_TYPE_TAB
    NotRequired, layout = check_func(layout)
    return [type, layout[0], name, icon]


def option(value: any = '', icon: None = None):
    type = ELEM_TYPE_OPTION
    return [type, value, icon]


def ListItem(label: any = '', icon: None = None):
    type = ELEM_TYPE_LIST_ITEM
    return [type, label, icon]


def separator():
    type = ELEM_TYPE_SEPARATOR
    return [type]


def empty():
    type = ELEM_TYPE_EMPTY
    return [type]


def fieldset(label: str = '', widgets: list = None, id: None = None, orientation: str = SET_VERTICAL):
    elem_type = ELEM_TYPE_FIELDSET
    return [elem_type, label, widgets, id, orientation]


def Group(widgets: list = None, orientation: str = SET_VERTICAL):
    elem_type = ELEM_TYPE_GROUP
    return [elem_type, widgets, orientation]


def group(*args, **kwargs):
    return Group(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
#################################  BUTTON  ################################
###########################################################################

# ---------------ToolBarArea---------------------------------------------------------#


def window_button(lyt, button_text, func, icon,
                  ID, disabled, default, sizepolicy, grid, grid_pos_x, grid_pos_y, checkable,
                  checked, hidden, focus, icon_size, statustip, tooltip, shortcut):

    button = INIT_WIDGET(ID, QPushButton(button_text))
    set_widget(lyt, grid, button, grid_pos_x, grid_pos_y)
    set_size_policy(button, sizepolicy)

    button.setStatusTip(statustip)
    button.setToolTip(tooltip)
    if shortcut != None:
        button.setShortcut(shortcut)
    
    button.setIcon(QIcon(init_image(icon)))
    button.setIconSize(QSize(icon_size, icon_size))
    button.setDisabled(disabled)
    button.setDefault(default)
    button.setCheckable(checkable)
    button.setChecked(checked)
    button.clicked.connect(func)
    button.setHidden(hidden)

    # button.setFocus(Qt.NoFocusReason)
    if focus == False:
        button.setFocusPolicy(Qt.NoFocus)

    return button


class Button:
    def __init__(self, value: any = '', func: None = None, icon: str = None, id: any = None,
                 disabled: bool = False, default: bool = False, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), checkable: bool = False,
                 checked: bool = False, hidden: bool = False, focus: bool = True, 
                 icon_size: int = 20, statustip: str = None, tooltip: str = None, shortcut: str = None):
        '''
        Button Widget

        :param value:
        :param func:
        :param icon:
        :param id:
        :param disabled:
        :param default:
        :param grid:
        :param sizepolicy:
        :param checkable:
        :param checked:
        :param hidden:
        :param focus:
        :param icon_size:
        :param statustip:
        :param tooltip:
        :param shortcut:
        '''

        elem_type = ELEM_TYPE_BUTTON
        self.rtn = [elem_type, str(value), func, icon, id,
                    disabled, default, grid, sizepolicy, checkable, checked, hidden, focus, icon_size, statustip, tooltip, shortcut]

    def __call__(self):
        return self.rtn


class button(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
#################################  INPUT  #################################
###########################################################################

# ------------------------------------------------------------------------#


def window_input(lyt, placeholder, ID, value, type, disabled,
                 readonly, maxlength, hidden, font, fontsize, text_changed, return_pressed,
                 editing_finished, text_edited, selection_changed, sizepolicy, grid,
                 grid_pos_x, grid_pos_y,):

    input = INIT_WIDGET(ID, QLineEdit())

    set_widget(lyt, grid, input, grid_pos_x, grid_pos_y)
    set_size_policy(input, sizepolicy)

    if fontsize != None:
        input.setFont(QFont(font, fontsize))
    else:
        input.setFont(QFont(font))

    if maxlength != None:
        input.setMaxLength(maxlength)

    input.setHidden(hidden)
    input.setDisabled(disabled)
    input.setReadOnly(readonly)
    input.setText(value)
    input.setPlaceholderText(placeholder)
    input.textChanged.connect(text_changed)
    input.returnPressed.connect(return_pressed)
    input.editingFinished.connect(editing_finished)
    input.textEdited.connect(text_edited)
    input.selectionChanged.connect(selection_changed)

    input_type = type.upper()

    if input_type == INPUT_TYPE_PASSWORD:
        input.setEchoMode(QLineEdit.Password)
    elif input_type == INPUT_TYPE_STANDARD:
        input.setEchoMode(QLineEdit.Normal)
    elif input_type == INPUT_TYPE_NO_ECHO:
        input.setEchoMode(QLineEdit.NoEcho)
    else:
        raise ValueError(type)

    return input


class Input:
    def __init__(self, placeholder: any = None, id: any = None, value: any = None,
                 type: str = INPUT_TYPE_STANDARD, disabled: bool = False, readonly: bool = False,
                 maxlength: int | None = None, hidden: bool = False, font: str | None = None,
                 fontsize: int | None = None, text_changed: None = None, return_pressed: None = None,
                 editing_finished: None = None, text_edited: None = None,
                 selection_changed: None = None, sizepolicy: tuple = (None, None), grid: tuple = (None, None)):
        '''
        Input Widget

        :param placeholder:
        :param id:
        :param value:
        :param type:
        :param diabled:
        :param readonly:
        :param maxlength:
        :param hidden:
        :param font:
        :param fontsize:
        :param text_changed:
        :param return_pressed:
        :param editing_finished:
        :param text_edited:
        :param selection_changed:
        :param sizepolicy:
        :param grid:
        '''

        elem_type = ELEM_TYPE_INPUT
        self.rtn = [elem_type, placeholder, id, value, type, disabled,
                    readonly, maxlength, hidden, font, fontsize, text_changed, return_pressed,
                    editing_finished, text_edited, selection_changed, sizepolicy, grid]

    def __call__(self):
        return self.rtn


class input(Input):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
##################################  TEXT  #################################
###########################################################################

# ------------------------------------------------------------------------#


def window_text(lyt, text, ID, link, hovered, clicked, buddy, alignment, word_wrap,
                sizepolicy, grid, grid_pos_x, grid_pos_y, hidden):

    label = INIT_WIDGET(ID, QLabel(text))

    set_widget(lyt, grid, label, grid_pos_x, grid_pos_y)
    set_size_policy(label, sizepolicy)

    if link != None:
        anchor = f'<a href="{link}">{text}</a>'
        label.setText(anchor)
        label.linkActivated.connect(clicked)
        label.linkHovered.connect(hovered)

    if buddy != None:
        label.setBuddy(WIDGET_ID_SAFE[buddy])

    if alignment != None:
        make_alignment(label, alignment)

    label.setWordWrap(word_wrap)
    label.setHidden(hidden)

    return label


class Text:
    def __init__(self, value: any = '', id: any = None, link: str = None,
                 hovered: None = None, clicked: None = None, buddy: str = None, alignment: str = None,
                 wordwrap: bool = False, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), hidden: bool = False):
        '''
        Text Widget

        :param value:
        :param id:
        :param link:
        :param hovered:
        :param clicked:
        :param buddy:
        :param alignment:
        :param wordwrap:
        :param grid:
        :param sizepolicy:
        :param hidden:
        '''

        elem_type = ELEM_TYPE_TEXT
        self.rtn = [elem_type, str(value), id, link,
                    hovered, clicked, buddy, alignment, wordwrap, grid, sizepolicy, hidden]

    def __call__(self):
        return self.rtn


class text(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
#################################  IMAGE  #################################
###########################################################################

# ------------------------------------------------------------------------#


def window_image(lyt, image, ID, size, alignment, hidden, sizepolicy, grid, grid_pos_x, grid_pos_y,):

    img = INIT_WIDGET(ID, QLabel())

    set_widget(lyt, grid, img, grid_pos_x, grid_pos_y)
    set_size_policy(img, sizepolicy)

    if image != None:
        pixmap = init_image(image)

        if type(size) == sample_integer:
            pixmap = pixmap.scaledToWidth(size)
        elif type(size) == sample_tuple:
            if len(size) == 2:
                height, width = size
                pixmap = pixmap.scaled(QSize(height, width))

        img.setPixmap(pixmap)

        if alignment != None:
            make_alignment(img, alignment)

        img.setHidden(hidden)

    return img


class Image:
    def __init__(self, source: str = None, id: any = None, size: int = None, alignment: str = None, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), hidden: bool = False):
        '''
        Image Widget

        :param source:
        :param id:
        :param size:
        :param alignment:
        :param grid:
        :param sizePolicy:
        :param hidden:
        '''

        elem_type = ELEM_TYPE_IMAGE
        self.rtn = [elem_type, source, id, size,
                    alignment, grid, sizepolicy, hidden]

    def __call__(self):
        return self.rtn


class image(Image):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
################################  CHECKBOX  ###############################
###########################################################################

# ------------------------------------------------------------------------#


def window_checkbox(lyt, name, checked, ID, state_changed, toggled, sizepolicy,
                    grid, grid_pos_x, grid_pos_y,):

    checkbox = INIT_WIDGET(ID, QCheckBox(name))

    set_widget(lyt, grid, checkbox, grid_pos_x, grid_pos_y)
    set_size_policy(checkbox, sizepolicy)

    checkbox.setChecked(checked)
    checkbox.stateChanged.connect(state_changed)
    checkbox.toggled.connect(toggled)

    return checkbox


class CheckBox:
    def __init__(self, label: any = '', checked: bool = False, id: any = None,
                 state_changed: None = None, toggled: None = None, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None)):
        '''
        Checkbox Widget

        :param label:
        :param checked:
        :param id:
        :param state_changed:
        :param toggled:
        :param grid:
        :param sizepolicy:
        '''

        elem_type = ELEM_TYPE_CHECKBOX
        self.rtn = [elem_type, label, checked, id,
                    state_changed, toggled, grid, sizepolicy]

    def __call__(self):
        return self.rtn


class checkbox(CheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
##############################  RADIOBUTTON  ##############################
###########################################################################

# ------------------------------------------------------------------------#


def window_radio_button(lyt, name, checked, ID, toggled, sizepolicy, grid,
                        grid_pos_x, grid_pos_y):

    radio_button = INIT_WIDGET(ID, QRadioButton(name))

    set_widget(lyt, grid, radio_button, grid_pos_x, grid_pos_y)
    set_size_policy(radio_button, sizepolicy)

    radio_button.setChecked(checked)
    radio_button.toggled.connect(toggled)

    return radio_button


class RadioButton:
    def __init__(self, label: any = '', checked: bool = False, id: any = None,
                 toggled: None = None, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None)):
        '''
        RadioButton Widget

        :param label:
        :param checked:
        :param id:
        :param stateChanged:
        :param toggled:
        :param grid:
        :param sizepolicy:
        '''

        elem_type = ELEM_TYPE_RADIO_BUTTON
        self.rtn = [elem_type, label, checked, id, toggled, grid, sizepolicy]

    def __call__(self):
        return self.rtn


class radiobutton(RadioButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
################################  TEXTAREA  ###############################
###########################################################################

# ------------------------------------------------------------------------#


def window_textarea(lyt, ID, placeholder, hidden, alignment, value, disabled, readonly, text_changed,
                    selection_changed, undo_available, redo_available, maxlength, font, fontsize,
                    sizepolicy, grid, grid_pos_x, grid_pos_y, tabwidth, wordwrap):

    textarea = INIT_WIDGET(ID, QTextEdit())

    set_widget(lyt, grid, textarea, grid_pos_x, grid_pos_y)
    set_size_policy(textarea, sizepolicy)
    
    #  set word wrap for textedit
    if not wordwrap:
        textarea.setLineWrapMode(textarea.LineWrapMode.NoWrap)

    textarea.setHidden(hidden)
    textarea.setDisabled(disabled)
    textarea.setReadOnly(readonly)
    textarea.setText(value)
    textarea.setPlaceholderText(placeholder)

    textarea.textChanged.connect(text_changed)
    textarea.selectionChanged.connect(selection_changed)
    textarea.undoAvailable.connect(undo_available)
    textarea.redoAvailable.connect(redo_available)

    textarea.setTabStopDistance(tabwidth)

    if fontsize != None:
        textarea.setFont(QFont(font, fontsize))
    else:
        textarea.setFont(QFont(font))

    if maxlength != None:
        textarea.setMaxLength(maxlength)

    if alignment != None:
        make_alignment(textarea, alignment)

    return textarea


class Textarea:
    def __init__(self, id: any = None, placeholder: any = None,
                 hidden: bool = False, alignment: str = None, value: any = None,
                 disabled: bool = False, readonly: bool = False, text_changed: None = None,
                 selection_changed: None = None, undo_available: None = None,
                 redo_available: None = None, maxlength: int | None = None, font: str | None = None,
                 fontsize: int | None = None, sizepolicy: tuple = (None, None),
                 grid: tuple = (None, None), tabwidth: int = DEFAULT_TAB_DISTANCE,
                 wordwrap: bool = True):
        '''
        Textarea Widget

        :param id:
        :param placeholder
        :param hidden:
        :param alignment:
        :param value;
        :param disabled:
        :param readonly:
        :param text_changed:
        :param selection_changed:
        :param undo_available:
        :param redo_available:
        :param maxlegth:
        :param font:
        :param fontsize:
        :param sizepolicy:
        :param grid:
        :param tabWidth:
        :param wordwrap:
        '''
        elem_type = ELEM_TYPE_TEXTAREA
        self.rtn = [elem_type, id, placeholder, hidden, alignment, value, disabled, readonly, text_changed,
                    selection_changed, undo_available, redo_available, maxlength, font, fontsize, sizepolicy, grid,
                    tabwidth, wordwrap]

    def __call__(self):
        return self.rtn


class textarea(Textarea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
###############################  LISTWIDGET  ##############################
###########################################################################

# ------------------------------------------------------------------------#


def window_list_widget(lyt, list_items, ID, mode, grid, sizepolicy, grid_pos_x, grid_pos_y, func):
    list_widget = INIT_WIDGET(ID, QListWidget())

    set_widget(lyt, grid, list_widget, grid_pos_x, grid_pos_y)
    set_size_policy(list_widget, sizepolicy)

    selection_modes = [
        [ITEM_SELECTION_MODE_NO_SELECTION, QAbstractItemView.NoSelection],
        [ITEM_SELECTION_MODE_SINGLE, QAbstractItemView.SingleSelection],
        [ITEM_SELECTION_MODE_MULTI, QAbstractItemView.MultiSelection],
        [ITEM_SELECTION_MODE_EXTENDED, QAbstractItemView.ExtendedSelection]
    ]

    # def pass_value(item):
    #     func(item.text())

    # list_widget.currentItemChanged.connect(pass_value)

    # if func != None:
    #     list_widget.itemClicked.connect(pass_value)

    # signals and hidden setup
    # create list widget id system.

    for items in selection_modes:

        new_mode = mode.lower()

        if new_mode in items:
            list_mode = items[1]
            list_widget.setSelectionMode(list_mode)
            break
    else:
        raise ItemSelectionModeError(f"{mode} is not a valid mode")

    add_list_items(list_widget, list_items)


class ListWidget:
    def __init__(self, list_items: any = None, id: any = None, mode: str = ITEM_SELECTION_MODE_SINGLE, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), func: None = None):
        '''
        List Widget

        :param list_items:
        :param id:
        :param mode:
        :param grid:
        :param sizepolicy:
        :param func:
        '''

        elem_type = ELEM_TYPE_LIST_WIDGET
        self.rtn = [elem_type, list_items, id, mode, grid, sizepolicy, func]

    def __call__(self):
        return self.rtn


class listwidget(ListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
################################   SELECT   ###############################
###########################################################################

# ------------------------------------------------------------------------#


def window_select(lyt, options, ID, placeholder, grid, sizepolicy, grid_pos_x, grid_pos_y, current_text_changed, activated):
    select = INIT_WIDGET(ID, QComboBox())

    set_widget(lyt, grid, select, grid_pos_x, grid_pos_y)
    set_size_policy(select, sizepolicy)

    select.setPlaceholderText(placeholder)

    if options != None:
        if type(options[0]) == sample_string:
            options = [options]
        elif type(options[0]) == sample_list:
            pass

        add_select_option(select, options)

    select.currentTextChanged.connect(current_text_changed)
    select.activated.connect(activated)


class Select:
    def __init__(self, options: any = None, id: any = None, placeholder: any = None, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), current_text_changed: None = None, activated: None = None):
        '''
        Select Widget

        :param options:
        :param id:
        :param placeholder:
        :param grid:
        :param sizepolicy:
        :param current_text_changed:
        :param activated:
        '''

        elem_type = ELEM_TYPE_SELECT

        self.rtn = [elem_type, options, id, placeholder, grid,
                    sizepolicy, current_text_changed, activated]

    def __call__(self):
        return self.rtn


class select(Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
##############################   PROGRESSBAR   ############################
###########################################################################

# ------------------------------------------------------------------------#


def window_progress_bar(lyt, ID, minimum, maximum, value, orientation, grid,
                        sizepolicy, text_visible, inverted, value_changed, grid_pos_x, grid_pos_y):
    progress_bar = INIT_WIDGET(ID, QProgressBar())

    set_widget(lyt, grid, progress_bar, grid_pos_x, grid_pos_y)
    set_size_policy(progress_bar, sizepolicy)

    progress_bar.setRange(minimum, maximum)

    if value != None:
        progress_bar.setValue(value)

    progress_bar.setInvertedAppearance(inverted)

    progress_bar.setTextVisible(text_visible)

    if orientation.lower() in DEFAULT_VERTICAL_TYPES:
        progress_bar.setOrientation(Qt.Vertical)
    elif orientation.lower() in DEFAULT_HORIZONTAL_TYPES:
        progress_bar.setOrientation(Qt.Horizontal)
    else:
        raise ValueError(orientation)

    # progress_bar.setTextDirection(QProgressBar.BottomToTop)

    progress_bar.valueChanged.connect(value_changed)


class ProgressBar:
    def __init__(self, id: any = None,  min: int = 0, max: int = 0, value: int = None,
                 orientation: str = SET_HORIZONTAL, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), text_visible: bool = True, inverted: bool = False, value_changed: None = None):
        '''
        ProgressBar Widget

        :param id:
        :param min:
        :param max:
        :param value:
        :param orientation:
        :param grid:
        :param sizepolicy:
        :param text_visible:
        :param inverted:
        :param value_changed:
        '''

        elem_type = ELEM_TYPE_PROGRESS_BAR

        self.rtn = [elem_type, id,  min, max, value, orientation, grid,
                    sizepolicy, text_visible, inverted, value_changed]

    def __call__(self):
        return self.rtn


class progressbar(ProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
#################################   SLIDER   ##############################
###########################################################################

# ------------------------------------------------------------------------#


def window_slider(lyt, ID, min, max, value, step, orientation, grid,
                  sizepolicy, value_changed, grid_pos_x, grid_pos_y):

    if orientation.lower() in DEFAULT_VERTICAL_TYPES:
        setOrientation = Qt.Vertical
    elif orientation.lower() in DEFAULT_HORIZONTAL_TYPES:
        setOrientation = Qt.Horizontal
    else:
        raise ValueError(orientation)

    slider = INIT_WIDGET(ID, QSlider(setOrientation))

    set_widget(lyt, grid, slider, grid_pos_x, grid_pos_y)
    set_size_policy(slider, sizepolicy)

    slider.setMinimum(min)
    slider.setMaximum(max)

    if value != None:
        slider.setValue(value)

    if step != None:
        slider.setSingleStep(step)

    slider.valueChanged.connect(value_changed)


class Slider:
    def __init__(self, id: any = None, min: int = 0, max: int = 0, value: int = None,
                 step: None = None, orientation: str = SET_HORIZONTAL, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), value_changed: None = None):
        '''
        Slider Widget

        :param id:
        :param min:
        :param max:
        :param value:
        :param step:
        :param orientation:
        :param grid:
        :param sizepolicy:
        :param value_changed:
        '''

        elem_type = ELEM_TYPE_SLIDER

        self.rtn = [elem_type, id,  min, max, value,
                    step, orientation, grid, sizepolicy, value_changed]

    def __call__(self):
        return self.rtn


class slider(Slider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
##################################   DIAL   ###############################
###########################################################################

# ------------------------------------------------------------------------#


def window_dial(lyt, ID, min, max, value, tick_target, tick, wrapping, grid,
                sizepolicy, value_changed, grid_pos_x, grid_pos_y):

    dial = INIT_WIDGET(ID, QDial())

    set_widget(lyt, grid, dial, grid_pos_x, grid_pos_y)
    set_size_policy(dial, sizepolicy)

    dial.setMinimum(min)
    dial.setMaximum(max)

    if value != None:
        dial.setValue(value)

    if tick_target != None:
        dial.setNotchTarget(tick_target)

    dial.setNotchesVisible(tick)
    dial.setWrapping(wrapping)

    dial.valueChanged.connect(value_changed)


class Dial:
    def __init__(self, id: any = None, min: int = 0, max: int = 0, value: int = None,
                 tick_target: None = None, tick: bool = False, wrapping: bool = False, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), value_changed: None = None):
        '''
        Dial Widget

        :param id:
        :param min:
        :param max:
        :param value:
        :param tick_target:
        :param tick:
        :param wrapping:
        :param grid:
        :param sizepolicy:
        :param value_changed:
        '''

        elem_type = ELEM_TYPE_DIAL

        self.rtn = [elem_type, id,  min, max, value,
                    tick_target, tick, wrapping, grid, sizepolicy, value_changed]

    def __call__(self):
        return self.rtn


class dial(Dial):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def window_table(lyt, ID, sizepolicy, grid, grid_pos_x, grid_pos_y):
    table_widget = INIT_WIDGET(ID, QTableWidget())

    set_widget(lyt, grid, table_widget, grid_pos_x, grid_pos_y)
    set_size_policy(dial, sizepolicy)

    labels = ['x', 'y']

    table_widget.setRowCount(3)
    table_widget.setColumnCount(3)
    table_widget.setHorizontalHeaderLabels(labels)
    table_widget.setItem(0, 7, QTableWidgetItem('HELLO'))

    # stretch
    table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class Table:
    def __init__(self, id: any = None, sizepolicy: tuple = (None, None), grid: tuple = (None, None)):
        elem_type = ELEM_TYPE_TABLE

        self.rtn = [elem_type, id, sizepolicy, grid]
    
    def __call__(self):
        return self.rtn
