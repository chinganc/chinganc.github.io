from setuptools import find_packages
from setuptools import setup

requirements = [
    # "setuptools==57.5.0"
    "Flask-Markdown>=0.3",
    "Flask==1.1.2",
    "Frozen-Flask>=0.15",
    "PyYAML>=5.1",
    "pybtex==0.21",  # fails with 0.22 onwards
    "requests>=2.21",
    "jinja2==2.11.3",
    "markupsafe==1.1.1",
    "itsdangerous==1.1.0",
    "werkzeug==1.0.1"
]

setup(
    name="cac-website",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    # extras_require={"dev": dev_requirements},
)
