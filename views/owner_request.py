import sqlite3
import json
from models import Owner

OWNERS = [
    {
        "id": 1,
        "first_name": "Jarrett",
        "last_name":"Thunder",
        "email": "jthunder0@amazon.de"
    
    }
]

def get_all_owners():
    with sqlite3.connect("./snakes.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.first_name,
            a.last_name,
            a.email
        FROM Owners a
        """)

        owners = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            owner = Owner(row['id'], row['first_name'], row['last_name'], row['email'])

            owners.append(owner.__dict__)

    return owners


def get_single_owner(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.first_name,
            a.last_name,
            a.email
        FROM Owners a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        owner = Owner(data['id'], data['first_name'], data['last_name'], data['email'])

        return owner.__dict__