import pymongo

from functions import *

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]

col = db["users"]
col1 = db["posts"]

if __name__ == "__main__":
    try:
        print_all(col)
#       user = input_login(col)

#        input_post(col1, user)
#        print_posts(col1)
    except Exception as e:
        print(str(e))

