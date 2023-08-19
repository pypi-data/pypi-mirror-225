from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = "Dynamic multiselect filters for Streamlit"
LONG_DESCRIPTION = 'Custom component to create dynamic multiselect filters in Streamlit.'

setup(
    name="streamlit_dynamic_filters",
    version=VERSION,
    author="Oleksandr Arsentiev",
    author_email="<arsentiev9393@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['streamlit'],
    keywords=['streamlit', 'custom', 'component'],
    license="MIT",
    url="https://github.com/arsentievalex/streamlit-dynamic-filters",
)