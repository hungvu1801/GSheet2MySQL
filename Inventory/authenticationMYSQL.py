from mysql.connector import connect

def enter_authentication_mysql(dbname):
    try:
        connection = connect(host='localhost', 
                            database=dbname,
                            user='root', 
                            password='BaeminInventory@123')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor(buffered=True)
        else:
            print('Not connected.')
        return db_Info, cursor, connection
    except Exception as err:
        print(f'...Error in authenticating MySQL...{err}')
        return