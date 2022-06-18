from cac.publications import list_publications
from cac import app
from flask import render_template, send_from_directory


@app.route("/")
def index():
    pubs_group_years = [[2010, 2015], [2016, 2017]]
    preprints = list_publications("preprints.bib", "preprints_desc.yaml")
    pubs = list_publications("publications.bib", "publications_desc.yaml", pubs_group_years)
    workshops = list_publications("workshops.bib", "workshops_desc.yaml")
    theses = list_publications("theses.bib", "theses_desc.yaml")

    return render_template('index.html', preprints=preprints, pubs=pubs, workshops=workshops, theses=theses)


@app.route('/docs/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['DOCS'], filename)