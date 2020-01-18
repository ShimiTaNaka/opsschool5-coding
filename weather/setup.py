from setuptools import setup

setup(
    name='Weather',
    version='2.0',
    py_modules=['weather'],
    install_requires=[
        'Click', 'requests'
    ],
    entry_points='''
        [console_scripts]
        weather=weather:cli
    '''
)
