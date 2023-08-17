from setuptools import setup, find_packages

setup(
    name='db-lonewolpy',          # Replace with your library name
    version='1.0.1',              # Specify the version number
    packages=find_packages(),   # Automatically discover and include packages
    install_requires=[
        'mysql-connector-python==8.1.0',
        'python-dotenv==1.0.0'
    ],
    description='DB Connector',
    author='Nikunj',
    author_email='nikunjs@spaising.com',
    url='https://github.com/nikunjs21/db-lonewolpy',
    license='MIT',
)
