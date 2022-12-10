"""
Database for user logins
==============================

"""
import sqlite3
from pydoc import html


def create_db():
    """ Create table 'logins' in 'login' database """
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logins (
                    username text NOT NULL,
                    password text NOT NULL,
                    access_level text,
                    currentuser text
                    )''')
        conn.commit()
        return True
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def add_user(username, password, access_level="user"):
    """ Data insert into login table
    param: username of user
    param: password of user
    param: level of access user has, defaulted to the lowest access
    """

    # initialize current user to false
    currentuser = "false"
    data_to_insert = [(username, password, access_level, currentuser)]
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        c.executemany("INSERT INTO logins VALUES (?, ?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def is_user(username) -> bool:
    """
    determine if username already exits
    :param: username trying to be created
    :return: true if username exists, false if not

    """
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        # get usernames
        results = c.execute("SELECT username FROM logins")
        # find matching username if exists
        for row in results:
            if row[0] == username:
                return True
        return False
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def get_user(username: str):
    """
    gets password of user trying to log in
    :param: username of user trying to log in
    :return: password of username passed in, 0 if no user found
    """
    username = html.escape(username)
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        # find password for username to see if they match
        query = f"SELECT password FROM logins WHERE username='{username}'"
        result = c.execute(query).fetchall()
        return result[0][0]
    except IndexError:
        return 0
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def is_current_user():
    """
    determine if user is current user
    :return: str, username of active user
    """
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        # find user that has current user = true
        query = "SELECT username FROM logins WHERE currentuser = 'true'"
        result = c.execute(query).fetchall()[0][0]
        return result
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def set_current_user(username):
    """
    sets passed in username to the current user
    :param: str, username to be set to current user
    """
    username = html.escape(username)
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        # if not current user, set to current user
        if c.execute(f"SELECT currentuser FROM logins WHERE username='{username}'").fetchall()[0][0] == "false":
            update_value = f'''UPDATE logins SET currentuser = 'true' WHERE username="{username}"'''
            c.execute(update_value)
            conn.commit()
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def set_not_current_user(username):
    """
    sets passed in username to not be the current user
    :param: str, username to be set to not current user
    """

    username = html.escape(username)
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        # if current user, set to not current user
        if c.execute(f"SELECT currentuser FROM logins WHERE username='{username}'").fetchall()[0][0] == "true":
            update_value = f'''UPDATE logins SET currentuser = 'false' WHERE username="{username}"'''
            c.execute(update_value)
            conn.commit()
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def get_access_level(username):
    """
    gets access level of username
    :param: username to get access level of
    return: str, access level of user
    """
    username = html.escape(username)
    try:
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        # get access level from passed in username
        return c.execute(f"SELECT access_level FROM logins WHERE username='{username}'").fetchall()[0][0]
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


# if database has not been created, will create
create_db()
