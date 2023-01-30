import sqlite3
import json
from models import Species

SPECIES = [
    {
        "id": 1,
        "name": "Procyon cancrivorus"

    }
]


def get_all_species():
    with sqlite3.connect("./snakes.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name
        FROM Species a
        """)

        species = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            specie = Species(
                row['id'], row['name'])

            species.append(specie.__dict__)

    return species


def get_single_species(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name
        FROM Species a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        specie = Species(data['id'], data['name'])

        return specie.__dict__
