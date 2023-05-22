import os
import sqlite3
import random
from datetime import datetime, timedelta

"""
This script can be used to add example data to the
local SQLite database for testing purposes.
"""


# Example categories to insert into the database.
categories = {
    "category 1": None,
    "category 2": ["sub category 1", "sub category 2", "sub category 3"],
    "category 3": ["sub category 4", "sub category 5", "sub category 6"],
    "category 4": ["sub category 7", "sub category 8", "sub category 9"],
}


def insert_categories(cursor: sqlite3.Cursor) -> int:
    """
    Insert categories into the database,
    and return the number of categories inserted.
    """
    category_count = 0

    for category, sub_categories in categories.items():
        category_count += 1
        current_parent_category_id = category_count
        query = f"""INSERT INTO api_category
                    (id, name, level, parent_id)
                    VALUES
                    ({category_count}, '{category}', 1, NULL)"""
        cursor.execute(query)

        if sub_categories:
            for sub_category in sub_categories:
                category_count += 1
                query = f"""INSERT INTO api_category
                    (id, name, level, parent_id)
                    VALUES
                    ({category_count}, '{sub_category}', 2, {current_parent_category_id})"""
                cursor.execute(query)

    return category_count


def random_time_str(delta_seconds: int) -> str:
    """
    Return a random time string in the format of "YYYY-MM-DD HH:MM:SS"
    between the current time and the current time minus delta_seconds.
    """
    start_datetime = datetime.today() - timedelta(seconds=delta_seconds)
    start_offset = delta_seconds * random.random()

    random_datetime = start_datetime + timedelta(seconds=start_offset)

    return random_datetime.strftime("%Y-%m-%d %H:%M:%S")


def insert_random_case(categories: int, cursor: sqlite3.Cursor, delta_seconds: int) -> None:
    """
    Insert a random case into the database.
    """
    medium = random.choice(["phone", "email"])
    customer_time = random.randint(1, 10) * 1000000
    additional_time = random.randint(1, 10) * 1000000
    time = random_time_str(delta_seconds)
    created_at = time
    edited_at = time
    case_id = random.randint(1, 1000)
    category_id = random.randint(1, categories)

    query = f"""INSERT INTO api_case
        (medium, customer_time, additional_time, created_at, edited_at, case_id, category_id)
        VALUES
        ('{medium}', {customer_time}, {additional_time}, '{created_at}', '{edited_at}', {case_id},
         {category_id})"""
    cursor.execute(query)


def add_example_data(db_path: str):
    """
    Add example data to the database.
    """
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()

        # Clear categories
        cursor.execute("DELETE FROM api_category")
        # Insert new categories
        category_count = insert_categories(cursor)

        # Clear cases
        cursor.execute("DELETE FROM api_case")
        # Insert new cases
        for _ in range(10_000):
            insert_random_case(category_count, cursor, 60 * 60 * 24 * 100)

        sqliteConnection.commit()
        print(f"Data inserted successfully into {db_path}.")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data.", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()


def cli():
    """
    Command line interface for adding example data to the database.
    """
    db_path = "src/db.sqlite3"

    if not os.path.isfile(db_path):
        print(f"Database not found at {db_path}.")
        return

    print(f"This action will delete all cases and categories in {db_path}. Continue? (y/n)")

    if input().lower() == "y":
        add_example_data(db_path)
    else:
        print("Action cancelled.")


if __name__ == "__main__":
    cli()
