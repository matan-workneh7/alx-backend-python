import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):# this function accepts the 
    @functools.wraps(func)
    def Wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        result = func(conn, *args ,*kwargs)
        return result
    return Wrapper

def retry_on_failure(retries=3, delay=1): #this accepts the function with the db connection parameter func right? but how will it take the retries and delays kwargs if the withdb function (func) only takes the conn
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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