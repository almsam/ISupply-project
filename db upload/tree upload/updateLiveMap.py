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

map = pd.DataFrame(out, columns=["ser", "cat"])

print(map)

# save as a CSV file
output_path = "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/tree upload/liveMap.csv"
query_df = pd.DataFrame(map); query_df.to_csv(output_path, index=False) # oop type shenanigans - to df & to csv
