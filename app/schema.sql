CREATE TABLE IF NOT EXISTS exercise (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    name_key TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS template_version (
    id INTEGER PRIMARY KEY,
    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    valid_from TEXT NOT NULL,
    is_rest INTEGER NOT NULL DEFAULT 0,
    UNIQUE (weekday, valid_from)
);

CREATE TABLE IF NOT EXISTS template_item (
    id INTEGER PRIMARY KEY,
    template_version_id INTEGER NOT NULL REFERENCES template_version (id),
    exercise_id INTEGER NOT NULL REFERENCES exercise (id) ON DELETE RESTRICT,
    position INTEGER NOT NULL,
    planned_sets INTEGER NOT NULL CHECK (planned_sets > 0),
    planned_reps INTEGER NOT NULL CHECK (planned_reps > 0),
    UNIQUE (template_version_id, exercise_id)
);

CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    template_weekday INTEGER NOT NULL CHECK (template_weekday BETWEEN 0 AND 6),
    note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (date, template_weekday)
);

CREATE TABLE IF NOT EXISTS session_set (
    id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES session (id),
    exercise_id INTEGER NOT NULL REFERENCES exercise (id) ON DELETE RESTRICT,
    set_number INTEGER NOT NULL CHECK (set_number > 0),
    weight_kg REAL NOT NULL CHECK (weight_kg >= 0),
    reps INTEGER NOT NULL CHECK (reps > 0),
    UNIQUE (session_id, exercise_id, set_number)
);
