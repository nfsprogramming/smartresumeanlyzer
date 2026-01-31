CREATE TABLE IF NOT EXISTS job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT DEFAULT 'Applied', -- Applied, Interviewing, Offer, Rejected
    date_applied TEXT,
    ats_score INTEGER,
    resume_version_id INTEGER,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS resume_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_name TEXT,
    content TEXT,
    created_at TEXT,
    parent_version_id INTEGER
);
