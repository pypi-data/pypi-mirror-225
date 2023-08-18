from setuptools import setup, find_packages

setup(
    name='textweaver',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn',
        'ksuid',
        'psycopg2-binary',
        'nltk',
        'transformers',
        'termcolor',
        'pydantic',
    ],
    entry_points={
        'console_scripts': [
            'textweaver=hamming.app:start_app',  # This points to the run function in app.py
        ],
    },
)