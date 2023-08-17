from setuptools import setup, find_packages

setup(
    name='Pokemon-Py',
    version='0.11',
    description='A Python wrapper for PokeAPI (https://pokeapi.co/)',
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author='Rick Verbon',
    author_email='rick89@gmail.com',
    url='',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any dependencies required by your package
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
