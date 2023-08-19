from setuptools import setup


with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='MorseCodePy',
    packages=['MorseCodePy'],
    version='1.0.4',
    author='CrazyFlyKite',
    author_email='karpenkoartem2846@gmail.com',
    url='https://github.com/CrazyFlyKite/MorseCode',
    description='Easily translate text into Morse code',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
