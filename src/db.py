import sqlite3

def insert_record(stu, last, next, status):
    conn = sqlite3.connect('bpa.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO record (stu, last, next, status) values ('{stu}', '{last}', '{next}', '{status}')".format(
        stu=stu,
        last=last,
        next=next,
        status=status
    ))

    cursor.close()
    conn.commit()
    conn.close()
