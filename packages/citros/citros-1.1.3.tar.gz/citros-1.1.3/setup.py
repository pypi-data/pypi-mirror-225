#!/usr/bin/env python3
# ==============================================
#  ██████╗██╗████████╗██████╗  ██████╗ ███████╗
# ██╔════╝██║╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝
# ██║     ██║   ██║   ██████╔╝██║   ██║███████╗
# ██║     ██║   ██║   ██╔══██╗██║   ██║╚════██║
# ╚██████╗██║   ██║   ██║  ██║╚██████╔╝███████║
#  ╚═════╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝                                        
# ==============================================
from setuptools import setup, find_packages
from pathlib import Path
import citros_meta

CURRENT_DIR = Path(__file__).parent

try:
    import sys
    from semantic_release import setup_hook
    setup_hook(sys.argv)
except ImportError:
    pass

setup(
    name=citros_meta.__title__,
    version=citros_meta.__version__,
    author=citros_meta.__author__,
    author_email=citros_meta.__author_email__,
    packages=find_packages(),
    package_data={
        citros_meta.__title__: ['data/schemas/*.json'],
        citros_meta.__title__: ['data/defaults/*.json']
    },
    scripts=[
        'bin/citros',    
    ],
    url=citros_meta.__url__,
    license=citros_meta.__license__,
    description='A cli entrypoint for the citros system.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    install_requires=[
        "ansicolors",
        "gql",
        "graphql-core",
        "requests",
        "rosdep",
        "python-decouple",
        "requests_toolbelt",
        "soupsieve",
        "bs4",
        "zipp",
        "pyjwt",
        "psycopg2-binary",
        "urllib3",
        "InquirerPy",
        "GitPython",
        "jsonschema",
        "cryptography",
        "numpy",
        "psutil",
        "cmakeast",
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-exporter-otlp-proto-grpc",
        "pydantic==1.10.12",
        "python-on-whales" 
    ],
    py_modules=['citros', 'citros_meta', 'data'],
    project_urls={
        "Documentation": "http://citros.io/doc/docs_cli",
        "Source Code": "https://github.com/lulav/citros_cli",
        "Bug Tracker": "https://github.com/lulav/citros_cli/issues",
    }
)

