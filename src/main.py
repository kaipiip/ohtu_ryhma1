"""Sovelluksen käynnistys."""


from pathlib import Path

from flask import Flask, request, redirect, send_from_directory, render_template

from reference import Reference, generate_cite_key
from reference_formatter import format_reference
from validation import validate_form



ROOT = Path(__file__).resolve().parent.parent

app = Flask(__name__, template_folder=str(ROOT))
references: list[Reference] = []

TYPE_MAP = {
    "book": "book",
    "article": "article",
    "inproceedings": "inproceedings",
    "web": "misc",
    "unspecified": "misc",
}


@app.get("/")
def list_references():
    """Näyttää kaikki tallennetut viitteet ja lomakkeen."""
    rows = [(ref, format_reference(ref)) for ref in references]
    return render_template("index.xhtml", rows=rows)


@app.get("/tyyli.css")
def style():
    """Palauttaa tyylitiedoston."""
    return send_from_directory(ROOT, "tyyli.css")

@app.post("/submit")
def submit():
    """Vastaanottaa lomakkeen ja tallentaa viitteen."""
    form = request.form

    errors = validate_form(form)
    if errors:
        return "<br>".join(errors), 400

    authors = [a.strip() for a in form.getlist("ref-authors") if a.strip()]
    year = int(form["ref-year"])

    reference = Reference(
        cite_key=generate_cite_key(authors, year),
        entry_type=TYPE_MAP.get(form.get("reference", ""), "misc"),
        author=authors,
        title=form.get("ref-title", "").strip(),
        year=year,
        month=form.get("ref-month", "").strip(),
        journal=form.get("ref-journal", "").strip(),
        booktitle=form.get("ref-conference", "").strip(),
        publisher=form.get("ref-publisher", "").strip(),
        volume=form.get("ref-volume", "").strip(),
        number=form.get("ref-issue", "").strip(),
        pages=form.get("ref-pages", "").strip(),
        doi=form.get("ref-doi", "").strip(),
        url=form.get("ref-url", "").strip(),
    )
    references.append(reference)

    return redirect("/")


def main():
    """Käynnistää sovelluksen."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
