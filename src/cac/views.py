from typing import Tuple
from cac import publications
from cac.publications import list_publications
from cac import app
from flask import render_template, send_from_directory
from collections import OrderedDict


@app.route("/")
def index():
    pubs_group_years = [[2010, 2015], [2016, 2017]]
    preprints = list_publications("preprints.bib", "preprints_desc.yaml")
    pubs = list_publications("publications.bib", "publications_desc.yaml", pubs_group_years)
    workshops = list_publications("workshops.bib", "workshops_desc.yaml")
    theses = list_publications("theses.bib", "theses_desc.yaml")

    publications = []

    # color: 0 or 1 indicating different bg colors
    color = 0
    if preprints:
        publications.append(("Preprints", preprints, color))
        color = (color + 1) % 2
    if pubs:
        publications.append(("Journal/Conference Publications", pubs, color))
        color = (color + 1) % 2
    if workshops:
        publications.append(("Workshop Papers", workshops, color))
        color = (color + 1) % 2
    if theses:
        publications.append(("Theses", theses, color))

    return render_template('index.html', publications=publications)


@app.route('/docs/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['DOCS'], filename)