import sqlite3

def check_table(dbfile, table_name):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE name=\"%s\"" % (table_name))
    all_rows = c.fetchall()
    conn.close()
    return (len(all_rows) == 1)
