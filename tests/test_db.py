import sqlite3

import pytest

from app import db


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "gym-test.db"
    db.init_db(path)
    return path


@pytest.fixture
def connection(db_path):
    conn = db.connect(db_path)
    yield conn
    conn.close()


def add_exercise(conn, name="Press de banca", name_key=None):
    if name_key is None:
        name_key = name.lower()
    cursor = conn.execute(
        "INSERT INTO exercise (name, name_key) VALUES (?, ?)",
        (name, name_key),
    )
    return cursor.lastrowid


def add_template_version(conn, weekday=0, valid_from="2026-01-05", is_rest=0):
    cursor = conn.execute(
        "INSERT INTO template_version (weekday, valid_from, is_rest) VALUES (?, ?, ?)",
        (weekday, valid_from, is_rest),
    )
    return cursor.lastrowid


def add_template_item(
    conn,
    template_version_id,
    exercise_id,
    position=1,
    planned_sets=3,
    planned_reps=10,
):
    cursor = conn.execute(
        """
        INSERT INTO template_item
            (template_version_id, exercise_id, position, planned_sets, planned_reps)
        VALUES (?, ?, ?, ?, ?)
        """,
        (template_version_id, exercise_id, position, planned_sets, planned_reps),
    )
    return cursor.lastrowid


def add_session(conn, date="2026-01-05", template_weekday=0, note=None):
    cursor = conn.execute(
        "INSERT INTO session (date, template_weekday, note) VALUES (?, ?, ?)",
        (date, template_weekday, note),
    )
    return cursor.lastrowid


def add_session_set(
    conn,
    session_id,
    exercise_id,
    set_number=1,
    weight_kg=20.0,
    reps=10,
):
    cursor = conn.execute(
        """
        INSERT INTO session_set
            (session_id, exercise_id, set_number, weight_kg, reps)
        VALUES (?, ?, ?, ?, ?)
        """,
        (session_id, exercise_id, set_number, weight_kg, reps),
    )
    return cursor.lastrowid


# --- Esquema y conexión -----------------------------------------------------


def test_schema_version_is_set(connection):
    assert connection.execute("PRAGMA user_version").fetchone()[0] == 1


def test_all_tables_are_created(connection):
    names = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    assert {
        "exercise",
        "template_version",
        "template_item",
        "session",
        "session_set",
    } <= names


def test_foreign_keys_are_enabled_on_every_connection(db_path):
    first = db.connect(db_path)
    second = db.connect(db_path)
    try:
        assert first.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert second.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    finally:
        first.close()
        second.close()


# --- Restricciones de valores ----------------------------------------------


def test_weight_must_be_non_negative(connection):
    exercise_id = add_exercise(connection)
    session_id = add_session(connection)

    with pytest.raises(sqlite3.IntegrityError):
        add_session_set(connection, session_id, exercise_id, weight_kg=-0.1)


def test_zero_weight_is_allowed(connection):
    exercise_id = add_exercise(connection)
    session_id = add_session(connection)

    add_session_set(connection, session_id, exercise_id, weight_kg=0)

    count = connection.execute("SELECT COUNT(*) FROM session_set").fetchone()[0]
    assert count == 1


def test_reps_must_be_positive(connection):
    exercise_id = add_exercise(connection)
    session_id = add_session(connection)

    with pytest.raises(sqlite3.IntegrityError):
        add_session_set(connection, session_id, exercise_id, reps=0)


def test_set_number_must_be_positive(connection):
    exercise_id = add_exercise(connection)
    session_id = add_session(connection)

    with pytest.raises(sqlite3.IntegrityError):
        add_session_set(connection, session_id, exercise_id, set_number=0)


@pytest.mark.parametrize("field", ["planned_sets", "planned_reps"])
def test_planned_values_must_be_positive(connection, field):
    version_id = add_template_version(connection)
    exercise_id = add_exercise(connection)

    with pytest.raises(sqlite3.IntegrityError):
        add_template_item(connection, version_id, exercise_id, **{field: 0})


@pytest.mark.parametrize("weekday", [-1, 7])
def test_template_version_weekday_must_be_between_0_and_6(connection, weekday):
    with pytest.raises(sqlite3.IntegrityError):
        add_template_version(connection, weekday=weekday)


@pytest.mark.parametrize("weekday", [-1, 7])
def test_session_template_weekday_must_be_between_0_and_6(connection, weekday):
    with pytest.raises(sqlite3.IntegrityError):
        add_session(connection, template_weekday=weekday)


