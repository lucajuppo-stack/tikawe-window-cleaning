import db


def get_visits(job_id):
    sql = """SELECT v.id, v.visit_date, v.notes,
                    u.id AS user_id, u.username
             FROM visits v, users u
             WHERE v.job_id = ? AND v.user_id = u.id
             ORDER BY v.visit_date DESC, v.id DESC"""
    return db.query(sql, [job_id])


def get_visit(visit_id):
    sql = """SELECT id, job_id, user_id, visit_date, notes
             FROM visits
             WHERE id = ?"""
    result = db.query(sql, [visit_id])
    return result[0] if result else None


def add_visit(job_id, user_id, visit_date, notes):
    sql = """INSERT INTO visits (job_id, user_id, visit_date, notes)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [job_id, user_id, visit_date, notes])


def remove_visit(visit_id):
    db.execute("DELETE FROM visits WHERE id = ?", [visit_id])
