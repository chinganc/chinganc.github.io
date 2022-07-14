import os
import re
from collections import OrderedDict

from pybtex.database import BibliographyData
from pybtex.database import parse_file
from pybtex.richtext import Tag
from pybtex.richtext import Text
from pybtex.style.names import name_part
from pybtex.style.template import field
from pybtex.style.template import join
from pybtex.style.template import names
from pybtex.style.template import tag
from cac import bp
from cac.utils import load_yaml
from cac import markdown

def latex_to_richtext(latex):
    # Converts a single {\textbf{...}} to bolded rich text
    textbf = re.match(r"(?P<pre>.*)\{\\textbf\{(?P<b>[^\{\}]*?)\}\}(?P<post>.*)", latex)

    if textbf:
        return Text(
            latex_to_richtext(textbf.group("pre")),
            Tag("b", latex_to_richtext(textbf.group("b"))),
            latex_to_richtext(textbf.group("post")),
        )

    # Dispatches math mode to mathmode_to_richtext
    mathmode = re.match(r"(?P<pre>.*)\$(?P<math>[^\$]*?)\$(?P<post>.*)", latex)

    if mathmode:
        return Text(
            latex_to_richtext(mathmode.group("pre")),
            mathmode_to_richtext(mathmode.group("math")),
            latex_to_richtext(mathmode.group("post")),
        )

    return Text(latex)


def mathmode_to_richtext(mathmode):
    # Converts a single ^{...} to superscript rich text
    superscript = re.match(r"(?P<pre>.*)\^\{(?P<sup>[^\{\}]*?)\}(?P<post>.*)", mathmode)

    if superscript:
        return Text(
            latex_to_richtext(superscript.group("pre")),
            Tag("sup", latex_to_richtext(superscript.group("sup"))),
            latex_to_richtext(superscript.group("post")),
        )

    return Text(mathmode)


class BibStyle:
    from pybtex.backends.latex import Backend as LaTeXBackend

    latex = LaTeXBackend()

    def _format_name(self, person):
        rich_first_name = [latex_to_richtext(
            first_name.render(self.latex)
        ) for first_name in person.rich_first_names]

        rich_middle_name = [latex_to_richtext(
            middle_name.render(self.latex)
        ) for middle_name in person.rich_middle_names]

        rich_prelast_name = [latex_to_richtext(prelast_name.render(self.latex)) for prelast_name in person.rich_prelast_names]

        rich_last_name = [latex_to_richtext(last_name.render(self.latex)) for last_name in person.rich_last_names]
        template = join[
            name_part(tie=True, abbr=True)[rich_first_name + rich_middle_name], name_part[rich_prelast_name + rich_last_name]
        ]
        return template

    def _format_field(self, field_name, entry):
        template = tag("b")[field(field_name)]
        data = template.format_data(entry)
        return data.render_as("text")

    def format_names(self, entry):
        for person in entry.persons["author"]:
            person.text = self._format_name(person)
        template = join[names("author", sep=", ", sep2=" and ", last_sep=", and ")]
        authors = template.format_data(entry)
        authors = authors.render_as("text")
        # replace * with \* since * is a special char for markdown
        authors = authors.replace("*", "\*")
        # boldface name
        authors = authors.replace("C.-A. Cheng", "**C.-A. Cheng**")
        authors = markdown(authors)
        return authors

    def format_title(self, entry):
        return self._format_field("title", entry)

    def format_venue(self, entry):
        venue = None
        if entry.type == "inproceedings":
            venue = self._format_field("booktitle", entry)
        elif entry.type == "article":
            journal = self._format_field("journal", entry)
            venue = journal
        elif entry.type == "phdthesis":
            venue = f'PhD thesis, {self._format_str(entry.fields["school"])}'
        elif entry.type == "mastersthesis":
            venue = f'Master\'s thesis, {self._format_str(entry.fields["school"])}'
        elif entry.type == "techreport":
            venue = f'Technical Report, {self._format_str(entry.fields["institution"])}'
        return venue

    def format_year(self, entry):
        return int(entry.fields["year"])


def list_publications(bib_filename, yaml_filename=None, group_years=None):
    bib_path = os.path.join(
        bp.root_path, "data", "pubs", bib_filename
    )
    bib = parse_file(bib_path)

    if yaml_filename is not None:
        pub_overwrite_data = load_yaml(os.path.join("pubs", yaml_filename))
    else:
        pub_overwrite_data = dict()

    style = BibStyle()

    pubs = {}

    for pub_id, entry in bib.entries.items():
        title = style.format_title(entry)
        names = style.format_names(entry)
        venue = style.format_venue(entry)
        year = style.format_year(entry)

        if (year,) not in pubs:
            pubs[(year,)] = []

        if pub_id in pub_overwrite_data:
            pub_overwrite = pub_overwrite_data[pub_id]
        else:
            pub_overwrite = {}

        pub = {
            "id": pub_id,
            "title": title,
            "authors": names,
            "venue": venue,
            "year": year,
            "pdf_link": pub_overwrite["pdf_link"] if "pdf_link" in pub_overwrite else "",
            "pdf_file": pub_overwrite["pdf_file"] if "pdf_file" in pub_overwrite else "",
            "website": pub_overwrite["website"] if "website" in pub_overwrite else "",
            "note": pub_overwrite["note"] if "note" in pub_overwrite else "",
        }

        pubs[(year,)].append(pub)

    if group_years is not None:
        for g in group_years:
            pub_list = []
            for year in range(g[0], g[1] + 1):
                if (year,) in pubs:
                    pub_list.extend(pubs[(year,)])
                    del pubs[(year,)]
            pubs[(g[0], g[1])] = pub_list


    for k in pubs.keys():
        pubs[k].reverse()

    pubs = OrderedDict(sorted(pubs.items(), key=lambda t: t[0][0], reverse=True))

    pubs_str = OrderedDict()
    for k, v in pubs.items():
        if len(k) == 1:
            pubs_str[str(k[0])] = v
        else:
            pubs_str[str(k[0]) + '-' + str(k[1])] = v
    return pubs_str

if __name__ == "__main__":
    pubs = list_publications("publications.bib")
    print(pubs)