from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'Roboreactormaster'
LONG_DESCRIPTION = 'A package that allows you to build robotics middleware.'

# Setting up
setup(
    name="roboreactmaster",
    version=VERSION,
    author="Roboreactor",
    author_email="<support@idatabots.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['opencv-python', 'smbus','smbus2' ,'Adafruit-Blinka', 'bmp280','pyinstaller' ,'adafruit-circuitpython-mpu6050', 'adafruit-circuitpython-icm20x', 'imultils', 'uindecode','streamlit','Pynq','python3-scapy','scipy','sklearn','matplotlib','pandas','Pillow','PyPDF2','pdfquery','adafruit-circuitpython-pca9685','adafruit-circuitpython-servokit','face_recognition','pyzbar','SpeechRecognition'],
    keywords=['python', 'robotics', 'robotic middleware', 'service robot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
