# Vaatimusten tarkastus

Tähän tiedostoon on koottu kurssin vaatimukset ja se, miten ne toteutuvat
sovelluksessa. Vaatimukset on otettu kurssimateriaalin sivuilta
[Projektin aloitus](https://hy-tikawe.github.io/materiaali/aloitus/),
[Kurssin arvostelu](https://hy-tikawe.github.io/materiaali/arvostelu/) ja
[Tekninen tarkastuslista](https://hy-tikawe.github.io/materiaali/lista/).

## Sovelluksen perusvaatimukset (arvosana 3)

| Vaatimus | Toteutus |
| --- | --- |
| Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään | `app.py`: `/register`, `/login`, `/logout`; `users.py` |
| Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita | `/new_job`, `/job/<id>/edit`, `/job/<id>/remove`; `jobs.py` |
| Käyttäjä näkee sovellukseen lisätyt tietokohteet | etusivu `/` listaa kaikkien käyttäjien kohteet (vaatii kirjautumisen) |
| Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella | `/find`: hakusana ja luokitussuodatin; `jobs.find_jobs` |
| Käyttäjäsivu näyttää tilastoja ja käyttäjän lisäämät tietokohteet | `/user/<id>`; `users.get_stats` laskee tilastot SQL:llä |
| Tietokohteille on valittavissa useampia luokitteluja | kolme luokitteluryhmää (`Kohdetyyppi`, `Palvelu`, `Vaihe`), vaihtoehdot taulussa `classes`, monivalinta |
| Käyttäjä pystyy lisäämään toissijaisia tietokohteita omiin ja muiden kohteisiin | käynnit (`visits`), lomake kohteen sivulla, oikeus tarkistetaan kirjautumisella |

## Tekniset perusvaatimukset (arvosana 3)

| Vaatimus | Toteutus |
| --- | --- |
| Toteutettu kurssimateriaalin mukaisesti | rakenne kuten esimerkkisovelluksessa: `app.py`, `db.py`, `schema.sql`, `init.sql`, omat moduulit kyselyille |
| Python ja Flask | `app.py`, `requirements`: vain Flask |
| SQLite-tietokanta | `db.py`, tiedosto `database.db` |
| Gitiä ja GitHubia käytetty | tämä repositorio, commitit pienissä osissa |
| Käyttöliittymä HTML-sivuina | `templates/` |
| Ei JavaScriptiä | ei yhtään `<script>`-elementtiä eikä JS-tiedostoa |
| SQL suoraan, ei ORMia | kaikki kyselyt `db.query` / `db.execute` -funktioilla |
| Ei muita kirjastoja kuin Flask | `werkzeug` tulee Flaskin mukana, muita ei ole |
| Ulkoasu itse ilman kirjastoja | `static/main.css` on kokonaan oma |
| Koodi englanniksi | muuttujat, funktiot, taulut ja sarakkeet englanniksi |
| Taulut ja sarakkeet englanniksi | `users`, `jobs`, `classes`, `job_classes`, `visits` |

## Versionhallinta

| Vaatimus | Toteutus |
| --- | --- |
| `README.md` kertoo sovelluksesta ja testaamisesta | `README.md` |
| Commiteja säännöllisesti | commitit tehty ominaisuus kerrallaan |
| Commit-viestit englanniksi | kyllä |
| Ei ylimääräisiä tiedostoja | `.gitignore` sulkee pois `venv/`, `__pycache__/`, `database.db`, `.secret_key` |

## Turvallisuus

| Vaatimus | Toteutus |
| --- | --- |
| Salasanat tallennetaan asianmukaisesti | `werkzeug.security.generate_password_hash` (scrypt-tiiviste ja suola) |
| Sivun katsomisen oikeus tarkastetaan | `@login_required`-dekoraattori ohjaa kirjautumattoman kävijän kirjautumissivulle, joten kohteita ei näe ilman tunnusta; POST-reitit vastaavat 403; omistajuus tarkastetaan muokkauksessa ja poistossa |
| Lomakkeen lähettämisen oikeus tarkastetaan | `check_csrf` sekä omistajuuden tarkastus palvelimella, ei piilokenttien varassa |
| Syötteet tarkastetaan ennen tallennusta | `read_job_form` ja `add_visit` tarkastavat pituudet, kokonaisluvut ja luokitusten olemassaolon |
| SQL-komennoissa parametrit | kaikki arvot `?`-parametreina, ei merkkijonojen yhdistelyä arvojen kanssa |
| Sivut sivupohjien kautta | kaikki sivut `render_template`-kutsulla |
| CSRF-aukko estetty | istuntokohtainen `csrf_token` jokaisessa lomakkeessa ja `check_csrf` jokaisessa POST-reitissä |

## Lisävaatimukset (arvosana 4)

| Vaatimus | Toteutus |
| --- | --- |
| Sovellusta helppoa ja loogista käyttää | yhtenäinen valikko, lomakkeissa nimetyt kentät ja ohjeet, muutosten jälkeen ilmoitus ja ohjaus |
| CSS:llä toteutettu ulkoasu | `static/main.css`, ei CSS-kirjastoa |
| Ei versionhallintaan kuulumattomia tiedostoja | `.gitignore` |
| Commitit hyviä kokonaisuuksia | ominaisuus per commit |
| Muuttujat ja funktiot nimetty kuvaavasti | esim. `window_count`, `job_classes`, `get_stats` |
| Sisennys neljä välilyöntiä | koko koodi |
| Ei liian pitkiä rivejä | rivit alle 80 merkin |
| Nimet muotoa `total_count` | snake_case |
| Välit `=` ja `,` -merkkien ympärillä | noudatettu |
| Ei ylimääräisiä sulkeita `if`-rakenteissa | ei käytetä |
| Ei käyttämättömiä funktioita tai moduuleja | Pylint-raportissa ei ole `unused-import`- tai `unused-variable`-ilmoituksia |
| Taulut ja sarakkeet nimetty kuvaavasti | kyllä |
| `REFERENCES` viittauksissa | `jobs.user_id`, `job_classes.*`, `visits.*` |
| Ei `SELECT *` -kyselyitä | kaikissa kyselyissä sarakkeet listattu |
| SQL:n ominaisuuksia käytetty järkevästi | `GROUP BY`, `LEFT JOIN`, korreloivat alikyselyt tilastoissa, `LIMIT`/`OFFSET` sivuituksessa |

## Lisävaatimukset (arvosana 5)

| Vaatimus | Toteutus |
| --- | --- |
| Pylint-raportti ja selostus jokaisesta ilmoituksesta | `pylint-report.md` |
| Rivinvaihdot näkyvät selaimessa | `show_lines`-suodatin kuvausta ja muistiinpanoja varten |
| Kuvien `alt`-attribuutit | sovelluksessa ei ole kuvia |
| Lomakkeiden `label`-elementit | kaikissa lomakkeissa |
| Testattu suurella tietomäärällä ja tulokset raportoitu | `seed.py` ja `README.md`: 100 000 kohdetta |
| Kohteiden sivutus | etusivu, haku ja profiilisivu |
| Indeksi nopeuttamaan suurta tietomäärää | `jobs(user_id)` ja `visits(user_id)`, mittaukset `README.md`:ssä |

## Kurssin ulkopuoliset asiat

Vertaisarvioinnit ja kurssipalaute annetaan Labtoolissa, eivät tässä
repositoriossa.
