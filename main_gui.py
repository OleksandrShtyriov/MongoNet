import tkinter as tk

import pymongo

from functions_gui import *

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]

col_users = db["users"]
col_posts = db["posts"]
col_reacts = db["reactions"]
col_friend_req = db["friend_requests"]
col_friends = db["friends"]
col_comments = db["comments"]
col_comment_reacts = db["comment_reactions"]

if __name__ == "__main__":
    window = tk.Tk()
    window.attributes("-fullscreen", True)

    login_screen(col_users, col_posts, col_reacts, 
                 col_friend_req, col_friends,
                 col_comments, col_comment_reacts,
                 window)

    window.mainloop()

