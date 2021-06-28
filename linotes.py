import pandas as pd
import sqlite3
import argparse

DEFAULT_CSV_FILE = "Connections.csv"
DEFAULT_DB = "connections.db"
DEFAULT_TABLE = "conn_info"

def create_connection(dbname):

    """ Return a connection and cursor to the database
    """

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()

    return connection, cursor

def create_db_and_table(input_csv_file, dbname):

    """ Create the initial database and table using default names. 
        Insert all records read from the csv file into the table.
    """

    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS conn_info (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, company TEXT, position TEXT, notes TEXT)')

    df = pd.read_csv(input_csv_file)
    num_records = df.shape[0]
    res = [insert_record(connection, cursor, a,b,c,d) for a,b,c,d in zip(df['First Name'],df['Last Name'],df['Company'],df['Position'])]

    connection.commit()
    connection.close()
    print('successfully created database and table. Inserted records: ',num_records)

def read_from_table(mcursor):

    """ Read all records from the table.
    """

    readQuery = "SELECT * FROM conn_info"
    mcursor.execute(readQuery)
    data = mcursor.fetchall()

    return data

def insert_record(mconn, mcursor, a,b,c,d):

    """ Insert a record into the table
    """

    insertQuery = """INSERT INTO conn_info (first_name, last_name, company, position, notes) VALUES (?,?,?,?,?)"""
    n = 'none'
    record = (a,b,c,d,n)
    mcursor.execute(insertQuery,record)
    mconn.commit()

    return

def get_id(mcursor, fname, lname):

    """ Get id based on first and last name.
    """

    getQuery = """SELECT id, first_name, last_name, company FROM conn_info WHERE lower(first_name) LIKE ? || '%' and  lower(last_name) LIKE ? || '%'"""
    record = (fname,lname)
    mcursor.execute(getQuery,record)

    data = mcursor.fetchall()

    return data

def find_person_by_name(mcurr, fname, lname):

    """ Find a person based on first and last name.
        Partial strings for the names will work too.
    """

    getQuery = """SELECT * FROM conn_info WHERE lower(first_name) LIKE ? || '%' and lower(last_name) LIKE ? || '%'"""
    record = (fname,lname)
    mcurr.execute(getQuery,record)

    data = mcurr.fetchall()

    return data

def update_record(mconn, mcurr, fname, lname, mnote):

    """ Update a record based on first and last name with given notes.
        Partial strings for the names will work too.
    """

    mid = get_id(mcurr, fname, lname)   
    pid = mid[0][0]

    if len(mid) >  1:
        print('Found multiple matches. Which id do you want to update?')
        for item in mid:
            print(item[0], item[1], item[2], item[3])
        select_id = input('id: ')
        pid = select_id

    updateQuery = """UPDATE conn_info SET notes = ? WHERE id = ?"""
    record = (mnote,pid)
    mcurr.execute(updateQuery,record)

    mconn.commit()
    print('successfully updated record')

    return 1

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action='store_true', help="initialize database")
    parser.add_argument("-i", default=DEFAULT_CSV_FILE, help="name of input csv file containing connection info")
    parser.add_argument("-d", default=DEFAULT_DB, help="name of sqllite3 database")
    parser.add_argument("-r", action='store_true', help="read from table")
    parser.add_argument("-a", action='store_true', help="add note")
    parser.add_argument("-F", default=None, help="first name")
    parser.add_argument("-L", default=None, help="last name")
    parser.add_argument("-n", default='None', help="name of input csv file containing connection info")
    parser.add_argument("-p", action='store_true', help="find person")
    args = parser.parse_args()

    conn=None
    if args.c:
        print('creating new DB and table...')
        input_csv_file = args.i
        dbname = args.d
        create_db_and_table(input_csv_file, dbname)
    elif args.r:
        print('reading all entries from table...')
        conn, curr = create_connection(DEFAULT_DB)
        
        mdata = read_from_table(curr)
        for item in mdata:
            print(item)
    elif args.a:
        print('adding note to connection...')
        fname = args.F
        lname = args.L
        note = args.n

        conn, curr = create_connection(DEFAULT_DB)
        update_record(conn, curr, str(fname).lower(), str(lname).lower(), note)
    elif args.p:
        print('finding person...')
        fname = args.F
        lname = args.L

        conn, curr = create_connection(DEFAULT_DB)
        persons = find_person_by_name(curr, str(fname).lower(), str(lname).lower())
        for person in persons:
            print(person)

    if conn:
        conn.close()

