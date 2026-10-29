CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    address TEXT NOT NULL,
    window_count INTEGER NOT NULL,
    price INTEGER NOT NULL,
    description TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    value TEXT NOT NULL,
    UNIQUE (title, value)
);

CREATE TABLE job_classes (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs,
    class_id INTEGER NOT NULL REFERENCES classes,
    UNIQUE (job_id, class_id)
);

CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs,
    user_id INTEGER NOT NULL REFERENCES users,
    visit_date TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE INDEX idx_jobs_user_id ON jobs (user_id);
CREATE INDEX idx_jobs_title ON jobs (title);
CREATE INDEX idx_job_classes_job_id ON job_classes (job_id);
CREATE INDEX idx_visits_job_id ON visits (job_id);
CREATE INDEX idx_visits_user_id ON visits (user_id);
