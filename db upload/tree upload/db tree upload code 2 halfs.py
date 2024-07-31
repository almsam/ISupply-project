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
out = cursor.fetchall()  # make a dictionary of what the db currently has
cursor.close()
con.close()

df = pd.DataFrame(out, columns=["ser", "cat"])
dfT = pd.read_excel(
    "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/slimTree.xlsx"  # Read the existing tree
)
dfT.fillna("-1", inplace=True)
dfT.head(15)

map_dic = df.set_index("cat")["ser"].to_dict()

dfInt = pd.DataFrame(dfT)

dfInt["category"] = dfInt["category"].map(map_dic).fillna(-1).astype(int)
dfInt["subcategory"] = (
    dfInt["subcategory"].map(map_dic).fillna(-1).astype(int)
)  # fill -1 for targeted cells

print(
    "The dataframe has ", dfInt.size, "/ 27564 entries"
)  # confirm all entries got through

dfIntUnique = pd.DataFrame(dfInt.drop_duplicates())

print(
    "Now the dataframe has ", dfIntUnique.size, "/ 15400 entries"
)  # confirm all unique entries got through

dfIntUnique.reset_index(drop=True, inplace=True)
dfIntUnique.size


def get_category_subcategory(df, index):
    parent = str(df.loc[index, "category"])  # O( log(n) )
    child = str(df.loc[index, "subcategory"])
    return parent, child


def process_categories(df, cursor, con, start, end):
    listOfCollisions = []
    listOfAllErrors = []
    j = 0

    for i in range(start, end):  # for each entry in the data frame # O(n)
        parent, child = get_category_subcategory(df, i)

        try:
            cursor.execute(
                """INSERT INTO "Category_Tree" (category_id, sub_category_id) VALUES ("""
                + parent
                + """, """
                + child
                + """)"""
            )  # O(n)
        except psycopg2.errors.UniqueViolation as e:  # catch a unique exception
            listOfAllErrors.append(i)
            listOfCollisions.append(i)
        except Exception as e:
            print(f"Error occurred: {e}")
            listOfAllErrors.append(i)

        if j == 10:
            con.commit()
            j = 0  # this time we will commit for each 10th entry
        j = j + 1

    con.commit()

    print(len(listOfCollisions), len(listOfAllErrors))
    return listOfCollisions, listOfAllErrors


listOfCollisions = []
listOfAllErrors = []

# wipe db

con = psycopg2.connect(
    database="iSupply",
    host="38.180.117.52",
    user="postgres",
    password="deerRun",
    port="5432",
)
cursor = con.cursor()  # open

# for i in range(77):  # first 77 00, this was already done
#     collisions, errors = process_categories(
#         dfIntUnique, cursor, con, (100 * i), ((100 * i) + 100)
#     )
#     listOfCollisions += collisions
#     listOfAllErrors += errors
#     print("100 number ", (i + 1), " done")

# collisions, errors = process_categories(dfIntUnique, cursor, con, (7702), ((7800)))
# listOfCollisions += collisions
# listOfAllErrors += errors
# print("100 number ", 77, " done, this case was special")

for i in range(76):  # second 77 00 - essentially skip the bad entry
    k = i + 78
    collisions, errors = process_categories(
        dfIntUnique, cursor, con, (100 * k), ((100 * k) + 100)
    )
    listOfCollisions += collisions
    listOfAllErrors += errors
    print("100 number ", (k + 1), " done, i =", i)

cursor.close()
con.close()  # close
