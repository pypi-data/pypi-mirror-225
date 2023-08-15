import os.path as path

TYPE_MARKER = '%TYPE%'
SEPERATION_MARKER = ':-sep-:'
PRE_MARK = '%<%'
POST_MARK = '%>%'

compr = [
    'button::QPushButton',
    'text:image:img::QLabel',
    'input::QLineEdit',
    'checkbox::QCheckBox',
    'radiobutton::QRadioButton',
    'toolbar::QToolBar',
    'fieldset::QGroupBox',
    'item::QToolButton',
    'textarea::QTextEdit',
    'window::QMainWindow',
    'listwidget::QListWidget',
    'select::QComboBox',
    'progressbar::QProgressBar',
    'slider::QSlider',
    'dial::QDial',
    'tabwidget::QTabWidget',
    'popup::QDialog',
    'group::QGroupBox',
    'scrollbar::QScrollBar',
    'stack::QStackedWidget',
    'tooltip::QToolTip'
]

FILE_LINKS = []

def get_file_link(css):
    get_link_css = css.split('\n')

    for line in get_link_css:
        if line.strip().startswith('@'):
            FILE_LINKS.append(line.strip())
    else:
        for links in FILE_LINKS:
            css = css.replace(links, '')
    
    for idx in range(len(FILE_LINKS)):
        FILE_LINKS[idx] = path.abspath(FILE_LINKS[idx].removeprefix('@'))

    return css

def error_check(property):
    if property.count(':') != property.count(';'):
        property = property.split(';')
        for items in property:
            if items.count(':') > 1:
                error = items.split(' ')
                error.remove('')

                cnt = len(error) / 2
                error = error[0:int(cnt)]
                csserr = ' '.join(error).strip()

                raise ValueError(
                    f"'{csserr}' missing a semi-colon")


def console_css(user_css):
    user_css = get_file_link(user_css)
    css = []
    user_css = user_css.replace('[', '{').replace(']', '}')
    user_css = user_css.split('}')
    stylesheet = ""

    key_version = []
    make_key_version = {}

    for item in user_css:
        item = item.replace('\n', '').replace('   ', '')
        item = item.split('{')
        if len(item[0]) != 0:
            css.append(item)

    def local(name, property):
        merged_chunk = f'{name.strip()} [{property}]'
        final_chunk = merged_chunk.replace('[', '{').replace(']', ' } ')

        return final_chunk

    for items in css:

        valid = False

        if len(items) == 2:
            name = items[0]
            if ':' in name:
                idx = name.index(':')
                selector = name[idx:]
                name = name[:idx]
            else:
                selector = ''

            chunk_name = name.strip()
            chunk_name = chunk_name.lower()
            property = items[1]

            # checks whether style is missing a semi-colon
            error_check(property)

            for widget_types in compr:
                if chunk_name in widget_types:
                    type_id = compr.index(widget_types)
                    item = compr[type_id].split('::')
                    if chunk_name in item:
                        widget_name = item[-1]
                        stylesheet += local(widget_name + selector, property)

                        valid = True

            if valid != True:
                if '#' in name:
                    name = int(name.replace('#', ''))
                else:
                    name = name.strip()

                if len(selector) != 0:
                    property = selector + SEPERATION_MARKER + property

                # name = name + selector
                # x = [name, property]
                # key_version.append(x)

                KEY = name
                if SEPERATION_MARKER in property:
                    property = property.split(SEPERATION_MARKER)
                    property = f'{TYPE_MARKER}{property[0]}{PRE_MARK + property[1] + POST_MARK}'
                else:
                    property = f'{TYPE_MARKER}{PRE_MARK + property + POST_MARK}'

                property = property.replace(
                    PRE_MARK, '{').replace(POST_MARK, '}')

                if make_key_version.get(KEY):
                    make_key_version[KEY] = make_key_version[KEY] + \
                        ' ' + property
                else:
                    make_key_version[KEY] = property

    for KEY in make_key_version.keys():
        key_version.append([KEY, make_key_version[KEY]])

    return (key_version, stylesheet)


def get_style_check(css):
    css = css.replace('[', '{').replace(']', '}')
    if '{' in css and '}' in css:
        NotRequired, css = console_css(css)
    else:
        errorcheck = css.split(';')
        for items in errorcheck:
            if items.count(':') > 1:
                csserr = items.split(' ')
                csserr = csserr[:2]
                csserr = ' '.join(csserr).strip()
                raise ValueError(f"'{csserr}' missing a semi-colon")

    return css
