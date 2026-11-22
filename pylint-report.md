# Pylint-raportti

Raportti on tehty sovelluksen lopullisesta versiosta. Pylint ajettiin
virtuaaliympäristössä komennolla:

```console
$ pylint app.py config.py db.py jobs.py users.py visits.py seed.py
```

Pylint antoi seuraavan tulosteen:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:53:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:74:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:90:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:94:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:101:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:181:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:191:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:205:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:226:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:240:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:268:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:291:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:301:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:322:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:355:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:375:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:404:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module jobs
jobs.py:1:0: C0114: Missing module docstring (missing-module-docstring)
jobs.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:69:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:103:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:103:0: R0913: Too many arguments (7/5) (too-many-arguments)
jobs.py:103:0: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
jobs.py:115:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:121:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:121:0: R0913: Too many arguments (7/5) (too-many-arguments)
jobs.py:121:0: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
jobs.py:132:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:40:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module visits
visits.py:1:0: C0114: Missing module docstring (missing-module-docstring)
visits.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
visits.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
visits.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
visits.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:52:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.70/10 (previous run: 8.70/10, +0.00)
```

## Ilmoitukset ja miksi niitä ei ole korjattu

### `missing-function-docstring` (C0116) ja `missing-module-docstring` (C0114)

Suurin osa ilmoituksista koskee puuttuvia docstringejä. Funktiot ovat lyhyitä
ja nimetty kuvaavasti (`get_job`, `count_jobs_by_user`, `check_login`), ja
jokaisen funktion ydin on yksi luettava SQL-kysely tai muutama rivi
tarkastuksia, joten docstring toistaisi käytännössä funktion nimen. Kurssin
esimerkkisovellus on kirjoitettu samalla tavalla ilman docstringejä, ja
sovellus on tarkoitus pitää saman tyylisenä kuin kurssimateriaali. Jos
sovelluksesta tehtäisiin kirjasto tai siihen liitettäisiin laajempi
rajapinta, docstringit olisi syytä lisätä.

### `too-many-arguments` (R0913) ja `too-many-positional-arguments` (R0917)

Ilmoitukset tulevat funktioista `jobs.add_job` ja `jobs.update_job`, joilla on
seitsemän parametria. Parametrit vastaavat suoraan kohteen lomakkeen kenttiä,
ja ne välitetään sellaisenaan SQL-komennon parametrilistaksi. Arvot voisi
koota sanakirjaan, mutta silloin SQL-kyselyn ja lomakkeen välinen yhteys
muuttuisi epäselvemmäksi ja parametrisoitu kysely vaatisi erillistä
sovitusta. Seitsemän parametria on tässä selkeämpi ratkaisu.

### Lomakkeen tarkastus

Lomakkeen tarkastus (`read_job_form`) kerää virheet sanakirjaan sen sijaan,
että se palauttaisi `None` jokaisesta virheellisestä kentästä erikseen.
Ratkaisu poisti aiemman `too-many-return-statements`-ilmoituksen, ja samalla
jokainen virheellinen kenttä saa oman viestinsä sen sijaan, että kaikki
virheet näytettäisiin samana "tarkista lomakkeen tiedot" -ilmoituksena.
