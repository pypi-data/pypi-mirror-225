import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.3'
PACKAGE_NAME = 'RFMCustomer'
AUTHOR = 'Sebastian Marat Urdanegui Bisalaya'
AUTHOR_EMAIL = 'sebasurdanegui@gmail.com'
URL = 'https://github.com/SebastianUrdaneguiBisalaya/Segmentacion-RFM'

LICENSE = 'MIT'
DESCRIPTION = 'Librería para realizar una segmentación RFM.'
LONG_DESC_TYPE = "text/markdown"


INSTALL_REQUIRES = [
      'pandas', 'numpy', 'matplotlib', 'seaborn',
      'plotly', 'datetime'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)