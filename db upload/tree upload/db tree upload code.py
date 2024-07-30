import pandas as pd
import psycopg2

# read from db
con = psycopg2.connect(
    database="iSupply",
    host="38.180.117.52",
    user="postgres",
    password="deerRun",
    port="5432",
)
cursor = con.cursor()
cursor.execute("""select * from "Categories" c""")
out = cursor.fetchall()
print(out)
cursor.close()
con.close()
