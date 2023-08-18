from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='json2pdfConverter',
    version='0.1',
    packages=['pdf_generator_rysun'],
    install_requires=[
        'pandas',
        'jinja2',
        'pdfkit',
        'PyPDF2'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
