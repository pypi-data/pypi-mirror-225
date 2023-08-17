from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pybaseanal',
    version='0.0.3',
    description='A package to import basic libraries and perform basic data analysis',
    author= 'Ateendra Jha',
    author_email="jhaateendra@gmail.com",
    url = 'http://pybaseanal.phaf.in',
    long_description_content_type="text/markdown",
    long_description = long_description,
    packages=setuptools.find_packages(),
    keywords=['python', 'pandas', 'numpy', 'basic libraries', 'Null analysis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['pybaseanal'],
    package_dir={'':'src'},
    install_requires = [
        'pandas',
        'numpy',
        'seaborn',
        'matplotlib'
    ]
)