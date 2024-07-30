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

df = pd.DataFrame(out, columns=["ser", "cat"])
dfT = pd.read_excel("slimTree.xlsx")
dfT.fillna("-1", inplace=True)
dfT.head(15)

map_dic = df.set_index("cat")["ser"].to_dict()

dfInt = pd.DataFrame(dfT)

dfInt["category"] = dfInt["category"].map(map_dic).fillna(-1).astype(int)
dfInt["subcategory"] = dfInt["subcategory"].map(map_dic).fillna(-1).astype(int)

print("The dataframe has ", dfInt.size, "/27564 entries")

dfIntUnique = pd.DataFrame(dfInt.drop_duplicates())

print("Now the dataframe has ", dfIntUnique.size, "/15400 entries")
