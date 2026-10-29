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
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:50:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:62:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:68:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:73:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:84:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:84:0: R0911: Too many return statements (10/6) (too-many-return-statements)
app.py:122:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:131:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:144:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:164:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:178:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:206:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:229:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:238:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:265:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:305:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:326:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:355:0: C0116: Missing function or method docstring (missing-function-docstring)
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
jobs.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:66:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:100:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:100:0: R0913: Too many arguments (7/5) (too-many-arguments)
jobs.py:100:0: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
jobs.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:118:0: C0116: Missing function or method docstring (missing-function-docstring)
jobs.py:118:0: R0913: Too many arguments (7/5) (too-many-arguments)
jobs.py:118:0: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
jobs.py:129:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:50:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module visits
visits.py:1:0: C0114: Missing module docstring (missing-module-docstring)
visits.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
visits.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
visits.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
visits.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
visits.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:52:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.57/10 (previous run: 8.56/10, +0.01)
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

### `too-many-return-statements` (R0911)

Ilmoitus tulee funktiosta `read_job_form`, joka tarkastaa lomakkeen kentät
yksi kerrallaan ja palauttaa `None`, jos jokin tarkastus ei mene läpi.
Varhaiset paluut pitävät tarkastukset tasaisena listana ilman sisäkkäisiä
ehtolauseita, ja funktion kutsuja käsittelee kaikki virheet samalla tavalla.
Tarkastukset voisi koota silmukaksi, mutta silloin jokainen kenttä tarvitsisi
oman tarkastusfunktionsa ja koodista tulisi vaikeammin luettavaa.
