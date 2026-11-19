"""Sovelluksen käynnistys."""


from pathlib import Path

from flask import Flask, request, redirect, send_from_directory

from reference import Reference, generate_cite_key


ROOT = Path(__file__).resolve().parent.parent

app = Flask(__name__)
references: list[Reference] = []

TYPE_MAP = {
    "book": "book",
    "article": "article",
    "inproceedings": "inproceedings",
    "web": "misc",
    "unspecified": "misc",
}


@app.get("/")
def index():
    """Näyttää lomakkeen."""
    return send_from_directory(ROOT, "index.xhtml")


@app.get("/tyyli.css")
def style():
    """Palauttaa tyylitiedoston."""
    return send_from_directory(ROOT, "tyyli.css")


@app.post("/submit")
def submit():
    """Vastaanottaa lomakkeen ja tallentaa viitteen."""
    form = request.form

    authors = [a.strip() for a in form.getlist("ref-authors") if a.strip()]
    if not authors:
        return "Vähintään yksi kirjoittaja vaaditaan", 400

    try:
        year = int(form["ref-year"])
    except (KeyError, ValueError):
        return "Vuoden pitää olla kokonaisluku", 400

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
