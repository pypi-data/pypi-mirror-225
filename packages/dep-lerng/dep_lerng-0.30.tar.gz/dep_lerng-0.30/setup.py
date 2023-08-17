from setuptools import setup
setup(name='dep_lerng',
version='0.30',
description='Testing installation of Package',
url='https://github.com/Kitty2xl/dep_lerng',
author='auth',
author_email='kitty2xl41@email.com',
license='MIT',
packages=['dep_lerng'],
zip_safe=False)

"""
py -m build
py -m twine upload dist/*

"""