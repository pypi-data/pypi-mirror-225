from setuptools import setup, find_packages

VERSION = '0.1.5'
DESCRIPTION = 'Absolute Molecule File library extension for python'
LONG_DESCRIPTION = 'Absolute Molecule File library extension for python. Absolute Molecule File (*.amf) is a specific kind of a filetype that allows people to create molecules and proteins easily. You can access the documentation from [here](https://UDoruk3250.github.io/amf/Documentation)'


setup(name='amfpy-python',
      version=VERSION,
      author='Doruk Alp Uzunarslan',
      author_email='duzunarslan27@my.uaa.k12.tr',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=['matplotlib'],
      keywords=['python', 'modelling', 'molecule', 'atom', 'molecular modelling', 'bioinformatics'])
