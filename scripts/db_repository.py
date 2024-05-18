import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="diabetes",
        user="postgres",
        password="postgres",
        port='5432'
    )
    return conn

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

    conn.commit()
    cur.close()

def login(conn, email, password):
    cur = conn.cursor()
    query = """
        SELECT id, display_name FROM users WHERE email = %s AND password = %s
    """
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
    query = """
        SELECT * FROM users WHERE email = %s
    """
    params = (email,)
    cur.execute(query, params)
    user = cur.fetchone()
    cur.close()

    if user is None:
        return True
    else:
        return False

def get_height(conn, user_id):
    cur = conn.cursor()
    query = """
        SELECT height FROM users WHERE id = %s
    """
    params = (user_id,)
    cur.execute(query, params)
    height = cur.fetchone()
    cur.close()
    return height

def get_weight(conn, user_id):
    cur = conn.cursor()
    query = """
        SELECT weight, datetime FROM weight WHERE user_id = %s ORDER BY datetime ASC
    """
    params = (user_id,)
    cur.execute(query, params)
    weights = cur.fetchall()
    cur.close()
    return weights

def get_glucoses(conn, user_id):
    cur = conn.cursor()
    query = """
        SELECT level, datetime FROM glucose WHERE user_id = %s ORDER BY datetime ASC
    """
    params = (user_id,)
    cur.execute(query, params)
    glucoses = cur.fetchall()
    cur.close()
    return glucoses

def get_exercises(conn):
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
        SELECT title, time_elapsed, calories_total FROM exercises_users WHERE user_id = %s
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
    query = """
        INSERT INTO users (email, password, display_name, gender, age, height) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (email, password, display_name, gender, age, height)
    cur.execute(query, params)
    conn.commit()

def insert_glucose(conn, record, datetime, user_id):
    cur = conn.cursor()
    
    query = """
        INSERT INTO glucose (level, datetime, user_id) 
        VALUES (%s, %s, %s)
    """
    params = (record, datetime, user_id)
    cur.execute(query, params)
    conn.commit()
    cur.close()

def insert_weight(conn, weight, datetime, user_id):
    cur = conn.cursor()
    query = """
        INSERT INTO weight (user_id, weight, datetime) 
        VALUES (%s, %s, %s)
    """
    params = (user_id, weight, datetime)
    cur.execute(query, params)
    conn.commit()

def insert_exercises_user(conn, user_id, exercise_id, title, time_elapsed, calories_total):
    cur = conn.cursor()
    query = """
        INSERT INTO exercises_users (user_id, exercise_id, title, time_elapsed, calories_total) 
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (user_id, exercise_id, title, time_elapsed, calories_total)
    cur.execute(query, params)
    conn.commit()
