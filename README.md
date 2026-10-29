# Ikkunanpesujen seuranta

Harjoitustyö kurssille [Tietokannat ja web-ohjelmointi](https://hy-tikawe.github.io/materiaali/)
(Helsingin yliopisto).

Sovellus on ikkunanpesuyrityksen työkalu. Yrityksen myyntiedustajat kirjaavat
sovellukseen asiakaskohteita (ikkunanpesutilauksia) ja käyntejä, jotka
liittyvät kohteisiin. Kohteita voi selata, hakea ja luokitella, ja jokaisella
myyntiedustajalla on oma profiilisivu tilastoineen.

Sovellus on toteutettu Pythonilla ja Flaskilla, tietokantana on SQLite.
Tietokantaa käytetään suoraan SQL-komennoilla ja kaikki HTML ja CSS on
kirjoitettu itse. Sovelluksessa ei ole JavaScriptiä eikä Flaskin lisäksi muita
erikseen asennettavia kirjastoja.

## Ominaisuudet

- **Tunnukset ja kirjautuminen**: käyttäjä luo tunnuksen ja kirjautuu sisään.
  Tunnus toimii myyntiedustajan profiilina. Salasanat tallennetaan tiivistettyinä.
- **Kohteet**: kirjautunut käyttäjä voi lisätä, muokata ja poistaa omia
  kohteitaan. Kaikki käyttäjät näkevät kaikkien kohteiden listan etusivulla.
  Kohde sisältää asiakkaan nimen, osoitteen, ikkunoiden määrän, hinnan ja
  kuvauksen.
- **Luokittelut**: kohteelle valitaan luokitteluja kolmesta ryhmästä
  (*Kohdetyyppi*, *Palvelu*, *Vaihe*). Luokittelut on määritelty tietokannan
  taulussa `classes`, ja jokaisesta ryhmästä voi valita useita vaihtoehtoja.
- **Haku**: kohteita voi hakea hakusanalla (asiakas, osoite tai kuvaus) ja
  suodattaa luokituksen perusteella. Haku kohdistuu kaikkien käyttäjien
  kohteisiin.
- **Käynnit**: käynti on toissijainen tietokohde, joka täydentää kohdetta.
  Kuka tahansa kirjautunut käyttäjä voi kirjata käynnin sekä omiin että muiden
  kohteisiin. Käynnin voi poistaa vain sen kirjannut käyttäjä.
- **Käyttäjäsivu**: profiilisivu näyttää tilastot (kohteiden määrä, käyntien
  määrä, kohteiden yhteenlaskettu hinta ja ikkunoiden määrä) sekä käyttäjän
  lisäämät kohteet.
- **Sivutus**: kohdelistat, hakutulokset ja profiilisivun kohdelista on
  sivutettu (20 kohdetta sivulla).

## Tietokannan rakenne

| Taulu | Sisältö |
| --- | --- |
| `users` | myyntiedustajat: tunnus ja salasanan tiiviste |
| `jobs` | kohteet: asiakas, osoite, ikkunoiden määrä, hinta, kuvaus, omistaja |
| `classes` | luokittelujen vaihtoehdot: ryhmän nimi (`title`) ja arvo (`value`) |
| `job_classes` | liitostaulu kohteen ja luokituksen välillä |
| `visits` | käynnit: kohde, kirjaaja, päivämäärä ja muistiinpano |

Tietokannassa on viiteavaimet (`REFERENCES`) ja `UNIQUE`-määreet sekä indeksit
`jobs(user_id)`, `jobs(title)`, `job_classes(job_id)`, `visits(job_id)` ja
`visits(user_id)`.

## Asennus ja käynnistys

```console
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install flask
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
$ flask run
```

Jos `sqlite3`-komentorivityökalua ei ole asennettu, saman voi tehdä
Pythonilla:

```console
$ python3 -c "import sqlite3; c = sqlite3.connect('database.db'); \
c.executescript(open('schema.sql').read()); \
c.executescript(open('init.sql').read()); c.commit()"
```

Sovellus käynnistyy osoitteeseen http://127.0.0.1:5000.

Salasanatiivisteiden salaisuus (`config.py`) luodaan ensimmäisellä
käynnistyskerralla tiedostoon `.secret_key`, joka ei ole versionhallinnassa.
`database.db` luodaan yllä olevilla komennoilla eikä sekään ole
versionhallinnassa.

## Testaaminen

1. Luo tunnus sivulla *Luo tunnus* (esim. `myyja_01` / `salasana123`).
2. Kirjaudu sisään ja lisää kohde valitsemalla vähintään yksi luokittelu.
3. Kokeile etusivun listaa, hakua (*Etsi*), kohteen muokkaamista ja
   poistamista sekä käynnin kirjaamista.
4. Luo toinen tunnus ja kirjaa käynti ensimmäisen käyttäjän kohteeseen.
5. Katso profiilisivu (*Oma profiili*) ja sen tilastot.

Valmiiksi täytetyn tietokannan saa myös `seed.py`-skriptillä, joka luo 20
myyntiedustajaa (tunnus `myyja_01` … `myyja_20`, salasana `salasana123`)
ja suuren määrän kohteita:

```console
$ python3 seed.py 100000
```

## Suuri tietomäärä

Sovellusta on testattu 100 000 kohteella. Tietokanta luotiin tiedostoilla
`schema.sql` ja `init.sql`, minkä jälkeen data luotiin komennolla
`python3 seed.py 100000`:

```console
users: 20, jobs: 100000, job_classes: 200233, visits: 75124
seeding took 4.3 seconds
```

Mittaukset tehtiin samalla koneella (Python 3.12.14, SQLite 3.53.1) Flaskin
testiasiakkaalla, jokaisesta pyynnöstä otettiin viiden ajon nopein.

| Pyyntö | Aika |
| --- | --- |
| etusivu, sivu 1 | 1,8 ms |
| etusivu, sivu 5000 (OFFSET 99980) | 17,2 ms |
| kohteen sivu | 1,1 ms |
| profiilisivu (5 tilastokyselyä) | 11,1 ms |
| haku hakusanalla | 40,6 ms |
| haku luokituksella | 38,5 ms |
| haku, ei osumia (koko taulu läpi) | 50,9 ms |

Indeksien vaikutus yksittäisiin kyselyihin:

| Kysely | indeksillä | ilman indeksiä |
| --- | --- | --- |
| yhden käyttäjän kohteiden määrä | 0,15 ms | 9,0 ms |
| profiilisivun tilastot | 7,6 ms | 29,9 ms |
| käyttäjien kohteiden laskenta (`GROUP BY`) | 80 ms | 107 ms |

Indeksi `jobs(user_id)` nopeuttaa yhden käyttäjän kohteiden laskentaa noin
60-kertaisesti ja indeksi `visits(user_id)` profiilisivun tilastoja noin
nelinkertaisesti. Hakusanahaku käyttää `LIKE`-ehtoa muodossa `%sana%`, johon
indeksi ei voi auttaa, joten haku käy taulun läpi. Sivutus pitää hakujen
tulokset pieninä: syvinkin sivu palautetaan noin 17 millisekunnissa, koska
`LIMIT`- ja `OFFSET`-ehdot rajaavat palautettavan aineiston.

## Tiedostot

| Tiedosto | Tehtävä |
| --- | --- |
| `app.py` | reitit, lomakkeiden tarkastus ja CSRF-tarkastus |
| `config.py` | istuntojen salainen avain |
| `db.py` | tietokantayhteydet ja kyselyjen suorittaminen |
| `jobs.py` | kohteisiin ja luokitteluihin liittyvät SQL-kyselyt |
| `users.py` | käyttäjiin ja tilastoihin liittyvät SQL-kyselyt |
| `visits.py` | käynteihin liittyvät SQL-kyselyt |
| `schema.sql` | tietokannan rakenne ja indeksit |
| `init.sql` | luokittelujen vaihtoehdot |
| `seed.py` | suuren testiaineiston luonti |
| `templates/` | sivupohjat |
| `static/main.css` | ulkoasu |
| `pylint-report.md` | Pylint-raportti |

Tekninen tarkastuslista on käyty läpi tiedostossa
[docs/vaatimukset.md](docs/vaatimukset.md).
