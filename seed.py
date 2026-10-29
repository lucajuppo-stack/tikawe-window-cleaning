"""Generate a large amount of test data for performance measurements.

Usage:
    python3 seed.py [number_of_jobs]

The script expects a database created with schema.sql and init.sql. The
default number of jobs is 100000, which is enough to see the effect of
pagination and of the indexes defined in schema.sql.
"""
import random
import sys
import time

from werkzeug.security import generate_password_hash

import db

DEFAULT_JOBS = 100000
BATCH_SIZE = 5000
SALES_REPS = 20
SEED_PASSWORD = "salasana123"

CITIES = ["Helsinki", "Espoo", "Vantaa", "Tampere", "Turku", "Oulu",
          "Jyväskylä", "Lahti", "Kuopio", "Pori"]
STREETS = ["Koulukatu", "Rantatie", "Puistokuja", "Asemakatu", "Kirkkotie",
           "Metsäpolku", "Satamakatu", "Koulutie", "Puutarhakatu",
           "Rautatienkatu"]
COMPANIES = ["Asunto Oy", "Kiinteistö Oy", "Koulu", "Kirjasto", "Liikekeskus",
             "Päiväkoti", "Toimisto"]
DESCRIPTIONS = [
    "Kerrostalo, ikkunat kolmessa kerroksessa.",
    "Rivitalo, ikkunat ja parvekelasit samalla käynnillä.",
    "Liikekiinteistö, isot näyteikkunat kadun puolella.\n"
    "Pesu ennen kello 9.",
    "Koulurakennus, ikkunat kahdessa kerroksessa ja lasiseinä.",
]


def create_sales_reps(con):
    existing = {row[0] for row in con.execute("SELECT username FROM users")}
    params = []
    for index in range(1, SALES_REPS + 1):
        username = f"myyja_{index:02d}"
        if username not in existing:
            params.append([username, generate_password_hash(SEED_PASSWORD)])
    con.executemany(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)", params)
    return [row[0] for row in con.execute(
        "SELECT id FROM users ORDER BY id LIMIT ?", [SALES_REPS])]


def get_class_ids(con):
    return [row[0] for row in con.execute("SELECT id FROM classes")]


def create_jobs(con, job_count, user_ids):
    rows = []
    for _ in range(job_count):
        street = random.choice(STREETS)
        rows.append([
            f"{random.choice(COMPANIES)} {street} {random.randint(1, 120)}",
            f"{street} {random.randint(1, 120)}, {random.choice(CITIES)}",
            random.randint(4, 400),
            random.randint(80, 9000),
            random.choice(DESCRIPTIONS),
            random.choice(user_ids),
        ])
        if len(rows) == BATCH_SIZE:
            con.executemany(
                "INSERT INTO jobs (title, address, window_count, price,"
                " description, user_id) VALUES (?, ?, ?, ?, ?, ?)", rows)
            rows = []
    if rows:
        con.executemany(
            "INSERT INTO jobs (title, address, window_count, price,"
            " description, user_id) VALUES (?, ?, ?, ?, ?, ?)", rows)


def create_job_classes(con, min_id, max_id, class_ids):
    params = []
    sql = "INSERT INTO job_classes (job_id, class_id) VALUES (?, ?)"
    for job_id in range(min_id, max_id + 1):
        for class_id in random.sample(class_ids, random.randint(1, 3)):
            params.append([job_id, class_id])
        if len(params) >= BATCH_SIZE:
            con.executemany(sql, params)
            params = []
    if params:
        con.executemany(sql, params)


def create_visits(con, min_id, max_id, user_ids):
    params = []
    sql = """INSERT INTO visits (job_id, user_id, visit_date, notes)
             VALUES (?, ?, ?, ?)"""
    for job_id in range(min_id, max_id + 1):
        if random.random() < 0.5:
            continue
        for _ in range(random.randint(1, 2)):
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            params.append([job_id, random.choice(user_ids),
                           f"2026-{month:02d}-{day:02d}",
                           "Pesu sovittu ja suoritettu."])
        if len(params) >= BATCH_SIZE:
            con.executemany(sql, params)
            params = []
    if params:
        con.executemany(sql, params)


def main():
    job_count = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_JOBS
    random.seed(2026)
    con = db.get_connection()

    start = time.time()
    user_ids = create_sales_reps(con)
    all_class_ids = get_class_ids(con)
    before = con.execute("SELECT COALESCE(MAX(id), 0) FROM jobs").fetchone()[0]

    create_jobs(con, job_count, user_ids)
    after = con.execute("SELECT COALESCE(MAX(id), 0) FROM jobs").fetchone()[0]
    create_job_classes(con, before + 1, after, all_class_ids)
    create_visits(con, before + 1, after, user_ids)
    con.commit()

    elapsed = time.time() - start
    totals = []
    for table in ("users", "jobs", "job_classes", "visits"):
        count = con.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]
        totals.append(f"{table}: {count}")
    con.close()

    print(", ".join(totals))
    print(f"seeding took {elapsed:.1f} seconds")


if __name__ == "__main__":
    main()
