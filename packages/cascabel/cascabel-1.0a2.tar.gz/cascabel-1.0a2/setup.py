from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

import pypandoc
long_description = open('README.md', 'r', encoding='UTF-8').read()
   
import os

archivos = []

dir_file = str(os.getcwd() + '/cascabel')
for nombre_directorio, dirs, ficheros in os.walk(dir_file):
    if nombre_directorio.find('__pycache__') == -1:
        directorio = nombre_directorio.replace(dir_file + '\\', '').replace(dir_file, '').replace('\\', '/')
        if directorio != 'cascabel' and directorio != '':
            for nombre_fichero in ficheros:
                archivos.append(directorio + '/' + nombre_fichero)

VERSION = '1.0a2'

file = open('cascabel/classes/cascabel.py', 'r')

import re

contenido = re.sub( 'VERSION = ".*"', f'VERSION = "{VERSION}"' ,file.read())

file.close()

file = open('cascabel/classes/cascabel.py', 'w')
file.write(contenido)
file.close()

DESCRIPTION = 'Paquete creado para la agilización de creación de paginas con flask'
LONG_DESCRIPTION = long_description

# Setting up
setup(
    long_description_content_type='text/markdown',
    name="cascabel",
    version=VERSION,
    author="Ignacio Aguilera Oyaneder",
    author_email="<ignacio.a.o@outlook.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['colorama', 'flask', 'python-dotenv', 'Flask-WTF', 'flask-sqlalchemy'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data = {
        '': archivos
    },
    include_package_data=True,
    entry_points={'console_scripts':['cascabel = cascabel:main'] }
)