from setuptools import setup, find_packages

setup(
    name="mpl-add-ons",
    version='0.0.3',
    author="Ethan Blake",
    description="helper functions to make using matplotlib easier, more efficient and streamlined",
    packages=find_packages(),
    install_requires=['matplotlib', 'PyQt5']
)
