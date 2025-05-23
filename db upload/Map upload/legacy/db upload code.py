import pandas as pd
import psycopg2

df = pd.read_excel(
    "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/map.xlsx"
)
print(df.head())


def get_category_subcategory(df, index):
    num = df.loc[index, "Ser"]  # O( log(n) )
    name = df.loc[index, "combined"]
    return name, num


def process_categories(df, cursor, con, start, end):
    listOfCollisions = []
    listOfAllErrors = []
    j = 0

    for i in range(start, end):  # O(n)
        name, num = get_category_subcategory(df, i)
        num = str(num)

        try:
            cursor.execute(
                """INSERT INTO "Categories" (category_id, category) VALUES (%s, %s)""",
                (num, name),
            )  # O(n)
        except psycopg2.errors.UniqueViolation as e:
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

    # this should give us some details on where our data is going


listOfCollisions = []
listOfAllErrors = []

# wipe the db from DBeaver

con = psycopg2.connect(
    database="iSupply",
    host="38.180.117.52",
    user="postgres",
    password="deerRun",
    port="5432",
)
cursor = con.cursor()  # open

for i in range(45):  # all 4600 for the sake of analysis
    collisions, errors = process_categories(
        df, cursor, con, (100 * i), ((100 * i) + 100)
    )
    listOfCollisions += collisions
    listOfAllErrors += errors
    print("100 number ", (i + 1), " done")

collisions, errors = process_categories(df, cursor, con, (4500), (4596))
print("100 number ", (46), " done")

cursor.close()
con.close()  # close
