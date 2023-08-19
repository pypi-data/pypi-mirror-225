from setuptools import setup


with open('README.md', 'r') as readme:
    description = readme.read()

setup(
    name='MorseCodePy',
    packages=['MorseCodePy'],
    version='1.0.5',
    author='CrazyFlyKite',
    author_email='karpenkoartem2846@gmail.com',
    description='Easily translate text into Morse code',
    long_description=description,
    long_description_content_type='text/markdown'
)
