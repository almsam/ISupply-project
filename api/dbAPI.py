import pandas as pd
import psycopg2
import numpy as np

con = psycopg2.connect(
    database="iSupply",
    host="38.180.117.52",
    user="postgres",
    password="deerRun",
    port="5432",
)
cursor = con.cursor()
cursor.execute("""select * from "Categories" c""")
out = cursor.fetchall()  # make a dictionary of what the db currently has
cursor.close()
con.close()

