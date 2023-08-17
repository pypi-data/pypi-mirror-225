#!/usr/bin/env python3


from MightyMaxims.Maxims import Maxims as QDB

def get_random():
    import random
    import textwrap
    db = QDB()
    db.open()
    nelem = db.count()
    if not nelem:
        print("Database is empty.")
        quit()
    which = random.randrange(1, nelem + 1)
    go = db.select(f'SELECT * from {db.table_name} where ID = {which} LIMIT 1;')
    q = dict(*go)
    print(f"\nMighty Maxims #{q['MightyID']}: {q['Author']}\n")
    for _str in textwrap.wrap(q['Quote'], width=40):
        print(_str)
    print()
    db.close()

                
if __name__ == '__main__':
    get_random()
    
