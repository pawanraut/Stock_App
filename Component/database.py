import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://postgres:pawan123@localhost:5432/stock_db"

connection_pool = pool.SimpleConnectionPool(1, 20, dsn=DATABASE_URL)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)

def create_tables():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'user'
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id) ON DELETE CASCADE,
                    order_id VARCHAR(50) NOT NULL,
                    tradingsymbol VARCHAR(50) NOT NULL,
                    quantity INT NOT NULL,
                    price NUMERIC(12,2) NOT NULL,
                    transaction_type VARCHAR(10) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS access_tokens (
                    id SERIAL PRIMARY KEY,
                    token VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
         
            cur.execute("INSERT INTO users (email, password) VALUES ('test@example.com', 'password123') ON CONFLICT DO NOTHING;")
            conn.commit()
            print("Tables created successfully.")
    finally:
        release_connection(conn)
