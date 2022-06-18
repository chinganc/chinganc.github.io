import argparse
import os

from flask_frozen import Freezer
from cac import app

freezer = Freezer(app)


@freezer.register_generator
def pdf_file_generator():
    paperdir = app.config["DOCS"]
    pdf_files = []
    for file in os.listdir(paperdir):
        if file.endswith(".pdf") or file.endswith(".PDF"):
            pdf_files.append(file)
    for filename in pdf_files:
        yield ("download_file", {"filename": filename})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", "-b", help="Base url for hosted files.")
    parser.add_argument("--dest", "-d", help="Destination for static files.")
    args = parser.parse_args()
    if args.base_url:
        app.config["FREEZER_BASE_URL"] = args.base_url
    if args.dest:
        app.config["FREEZER_DESTINATION"] = os.path.abspath(args.dest)
    freezer.freeze()
