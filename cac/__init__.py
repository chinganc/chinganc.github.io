import os
from flask import Blueprint
from flask import Flask
from flaskext.markdown import Markdown

bp = Blueprint("cac", __name__)


app = Flask(__name__)
app.config["DOCS"] = os.path.join(
    bp.root_path, "docs"
)
markdown = Markdown(app, extensions=["markdown.extensions.extra"])

import cac.views

