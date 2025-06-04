import sqlite3

def connection(db_name):
    def decorator(func):
        def wrapper(*args, **kwargs):

            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            result = func(cursor, *args, **kwargs)

            conn.commit()
            #TODO: Fikse exception med rollback
            conn.close()
            
            return(result)
        return(wrapper)
    return(decorator)