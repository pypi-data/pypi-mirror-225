from setuptools import setup, find_packages

setup(
    name='swagern',
    version='0.1',
    author='Varsha Ryali, Trilokesh Chandra Barua, Anthony Fernandes, Shubhra Debnath',
    author_email='varsha.ryali@newfold.com, trilokesh.barua@newfold.com, anthony.fernandes@newfold.com, shubhra.debnath@newfold.com, ',
    description='A command-line tool for generating Tavern test cases from Swagger API specifications.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'swagern': ['mappers/*.yaml', 'swagger/*.yaml', 'swagern/templates/tavern_template_default.yaml'],
    },
    install_requires=[
        'click',
        'PyYAML',
        'jinja2==3.1.2',
        'requests==2.26.0',
        'Tavern==1.0.0',
        'fuzzywuzzy==0.18.0',
        'pytest-sugar'
    ],
    entry_points='''
        [console_scripts]
        swagern=swagern.main:cli
    ''',
)
