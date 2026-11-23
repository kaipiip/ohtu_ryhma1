# Ohjelmistotuotannon(JYU) 2026 kurssin miniprojekti ryhmä 1

### Lokaali selainsovellus lähdeviitteiden hallintaan LaTeX:illa.  
Käyttäjä voi tallentaa itselleen lähdeviitteitä selaimessa toimivalla lomakkeella. Viitteistä generoidaan LaTeX-dokumenttiin sopiva BibTeX-muotoinen tiedosto sekä listataan sivulle normaali luettavissa oleva lähdeluettelo.  

[Backlog](https://docs.google.com/spreadsheets/d/1NC18eR8eowJH83STexgb_yyQtPaERxYVcjvT9R7wCc0/edit?usp=sharing)

CI: [GitHub Actions](https://github.com/kaipiip/ohtu_ryhma1/actions)

Lisenssi: [MIT](LICENSE.txt)

## Definition of Done
User story on valmis, kun:
- hyväksymiskriteerit täyttyvät
- toiminnallisuudella on yksikkötestit, ja CI on vihreä
- koodi läpäisee pylintin
- muutos on katselmoitu pull requestissa ja yhdistetty mainiin

## Asennus ja käyttö
1. Kloonaa repositorio ja siirry projektikansioon
2. Asenna riippuvuudet: `uv sync`
3. Käynnistä sovellus: `uv run python src/main.py`
4. Avaa selaimessa http://127.0.0.1:5000
