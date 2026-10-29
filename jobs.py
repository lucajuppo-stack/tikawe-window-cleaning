import db


def get_classes():
    sql = "SELECT id, title, value FROM classes ORDER BY id"
    rows = db.query(sql)
    groups = {}
    for row in rows:
        groups.setdefault(row["title"], []).append(row)
    return groups


def get_class(class_id):
    sql = "SELECT id, title, value FROM classes WHERE id = ?"
    result = db.query(sql, [class_id])
    return result[0] if result else None


def get_job(job_id):
    sql = """SELECT j.id, j.title, j.address, j.window_count, j.price,
                    j.description, u.id AS user_id, u.username
             FROM jobs j, users u
             WHERE j.id = ? AND j.user_id = u.id"""
    result = db.query(sql, [job_id])
    return result[0] if result else None


def get_job_classes(job_id):
    sql = """SELECT c.id, c.title, c.value
             FROM classes c, job_classes jc
             WHERE jc.job_id = ? AND c.id = jc.class_id
             ORDER BY c.id"""
    return db.query(sql, [job_id])


def count_jobs():
    sql = "SELECT COUNT(*) AS total FROM jobs"
    return db.query(sql)[0]["total"]


def count_jobs_by_user(user_id):
    sql = "SELECT COUNT(*) AS total FROM jobs WHERE user_id = ?"
    return db.query(sql, [user_id])[0]["total"]


def get_jobs(page, per_page):
    sql = """SELECT j.id, j.title, j.address, j.window_count, j.price,
                    u.id AS user_id, u.username
             FROM jobs j, users u
             WHERE j.user_id = u.id
             ORDER BY j.id DESC
             LIMIT ? OFFSET ?"""
    return db.query(sql, [per_page, (page - 1) * per_page])


def get_jobs_by_user(user_id, page, per_page):
    sql = """SELECT j.id, j.title, j.address, j.window_count, j.price,
                    u.id AS user_id, u.username
             FROM jobs j, users u
             WHERE j.user_id = u.id AND j.user_id = ?
             ORDER BY j.id DESC
             LIMIT ? OFFSET ?"""
    return db.query(sql, [user_id, per_page, (page - 1) * per_page])


def find_jobs(query_text, class_id, page, per_page):
    # The WHERE clause is built from fixed fragments and all user input is
    # passed as query parameters.
    conditions = []
    params = []
    if query_text:
        pattern = "%" + query_text + "%"
        conditions.append(
            "(j.title LIKE ? OR j.address LIKE ? OR j.description LIKE ?)")
        params.extend([pattern, pattern, pattern])
    if class_id:
        conditions.append(
            "j.id IN (SELECT job_id FROM job_classes WHERE class_id = ?)")
        params.append(class_id)
    if conditions:
        where = " AND ".join(conditions)
    else:
        where = "1 = 1"

    count_sql = """SELECT COUNT(*) AS total
                   FROM jobs j, users u
                   WHERE j.user_id = u.id AND """ + where
    total = db.query(count_sql, params)[0]["total"]

    sql = """SELECT j.id, j.title, j.address, j.window_count, j.price,
                    u.id AS user_id, u.username
             FROM jobs j, users u
             WHERE j.user_id = u.id AND """ + where + """
             ORDER BY j.id DESC
             LIMIT ? OFFSET ?"""
    results = db.query(sql, params + [per_page, (page - 1) * per_page])
    return results, total


def add_job(title, address, window_count, price, description, user_id,
            class_ids):
    sql = """INSERT INTO jobs (title, address, window_count, price,
                               description, user_id)
             VALUES (?, ?, ?, ?, ?, ?)"""
    params = [title, address, window_count, price, description, user_id]
    db.execute(sql, params)
    job_id = db.last_insert_id()
    add_job_classes(job_id, class_ids)
    return job_id


def add_job_classes(job_id, class_ids):
    sql = "INSERT INTO job_classes (job_id, class_id) VALUES (?, ?)"
    params = [[job_id, class_id] for class_id in class_ids]
    db.execute_many(sql, params)


def update_job(job_id, title, address, window_count, price, description,
               class_ids):
    sql = """UPDATE jobs
             SET title = ?, address = ?, window_count = ?, price = ?,
                 description = ?
             WHERE id = ?"""
    db.execute(sql, [title, address, window_count, price, description, job_id])
    db.execute("DELETE FROM job_classes WHERE job_id = ?", [job_id])
    add_job_classes(job_id, class_ids)


def remove_job(job_id):
    db.execute("DELETE FROM visits WHERE job_id = ?", [job_id])
    db.execute("DELETE FROM job_classes WHERE job_id = ?", [job_id])
    db.execute("DELETE FROM jobs WHERE id = ?", [job_id])
