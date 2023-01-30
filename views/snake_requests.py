import sqlite3
import json
from models import Snake
from models import Species
from .species_requests import get_single_species

SNAKES = [
    {
        "id": 1,
        "name": "Annotée",
        "owner_id": 2,
        "species_id": 2,
        "gender": "Female",
        "color": 'Turquoise'
    }
]


def get_all_snakes():
    with sqlite3.connect("./snakes.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.owner_id,
            a.species_id,
            a.gender,
            a.color
        FROM Snakes a
        """)

        snakes = []

        dataset = db_cursor.fetchall()

        for row in dataset:

                snake = Snake(row['id'], row['name'], row['owner_id'], row['species_id'],
                                row['gender'], row['color'])

                snakes.append(snake.__dict__)

    return snakes



def get_single_snake(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.owner_id,
            a.species_id,
            a.gender,
            a.color,
            s.name species_name
        FROM Snakes a
        JOIN Species s
            ON s.id = a.species_id
        WHERE a.id = ?
        """, (id, ))

        snakes = []

        dataset = db_cursor.fetchall()
        
        for data in dataset:

            snake = Snake(data['id'], data['name'], data['owner_id'],
                            data['species_id'], data['gender'],
                            data['color'])
            species = Species(data['species_id'], data['species_name'])

            snake.species = species.__dict__

            snakes.append(snake.__dict__)

        return snake.__dict__



def create_snake(new_snake):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Snakes
            ( name, owner_id, species_id, gender, color )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_snake['name'], new_snake['owner_id'],
            new_snake['species_id'], new_snake['gender'],
            new_snake['color'], ))


        id = db_cursor.lastrowid

        new_snake['id'] = id


    return new_snake

def get_snakes_by_species(species):

    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.owner_id,
            c.species_id,
            c.gender,
            c.color
        from Snakes c
        WHERE c.species_id = ?
        """, (species,))

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snake(
                row['id'], row['name'], row['owner_id'], row['species_id'], row['gender'], row['color'])
            snakes.append(snake.__dict__)

    return snakes

