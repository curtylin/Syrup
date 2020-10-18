import sqlite3

def seedUsers():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()
    #Create table
    c.execute("INSERT INTO customers VALUES ('5063' , 'clxddf@gmail.com' , 100)")
    c.execute("INSERT INTO customers VALUES ('5064' , 'jssfk@gmail.com' , 100)")
    c.execute("INSERT INTO customers VALUES ('5065' , 'jddgy@gmail.com' , 100)")
    c.execute("INSERT INTO customers VALUES ('6604' , 'billnye@gmail.com' , 50)")
    conn.commit()
    conn.close()
    return

