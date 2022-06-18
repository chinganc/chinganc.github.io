# Website Maintainence Instructions
## To Preview the Website
1. (Recommended) Create a virtual environment with conda.
   ```bash
   conda create --name flask python=3.7
   conda activate flask
   ```
2. Clone the repository and install the dependencies with `pip`.
   ```bash
   # install deps
   cd cac-website
   pip install -e .[dev]
   ```
3. Run local dynamic site, which can be accessed at http://localhost:5000.
   ```bash
   FLASK_APP=cac flask run
   ```

## Deployment

1. Generate static site for deployment using [Frozen-Flask](https://pythonhosted.org/Frozen-Flask/).

```bash
python freeze.py -d www
```

2. (Optional) View the static site locally. The website is accessible at http://127.0.0.1:8000/ on your browser.

```bash
cd www
# set up a local python server
python -m http.server 8000 --bind 127.0.0.1
```

## To Update Contents
- Bio:
  - Html: `cac/templates/bio.html`
- Photo:
  - File: `cac/static/images/ching-an-cheng.jpg`
  - Html: `cac/templates/index.html` (line 5)
- CV:
  - File: `cac/docs/ching-an-cheng-cv.pdf`
- Publications:
  - Preprints:
    - BibTex: `cac/data/pubs/preprints.bib`
    - Description yaml (for adding `pdf_link`, `pdf_file`, or `note`): `cac/data/pubs/preprints_desc.yaml`
    - PDF file (if applicable): `cac/docs/[pdf_file]`. Remeber to add `pdf_file` in the description yaml file.
    - Html: `cac/templates/preprints.html`
  - Conference/Journal Publications:
    - BibTex: `cac/data/pubs/publications.bib`
    - Description yaml (for adding `pdf_link`, `pdf_file`, or `note`): `cac/data/pubs/publications_desc.yaml`
    - PDF file (if applicable): `cac/docs/[pdf_file]`. Remeber to add `pdf_file` in the description yaml file.
    - Html: `cac/templates/publications.html`
  - Workshop Papers:
    - BibTex: `cac/data/pubs/workshops.bib`
    - Description yaml (for adding `pdf_link`, `pdf_file`, or `note`): `cac/data/pubs/workshops_desc.yaml`
    - PDF file (if applicable): `cac/docs/[pdf_file]`. Remeber to add `pdf_file` in the description yaml file.
    - Html: `cac/templates/workshops.html`


