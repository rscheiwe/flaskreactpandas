import sys
import os
import settings
import mysql.connector

module_path = os.path.abspath(os.getcwd())    
if module_path not in sys.path:       
    sys.path.append(module_path)

cnx = mysql.connector.connect(user=settings.USER, 
                                password=settings.PASS,
                                host=settings.HOST,
                                database=settings.DB,
                                port=settings.PORT,
                                use_pure=False)

cursor = cnx.cursor()

query = ('SELECT * FROM `credit_cards`')

cursor.execute(query)

for last_four in cursor:
    print(last_four)

cursor.close()
cnx.close()
