import sqlite3
import random


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
    # Clear table
    cursor.execute("DELETE FROM api_category")

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
                            ({category_count}, '{sub_category}', 2, '{current_parent_category_id}')"""
                cursor.execute(query)
    
    return category_count


def random_time_str():
    year = "2023"
    month = "05"
    day = str(random.randint(1, 17)).rjust(2, '0')
    hour = str(random.randint(8, 17)).rjust(2, '0')
    minute = str(random.randint(0, 59)).rjust(2, '0')
    second = str(random.randint(0, 49)).rjust(2, '0')

    return f"{year}-{month}-{day} {hour}:{minute}:{second}"


def get_random_case_insert_query(categories: int):
    medium = random.choice(["phone", "email"])
    customer_time = random.randint(1, 10) * 1000000
    additional_time = random.randint(1, 10) * 1000000
    time = random_time_str()
    created_at = time
    edited_at = time
    case_id = random.randint(1, 1000)
    category_id = random.randint(1, categories)


    return f"""INSERT INTO api_case
                (medium, customer_time, additional_time, created_at, edited_at, case_id, category_id) 
                VALUES 
                ('{medium}', {customer_time}, {additional_time}, '{created_at}', '{edited_at}', {case_id}, {category_id})"""


def add_example_data():
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite.")

        category_count = insert_categories(cursor)

        # Clear cases
        cursor.execute("DELETE FROM api_case")

        for _ in range(100):
            cursor.execute(get_random_case_insert_query(category_count))

        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table.", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed.")


if __name__ == "__main__":
    add_example_data()
    print("Done.")