@pytest.mark.parametrize("weekday", [0, 6])
def test_weekday_bounds_are_accepted(connection, weekday):
    add_template_version(connection, weekday=weekday)
    add_session(connection, template_weekday=weekday)

    assert connection.execute("SELECT COUNT(*) FROM template_version").fetchone()[0] == 1
    assert connection.execute("SELECT COUNT(*) FROM session").fetchone()[0] == 1


# --- Restricciones de unicidad ---------------------------------------------


def test_exercise_name_key_must_be_unique(connection):
    add_exercise(connection, name="Press de banca", name_key="press de banca")

    with pytest.raises(sqlite3.IntegrityError):
        add_exercise(connection, name="PRESS DE BANCA", name_key="press de banca")


def test_template_version_is_unique_per_weekday_and_valid_from(connection):
    add_template_version(connection, weekday=1, valid_from="2026-01-06")

    with pytest.raises(sqlite3.IntegrityError):
        add_template_version(connection, weekday=1, valid_from="2026-01-06")


def test_same_weekday_with_different_valid_from_is_allowed(connection):
    add_template_version(connection, weekday=1, valid_from="2026-01-06")
    add_template_version(connection, weekday=1, valid_from="2026-01-13")

    count = connection.execute("SELECT COUNT(*) FROM template_version").fetchone()[0]
    assert count == 2


def test_template_item_is_unique_per_version_and_exercise(connection):
    version_id = add_template_version(connection)
    exercise_id = add_exercise(connection)
    add_template_item(connection, version_id, exercise_id)

    with pytest.raises(sqlite3.IntegrityError):
        add_template_item(connection, version_id, exercise_id, position=2)


def test_session_is_unique_per_date_and_template_weekday(connection):
    add_session(connection, date="2026-01-05", template_weekday=0)

    with pytest.raises(sqlite3.IntegrityError):
        add_session(connection, date="2026-01-05", template_weekday=0)


def test_same_date_with_different_template_weekday_is_allowed(connection):
    add_session(connection, date="2026-01-05", template_weekday=0)
    add_session(connection, date="2026-01-05", template_weekday=1)

    count = connection.execute("SELECT COUNT(*) FROM session").fetchone()[0]
    assert count == 2


def test_session_set_is_unique_per_session_exercise_and_number(connection):
    exercise_id = add_exercise(connection)
    session_id = add_session(connection)
    add_session_set(connection, session_id, exercise_id, set_number=1)

    with pytest.raises(sqlite3.IntegrityError):
        add_session_set(connection, session_id, exercise_id, set_number=1)


def test_same_set_number_for_another_exercise_is_allowed(connection):
    first_exercise = add_exercise(connection, name="Press de banca")
    second_exercise = add_exercise(connection, name="Remo con barra")
    session_id = add_session(connection)

    add_session_set(connection, session_id, first_exercise, set_number=1)
    add_session_set(connection, session_id, second_exercise, set_number=1)

    count = connection.execute("SELECT COUNT(*) FROM session_set").fetchone()[0]
    assert count == 2


# --- Integridad referencial -------------------------------------------------


def test_foreign_key_blocks_unknown_exercise(connection):
    version_id = add_template_version(connection)

    with pytest.raises(sqlite3.IntegrityError):
        add_template_item(connection, version_id, exercise_id=999)


def test_exercise_used_by_a_template_cannot_be_deleted(connection):
    version_id = add_template_version(connection)
    exercise_id = add_exercise(connection)
    add_template_item(connection, version_id, exercise_id)

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute("DELETE FROM exercise WHERE id = ?", (exercise_id,))


def test_exercise_used_by_a_session_cannot_be_deleted(connection):
    exercise_id = add_exercise(connection)
    session_id = add_session(connection)
    add_session_set(connection, session_id, exercise_id)

    with pytest.raises(sqlite3.IntegrityError):
        connection.execute("DELETE FROM exercise WHERE id = ?", (exercise_id,))


def test_unused_exercise_can_be_deleted(connection):
    exercise_id = add_exercise(connection)

    connection.execute("DELETE FROM exercise WHERE id = ?", (exercise_id,))

    count = connection.execute("SELECT COUNT(*) FROM exercise").fetchone()[0]
    assert count == 0


# --- Persistencia -----------------------------------------------------------


def test_data_survives_reopening_the_file(db_path):
    conn = db.connect(db_path)
    try:
        exercise_id = add_exercise(conn, name="Sentadilla", name_key="sentadilla")
        conn.commit()
    finally:
        conn.close()

    reopened = db.connect(db_path)
    try:
        row = reopened.execute(
            "SELECT name, name_key FROM exercise WHERE id = ?", (exercise_id,)
        ).fetchone()
    finally:
        reopened.close()

    assert row["name"] == "Sentadilla"
    assert row["name_key"] == "sentadilla"
