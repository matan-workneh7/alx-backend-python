import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    @functools.wraps(func)
    def Wrapper(*args, **kwargs):
        conn = sqlite3.connect("user.db")
        result = func(conn, *args ,*kwargs)
        return result
    return Wrapper

def retry_on_failure(func):
    def wrapper(*args, retries=3, delay=2, **kwargs):
        last_exception = None
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
        raise last_exception
    return wrapper  

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)