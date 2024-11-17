import pandas as pd
# import psycopg2
import numpy

df = pd.read_excel(
    "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/map.xlsx"
)
print(df.head())


def get_category_subcategory(df, index):
    num = df.loc[index, "Ser"]  # O( log(n) )
    name = df.loc[index, "combined"]
    return name, num


def process_categories(df, start, end):
    queryList = []

    for i in range(start, end):  # O(n)
        name, num = get_category_subcategory(df, i)
        num = str(num)

        query = (
            """INSERT INTO "Categories" (category_id, category) VALUES (%s, %s)""",
            (num, name),
        )
        queryList.append(str(query))






    # con.commit()
    # print(len(listOfCollisions), len(listOfAllErrors))
    # return listOfCollisions, listOfAllErrors
    print(len(queryList))
    return queryList

    # this should give us some details on where our data is going


# listOfCollisions = []
# listOfAllErrors = []
# queryList = []
queryList = process_categories(df, 0, 4600)



# for i in range(5):  # all 4600 for the sake of analysis
#     # collisions, errors = process_categories(
#     currentQL = process_categories(df, (100 * i), ((100 * i) + 100))
#     # listOfCollisions += collisions listOfAllErrors += errors
#     queryList += currentQL
#     print("100 number ", (i + 1), " done")

# currentQL = process_categories(df, cursor, con, (4500), (4596))
# queryList += currentQL
# print("100 number ", (46), " done")

print(len(queryList))
print(queryList)









# numpy.savetxt(
#     "c:/Users/samia/OneDrive/Desktop/ISupply-project/db upload/Map upload/errorLog.csv",
#     queryList,
#     delimiter=",",
# )

# for first 500, queryList had 3 entries:
# (\'INSERT INTO "Categories" (category_id, category) VALUES (%s, %s)\', (\'151\', nan))
# (\'INSERT INTO "Categories" (category_id, category) VALUES (%s, %s)\', (\'340\', nan))
# (\'INSERT INTO "Categories" (category_id, category) VALUES (%s, %s)\', (\'341\', \'Automobiles & Motorcycle s\'))

        # print(str(query))
        # query = str(query)

        # try:
        #     cursor.execute(
        #         """INSERT INTO "Categories" (category_id, category) VALUES (%s, %s)""",
        #         (num, name),
        #     )  # O(n)
        #     # cursor.execute(query)  # O(n)
        # except psycopg2.errors.UniqueViolation as e:
        #     # listOfAllErrors.append(i)
        #     # listOfCollisions.append(i)
        #     queryList.append(str(query))
        # except Exception as e:
        #     print(f"Error occurred: {e} q:", query)
        #     # listOfAllErrors.append(i)
        #     queryList.append(str(query))
        
        
# wipe the db from DBeaver

# con = psycopg2.connect(
#     database="iSupply",
#     host="38.180.117.52",
#     user="postgres",
#     password="deerRun",
#     port="5432",
# )
# cursor = con.cursor()  # open

# cursor.close()
# con.close()  # close