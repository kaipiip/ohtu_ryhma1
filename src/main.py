"""Sovelluksen käynnistys."""

from pathlib import Path

from flask import Flask, request, redirect, send_from_directory, render_template, url_for, abort, Response

from bibtex_formatter import references_to_bibtex
from reference import Reference, generate_cite_key
from reference_formatter import format_reference
from validation import validate_form
import storage



ROOT = Path(__file__).resolve().parent.parent

app = Flask(__name__, template_folder=str(ROOT))

TYPE_MAP = {
    "book": ("book","Kirja"),
    "article": ("article","Artikkeli"),
    "inproceedings": ("inproceedings","Konferenssijulkaisu"),
    "web": ("web","Web-sivu"),
    "unspecified": ("unspecified","Muu"),
}

@app.route("/<ref_id>")
def edit_ref(ref_id):
    """Vie muokattavaksi valitun viitteen kentät lomakkeelle"""
    ref = storage.get_reference(ref_id)
    if ref is None:
        abort(404)
    return render_template("index.xhtml", ref=ref, types=TYPE_MAP)

@app.route("/<ref_id>", methods=["POST"])
def update_ref(ref_id):
    """Päivittää valitun vitteen tietokannassa"""
    # TO-DO viitteen päivitys tietokannassa
    form = request.form
    errors = validate_form(form)
    if errors:
        return "<br>".join(errors), 400

    authors = [a.strip() for a in form.getlist("ref-authors") if a.strip()]
    year = int(form["ref-year"])

    reference = Reference(
        cite_key= ref_id,
        entry_type=TYPE_MAP.get(form.get("ref-type", ""), ("misc","Muu"))[0],
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

    storage.update_reference(ref_id, reference)

    return redirect(url_for("list_references"))

@app.route("/remove_ref")
def remove_ref(ref_id):
    """Poistaa valitun viitteen tietokannasta"""
    storage.remove_reference(ref_id)
    return redirect("/")

@app.get("/")
def list_references():
    """Näyttää kaikki tallennetut viitteet ja lomakkeen."""
    references = storage.load_references()
    rows = [(ref, format_reference(ref)) for ref in references]
    return render_template("index.xhtml", rows=rows, types=TYPE_MAP)

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
        entry_type=TYPE_MAP.get(form.get("ref-type", ""), ("misc","Muu"))[0],
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
        address=form.get("ref-city", "").strip(),
    )
    storage.add_reference(reference)

    return redirect("/")

@app.get("/bibtex")
def bibtex():
    """Näyttää viitteet BibTeX-muodossa selaimessa."""
    references = storage.load_references()
    text = references_to_bibtex(references)
    return Response(text, mimetype="text/plain; charset=utf-8")


@app.get("/bibtex/download")
def bibtex_download():
    """Lataa viitteet .bib-tiedostona."""
    references = storage.load_references()
    text = references_to_bibtex(references)
    return Response(
        text,
        mimetype="application/x-bibtex; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=viitteet.bib"},
    )


def main():
    """Käynnistää sovelluksen."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
