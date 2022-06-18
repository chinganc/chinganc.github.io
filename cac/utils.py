import csv
import os

import yaml
from flask import render_template
from cac import app
from cac import markdown
from cac import bp


DATA_ROOT = os.path.join(app.root_path, "data")

def load_yaml(fname):
    """
    Return data from a YAML file at {app.root_path}/data/{fname}.
    """
    with open(os.path.join(DATA_ROOT, fname)) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_markdown(fname):
    """
    Return formatted text from a Markdown file at
    {app.root_path}/pages/{fname}.
    """
    with app.open_resource(os.path.join("data", fname), "r") as f:
        return markdown(f.read())
