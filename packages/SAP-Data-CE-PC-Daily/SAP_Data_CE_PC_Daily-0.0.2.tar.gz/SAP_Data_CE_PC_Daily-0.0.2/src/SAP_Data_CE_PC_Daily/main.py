import pymssql
import pandas as pd
import getpass
import base64
from datetime import datetime

def retrieve_script_from_database(encoded_script_from_db):
    # Decoding
    decoded_script = base64.b64decode(encoded_script_from_db).decode('utf-8')
    return decoded_script

def SAP_Data_CE_PC_Daily():
    # Database connection
    server = 'KFICWPNXDBSP01'
    database = 'PlanX'
    username = 't_board_db'
    password = 'planX2018'
    cnxn = pymssql.connect(server=server, database=database, user=username, password=password)
    cursor = cnxn.cursor()

    # Fetch the script
    cursor.execute("SELECT Script_Data FROM [sta].[PowerBI_Script] WHERE ScriptID = 1 AND Region_Name = 'H.Q'")
    row = cursor.fetchone()

    if row is not None:
        encoded_script_from_database = row[0]
        python_script = retrieve_script_from_database(encoded_script_from_database)

        exec_environment = {}
        exec(python_script, exec_environment)  # Execute the script with the custom environment

        if 'main' in exec_environment:
            df = exec_environment['main']()  # Call 'main' function from the executed script's environment and get 'df'
        else:
            print("main function not found in the executed script.")
            df = None

    cnxn.close()
    return df