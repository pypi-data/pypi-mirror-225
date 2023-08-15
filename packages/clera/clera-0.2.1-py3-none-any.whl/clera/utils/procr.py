# from ..widgets import WindowButton, WindowInput, WindowText, WindowRadioButton,
# from ..widgets import WindowCheckbox, WindowImage, WindowTextarea


from ..widgets import *
from .handlers import *


def LayItOut(lyt, elem_type, property, grid_pos_x: None = None, grid_pos_y: None = None):
    if elem_type == ELEM_TYPE_BUTTON:
        [
            NotRequired,
            button_text,
            func, 
            icon,
            id, 
            disabled,
            default,
            grid,
            sizepolicy,
            checkable,
            checked,
            hidden,
            focus,
            icon_size, 
            statustip,
            tooltip,
            shortcut
        ] = property
        widget = window_button(
            lyt, button_text, func, icon, id, disabled, default, sizepolicy, grid, grid_pos_x, grid_pos_y, checkable, checked, hidden, focus, 
            icon_size, statustip, tooltip, shortcut)

    elif elem_type == ELEM_TYPE_INPUT:
        [
            NotRequired,
            placeholder,
            id,
            value,
            type,
            disabled,
            readonly,
            maxlength,
            hidden,
            font,
            fontsize,
            text_changed,
            return_pressed,
            editing_finished,
            text_edited,
            selection_changed,
            sizepolicy,
            grid
        ] = property

        widget = window_input(lyt, placeholder, id, value, type, disabled, readonly, maxlength, hidden,
                              font, fontsize, text_changed, return_pressed, editing_finished, text_edited,
                              selection_changed, sizepolicy, grid, grid_pos_x, grid_pos_y)

    elif elem_type == ELEM_TYPE_TEXT:
        [
            NotRequired,
            text,
            id,
            link,
            hovered,
            clicked,
            buddy,
            alignment,
            wordwrap,
            grid,
            sizepolicy,
            hidden
        ] = property

        widget = window_text(lyt, text, id, link, hovered, clicked, buddy, alignment,
                             wordwrap, sizepolicy, grid, grid_pos_x, grid_pos_y, hidden)

    elif elem_type == ELEM_TYPE_IMAGE:
        [
            NotRequired,
            image,
            id,
            size,
            alignment,
            grid,
            sizepolicy,
            hidden
        ] = property

        widget = window_image(
            lyt, image, id, size, alignment, hidden, sizepolicy, grid, grid_pos_x, grid_pos_y)

    elif elem_type == ELEM_TYPE_CHECKBOX:
        [
            NotRequired,
            name,
            checked,
            id,
            state_changed,
            toggled,
            grid,
            sizepolicy
        ] = property

        widget = window_checkbox(
            lyt, name, checked, id, state_changed, toggled, sizepolicy, grid, grid_pos_x, grid_pos_y)

    elif elem_type == ELEM_TYPE_RADIO_BUTTON:
        [
            NotRequired,
            name,
            checked,
            id,
            toggled,
            grid,
            sizepolicy
        ] = property

        widget = window_radio_button(
            lyt, name, checked, id, toggled, sizepolicy, grid, grid_pos_x, grid_pos_y)

    elif elem_type == ELEM_TYPE_TEXTAREA:
        [
            NotRequired,
            id, placeholder,
            hidden,
            alignment,
            value,
            disabled,
            readonly,
            text_changed,
            selection_changed,
            undo_available,
            redo_available,
            maxlength,
            font,
            fontsize,
            sizepolicy,
            grid,
            tabwidth,
            wordwrap
        ] = property

        widget = window_textarea(lyt, id, placeholder, hidden, alignment, value, disabled, readonly,
                                 text_changed, selection_changed, undo_available, redo_available,
                                 maxlength, font, fontsize, sizepolicy, grid, grid_pos_x, grid_pos_y, 
                                 tabwidth, wordwrap)

    elif elem_type == ELEM_TYPE_LIST_WIDGET:
        [
            NotRequired,
            list_items,
            id,
            mode,
            grid,
            sizepolicy,
            func,
        ] = property
        widget = window_list_widget(lyt, list_items, id, mode, grid, sizepolicy, grid_pos_x,
                                    grid_pos_y, func)

    elif elem_type == ELEM_TYPE_SELECT:
        [
            NotRequired,
            options,
            id,
            placeholder,
            grid,
            sizepolicy,
            current_text_changed,
            activated
        ] = property
        widget = window_select(lyt, options, id, placeholder, grid,
                               sizepolicy, grid_pos_x, grid_pos_y, current_text_changed, activated)

    elif elem_type == ELEM_TYPE_PROGRESS_BAR:
        [
            NotRequired,
            id,
            minimum,
            maximum,
            value,
            orientation,
            grid,
            sizepolicy,
            text_visible,
            inverted,
            value_changed
        ] = property
        widget = window_progress_bar(
            lyt, id, minimum, maximum, value,  orientation, grid,
            sizepolicy, text_visible, inverted, value_changed, grid_pos_x, grid_pos_y)

    elif elem_type == ELEM_TYPE_SLIDER:
        [
            NotRequired,
            id,
            min,
            max,
            value,
            step,
            orientation,
            grid,
            sizepolicy,
            value_changed
        ] = property
        widget = window_slider(lyt, id, min, max, value, step, orientation,
                               grid, sizepolicy, value_changed, grid_pos_x, grid_pos_y)

    elif elem_type == ELEM_TYPE_DIAL:
        [
            NotRequired,
            id,
            min,
            max,
            value,
            tick_target,
            tick,
            wrapping,
            grid,
            sizepolicy,
            value_changed
        ] = property
        widget = window_dial(lyt, id, min, max, value, tick_target, tick, wrapping,
                             grid, sizepolicy, value_changed, grid_pos_x, grid_pos_y)
    
    elif elem_type == ELEM_TYPE_TABLE:
        [
            NotRequired,
            id,
            sizepolicy,
            grid
        ] = property
        widget = window_table(lyt, id, sizepolicy, grid, grid_pos_x, grid_pos_y)

    try:
        return widget
    except:
        pass
