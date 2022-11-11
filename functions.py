from os import path
from datetime import datetime

from constants import *

def insert_user(col,
                email: str, pw: str, fn: str, 
                ln: str, interests: list) -> None:
    col.insert_one({"_id": get_id(),
                    "email": email,
                    "password": pw,
                    "firstname": fn,
                    "lastname": ln,
                    "interests": interests})    

    inc_id()

def input_user(col) -> None:
    email = input("Email: ")
    pw = input("Password: ")
    fn = input("First name: ")
    ln = input("Last name: ")
    interests = input("Interests: ")
    
    interests = interests.split()

    insert_user(col, email, pw, fn, ln, interests)

def id_file_exists() -> bool:
    return path.exists(id_file)

def inc_id() -> None:
    id = get_id()

    file = open(id_file, "w")
    file.write(str(id + 1))
    file.close()

def get_id() -> int:
    if id_file_exists():
        file = open(id_file, "r")
        id = int(file.readline()) 
        file.close()
    else:
        id = 0

    return id

def print_all(col) -> None:
    for user in col.find():
        print_user(dict(user))

def print_user(user: dict) -> None:
    print("User #" + str(user["_id"]) + ":")
    print("    email: " + user["email"])
    print("    password: " + user["password"])
    print("    first name: " + user["firstname"])
    print("    last name: " + user["lastname"])
    print("    interests: " + " ".join(user["interests"]))

def user_to_str(user: dict) -> str:
    return user["firstname"] + " " + user["lastname"]

def login(col, email: str, pw: str) -> bool:
    query = {"email": email, "password": pw}
    users = list(col.find(query))

    if len(users) > 0:
        return users[0]
    else:
        raise Exception("No such user")

def input_login(col):
    email = input("Email: ")
    pw = input("Password: ")

    return login(col, email, pw)

def write_post(col, time, title: str, text: str, user: dict) -> None:
    col.insert_one({"time": time,
                    "title": title,
                    "text": text,
                    "user": user})

def input_post(col, user) -> None:
    title = input("Title: ")

    text = input("Text: \n")

    while True:
        line = input()

        if line:
            text += line + "\n"
        else:
            break

    time = datetime.now()
    write_post(col, time, title, text, user)

def print_posts(col) -> None:
    print("\n\n\n".join(posts_to_str(col)))

def posts_to_str(col) -> list:
    res = []

    for post in col.find().sort("time", -1):
        res.append(post_to_str(dict(post)))

    return res

def post_to_str(post: dict) -> str:
    res = ""
    res += post["title"] + " by " + (post["user"]["firstname"] + " "
                                  + post["user"]["lastname"] + " "
                                  + post["user"]["email"])
    res += "\n" + post["time"].strftime("%Y-%m-%d %H:%M:%S")
    res += "\n\n"
    res += post["text"]

    return res

def print_post(post: dict) -> None:
    print(post_to_str(post))

def react(col_react, post, user) -> None:
    if col_react.find_one({"post": post}):
        r = col_react.find_one({"post": post})
        users = r["users"]
        new_users = users + [user]
        col_react.update_one({"post": post}, {"$set": {"users": new_users}},
                             upsert=False)
    else:
        col_react.insert_one({"post": post,
                              "users": [user]})

def unreact(col_react, post, user) -> None:
    r = col_react.find_one({"post": post})
    new_users = r["users"]
    new_users.remove(user)

    col_react.update_one({"post": post}, {"$set": {"users": new_users}},
                         upsert=False)

def get_reacts(col_react, post) -> int:
    if col_react.find_one({"post": post}):
        return len(col_react.find_one({"post": post})["users"])
    return 0

def get_users(col_react, post) -> list:
    if col_react.find_one({"post": post}):
        return col_react.find_one({"post": post})["users"]
    return []

def get_reacts_str(col_react, post) -> str:
    reacts = get_reacts(col_react, post)
    res = str(reacts) + " people liked"

    if reacts:
        res += ":\n"
        res += "\n".join(list(map(user_to_str, get_users(col_react, post))))

    return res

def send_request(col_friend_req, user1, user2) -> None:
    col_friend_req.insert_one({"from": user1,
                               "to": user2})

def get_requests(col_friends_req, user) -> list:
    return list(col_friends_req.find({"to": user}))

def request_to_str(req: dict) -> str:
    return "Incoming friend request from " + user_to_str(req["from"])

def accept(col_friend_req, col_friends, user1, user2) -> None:
    col_friends.insert_one({"user1": user1,
                            "user2": user2})
    col_friend_req.delete_one({"from": user1,
                               "to": user2})

def deny(col_friend_req, col_friends, user1, user2) -> None:
    col_friend_req.delete_one({"from": user1,
                               "to": user2})

def remove_friend(col_friend, user1, user2):
    if list(col_friend.find({"user1": user1, "user2": user2})):
        col_friend.delete_many({"user1": user1, "user2": user2})
    else:
        col_friend.delete_many({"user1": user2, "user2": user1})


def find_users(col_users, fn: str, ln: str) -> list:
    if fn and ln:
        return list(col_users.find({"firstname": fn,
                                    "lastname": ln}))
    if fn:
        return list(col_users.find({"firstname": fn}))
    return list(col_users.find({"lastname": ln}))

def did_request(col_friend_req, user1, user2):
    return {"from": user2, "to": user1} in get_requests(col_friend_req, user1)

def is_friend(col_friends, user1, user2):
    return ((len(list(col_friends.find({"user1": user1, "user2": user2}))) != 0)
        or (len(list(col_friends.find({"user1": user2, "user2": user1}))) != 0))

def relation(col_friend_req, col_friends, user1, user2) -> int:
    if is_friend(col_friends, user1, user2):
        return 1
    if did_request(col_friend_req, user1, user2):
        return 2
    return 0

def relation_str(rel: int) -> str:
    if rel == 1:
        return "Remove friend"
    if rel == 2:
        return "Accept friend"
    else:
        return "Add friend"

def rel_text(col_friend_req, col_friends, user1, user2):
    return relation_str(relation(col_friend_req, col_friends, user1, user2))

def write_comment(col_comments, post, user, text) -> None:
    col_comments.insert_one({"post": post,
                             "user": user,
                             "text": text})

def comment_to_str(comment: dict) -> str:
    res = user_to_str(comment["user"]) + " wrote:\n"
    res += comment["text"]

    return res

def get_comments(col_comments, post) -> list:
    return list(col_comments.find({"post": post}))

