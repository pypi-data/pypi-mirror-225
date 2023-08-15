from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    LONG_DESCRIPTION = readme.read()


VERSION = '0.2.1'
DESCRIPTION = 'Write Simple and Quick Python GUI Application'
KEYWORDS = ['gui', 'clera', 'simple', 'simplegui', 'pyside', 'pyside6', 'python', 'easy']


CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
]

def init_ref(folder):
    directory = [folder]
    data_ref = dict()
    excluded = ['docs', 'files']

    for dir in directory:
        files = []
        for item in os.scandir(dir):
            if item.is_dir():
                directory.append(item.path)
            elif item.is_file():
                name = item.name
                if name.endswith('.py') or name.endswith('.pyi'):
                    files.append(name)
        else:
            if len(files) != 0:
                for item in excluded:
                    if dir.endswith(item):
                        break
                else:
                    data_ref[dir] = files
    else:
        return data_ref

data_ref = init_ref('clera')

# Setting up
setup(
    name="clera",
    version=VERSION,
    author="Erasmus A. Junior",
    author_email="eirasmx@pm.me",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    licence='GNU LGPLv3',
    long_description=LONG_DESCRIPTION,
    packages=[data for data in data_ref],
    package_data=data_ref,
    python_requires='>=3.7',
    install_requires=['PySide6'],
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    py_modules=['clera'],
    entry_points = {
        'console_scripts': [
            'clera-editor = clera:editor'
        ]
    },
)
