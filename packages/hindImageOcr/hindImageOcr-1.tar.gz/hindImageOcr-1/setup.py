from setuptools import setup, find_packages

setup(
    name='hindImageOcr',
    version='1',  # Update with the appropriate version
    packages=find_packages(),
    install_requires=[
        'easyocr>=1.5.0',
        'googletrans==4.0.0-rc1',
        'Pillow>=9',
    ],
)
