import sqlite3 
import functools

def with_db_connection(func): #i wrote back this function because we were making it on another file
    def wrapper(*args, **kwargs): 
        conn = sqlite3.connect("users.db") #why do we need to open the connection here and writing it again it in the transaction function?
        result = func(conn, *args, **kwargs)
        conn.close()
        return result
    return wrapper

def transactional(func): #are we taking this func parameter from the update_user_email or from the with_db_connection function?
    @functools.wraps(func) #i dont really understand what this does and why were using it 
    def wrapper(conn, *args, **kwargs):
        # do i need to open conn here too? because it already made in with db connection
        try:
            result = func(conn, *args, **kwargs) #i guess this one takes the parameters from update_user_email funtcion
            conn.commit()
            return result
        except Exception as e:#dont understand what e and exception does here but i guess its for error handling
            conn.rollback()
            print(f"Transaction failed: {e}") #i guess this prints the error if transaction fails
        finally:
            conn.close()
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')