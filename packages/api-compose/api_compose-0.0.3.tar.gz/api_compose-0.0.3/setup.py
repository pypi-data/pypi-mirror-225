from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('src/api_compose/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="api_compose",
    version=main_ns['__version__'],
    description="A Framework for orchestrating, asserting and reporting on API calls with templates",
    author="Ken",
    author_email="kenho811job@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    # include all core templates and value files
    install_requires=[
        "requests==2.29.0",
        "jsonpath_ng==1.5.3",
        "typer[all]==0.9.0",
        "jinja2==3.1.2",
        "pyyaml==6.0",
        "pydantic==2.0.3",
        "networkx==3.1",
        "python-dotenv==1.0.0",
        "matplotlib==3.7.2",
        "lxml==4.9.3",
    ],
    extras_require={
        "test": [
            "pytest==7.3.1",
            # Mock REST server
            "connexion==2.14.2",
            "connexion[swagger-ui]",
            'pydeps==1.12.8',
            'dicttoxml==1.7.16',
        ],
        "dist": [
            'twine',
        ]
    },
    entry_points={
        'console_scripts': [
            'acp=api_compose.cli.main:app',
        ]
    },
)