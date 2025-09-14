import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        print(f" SQL query: {query}")
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
