from urllib.parse import urlparse
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def connect_to_db():
    url = DATABASE_URL
    try:
        result = urlparse(url)
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f'Could not connect to the database: {e}')
        return e

def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            display_name TEXT,
            gender TEXT,
            age INT,
            height FLOAT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS weight (
            id SERIAL PRIMARY KEY,
            weight FLOAT NOT NULL,
            datetime TIMESTAMP NOT NULL,
            user_id SERIAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS glucose (
            id SERIAL PRIMARY KEY,
            level INT NOT NULL,
            datetime TIMESTAMP NOT NULL,
            user_id SERIAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            calories FLOAT,
            intensity TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS exercises_users (
            id SERIAL PRIMARY KEY,
            user_id SERIAL,
            exercise_id SERIAL,
            title TEXT,
            time_elapsed FLOAT,
            calories_total FLOAT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        )
    ''')

    cur.execute('''
        SELECT COUNT(*) FROM exercises
    ''')
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('''
            INSERT INTO exercises (title, calories, intensity)
            VALUES
                ('Corrida', 600, 'Alta'),
                ('Caminhada', 250, 'Baixa'),
                ('Natação', 600, 'Alta'),
                ('Ciclismo', 450, 'Alta'),
                ('Yoga', 200, 'Baixa'),
                ('Pular Corda', 600, 'Alta'),
                ('Musculação', 300, 'Média'),
                ('Pilates', 200, 'Baixa'),
                ('Hidroginástica', 300, 'Média'),
                ('Escalada', 500, 'Alta'),
                ('Basquete', 450, 'Alta'),
                ('Vôlei', 300, 'Média'),
                ('Remo', 600, 'Alta'),
                ('Boxe', 700, 'Alta'),
                ('Futebol', 800, 'Alta'),
                ('Tennis', 400, 'Alta'),
                ('Crossfit', 700, 'Alta');
        ''')
        conn.commit()
    cur.close()

def get_all_tables(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema='public'
    """)
    tables = cur.fetchall()
    cur.close()
    return [table[0] for table in tables]

def fetch_table_data(conn, table_name):
    cur = conn.cursor()
    query = f'SELECT * FROM {table_name}'
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    return pd.DataFrame(rows, columns=colnames)

def login(conn, email, password):
    cur = conn.cursor()
    query = '''
        SELECT id, display_name FROM users WHERE email = %s AND password = %s
    '''
    params = (email, password)
    cur.execute(query, params)
    user = cur.fetchone()
    cur.close()

    if user is None:
        return False, None
    else:
        user_id, display_name = user
        return user_id, display_name

def verify_email(conn, email):
    cur = conn.cursor()
    query = '''
        SELECT * FROM users WHERE email = %s
    '''
    params = (email,)
    cur.execute(query, params)
    user = cur.fetchone()
    cur.close()

    if user is None:
        return True
    else:
        return False

def get_users(conn, user_):
    cur = conn.cursor()
    query = '''
        SELECT id, email, display_name, gender, age, height FROM users
    '''
    cur.execute(query)
    users = cur.fetchall()
    cur.close()
    return users

def get_height(conn, user_id):
    cur = conn.cursor()
    query = '''
        SELECT height FROM users WHERE id = %s
    '''
    params = (user_id,)
    cur.execute(query, params)
    height = cur.fetchone()
    cur.close()
    return height

def get_weight(conn, user_id):
    cur = conn.cursor()
    query = '''
        SELECT weight, datetime FROM weight WHERE user_id = %s ORDER BY datetime ASC
    '''
    params = (user_id,)
    cur.execute(query, params)
    weights = cur.fetchall()
    cur.close()
    return weights

def get_glucoses(conn, user_id):
    cur = conn.cursor()
    query = '''
        SELECT id, level, datetime FROM glucose WHERE user_id = %s ORDER BY datetime ASC
    '''
    params = (user_id,)
    cur.execute(query, params)
    glucoses = cur.fetchall()
    cur.close()
    return glucoses

def get_exercises(conn, user_id):
    cur = conn.cursor()
    query = '''
        SELECT * FROM exercises
    '''
    cur.execute(query)
    exercises = cur.fetchall()
    cur.close()
    return exercises

def get_exercises_user(conn, user_id):
    cur = conn.cursor()
    query = '''
        SELECT id, title, time_elapsed, calories_total FROM exercises_users WHERE user_id = %s
    '''
    params = (user_id,)
    cur.execute(query, params)
    exercises = cur.fetchall()
    cur.close()
    return exercises

def get_last_glucose(conn, user_id):
    cur = conn.cursor()
    query = ('''
        SELECT level, datetime FROM glucose WHERE user_id = %s ORDER BY datetime DESC
    ''')

    params = (user_id,) 
    cur.execute(query, params)
    glucose = cur.fetchone()
    if glucose is None:
        return None, None
    level, datetime = glucose
    return level, datetime

def insert_user(conn, email, password, display_name, gender, age, height):
    cur = conn.cursor()
    query = '''
        INSERT INTO users (email, password, display_name, gender, age, height) 
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    params = (email, password, display_name, gender, age, height)
    cur.execute(query, params)
    conn.commit()

def delete_user_by_id(conn, user_id):
    cur = conn.cursor()
    params = (user_id,)
    # Delete associated records from the 'weight' table
    query = "DELETE FROM weight WHERE user_id = %s"
    cur.execute(query, params)
    # Delete associated records from the 'glucose' table
    query = "DELETE FROM glucose WHERE user_id = %s"
    cur.execute(query, params)
    # Delete associated records from the 'exercises_users' table
    query = "DELETE FROM exercises_users WHERE user_id = %s"
    cur.execute(query, params)
    # Delete the user
    query = "DELETE FROM users WHERE id = %s"
    cur.execute(query, params)
    conn.commit()

def insert_glucose(conn, record, datetime, user_id):
    cur = conn.cursor()
    
    query = '''
        INSERT INTO glucose (level, datetime, user_id) 
        VALUES (%s, %s, %s)
    '''
    params = (record, datetime, user_id)
    cur.execute(query, params)
    conn.commit()
    cur.close()

def insert_weight(conn, weight, datetime, user_id):
    cur = conn.cursor()
    query = '''
        INSERT INTO weight (user_id, weight, datetime) 
        VALUES (%s, %s, %s)
    '''
    params = (user_id, weight, datetime)
    cur.execute(query, params)
    conn.commit()

def insert_exercises_user(conn, user_id, exercise_id, title, time_elapsed, calories_total):
    cur = conn.cursor()
    query = '''
        INSERT INTO exercises_users (user_id, exercise_id, title, time_elapsed, calories_total) 
        VALUES (%s, %s, %s, %s, %s)
    '''
    params = (user_id, exercise_id, title, time_elapsed, calories_total)
    cur.execute(query, params)
    conn.commit()

def insert_exercise(conn, title, calories, intensity):
    cur = conn.cursor()
    query = '''
        INSERT INTO exercises (title, calories, intensity) 
        VALUES (%s, %s, %s)
    '''
    params = (title, calories, intensity)
    cur.execute(query, params)
    conn.commit()

def delete_exercise_by_id(conn, exercise_id):
    cur = conn.cursor()
    query = '''
        DELETE FROM exercises WHERE id = %s
    '''
    params = (exercise_id,)
    cur.execute(query, params)
    conn.commit()

def delete_exercises(conn):
    cur = conn.cursor()
    query = '''
        DELETE FROM exercises
    '''
    cur.execute(query)
    conn.commit()
    cur.close()

def delete_tables(conn):
    cur = conn.cursor()
    query = '''
        DROP TABLE IF EXISTS exercises_users CASCADE;
        DROP TABLE IF EXISTS exercises CASCADE;
        DROP TABLE IF EXISTS glucose CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        DROP TABLE IF EXISTS weight CASCADE;
    '''
    cur.execute(query)
    conn.commit()
    cur.close()