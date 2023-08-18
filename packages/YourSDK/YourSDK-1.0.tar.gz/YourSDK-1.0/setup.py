from setuptools import setup, Extension

module = Extension('mymodule', sources=['mymodule.c'])

setup(
    name='YourSDK',
    version='1.0',
    packages=['your_sdk'],
    ext_modules=[module],
)
