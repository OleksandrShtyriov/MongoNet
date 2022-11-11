from datetime import datetime
import tkinter as tk

from functions import *

def login_screen(col_users, col_posts, col_reacts, 
                 col_friend_req, col_friends,
                 col_comments, col_comment_reacts,
                 window):
    window.title("Login")

    lbl_welcome = tk.Label(text="Welcome to MongoNet!",
                           width=20,
                           height = 10)
    lbl_welcome.pack()

    lbl_email = tk.Label(text="Email:")
    ent_email = tk.Entry(width=50)

    lbl_pw = tk.Label(text="Password:")
    ent_pw = tk.Entry(width=50)
    
    lbl_email.pack()
    ent_email.pack()
    lbl_pw.pack()
    ent_pw.pack()

    lbl_user = tk.Label(text="")
    lbl_user.pack()

    def hide():
        lbl_welcome.pack_forget()
        lbl_email.pack_forget()
        lbl_pw.pack_forget()
        lbl_user.pack_forget()
        ent_email.pack_forget()
        ent_pw.pack_forget()
        btn_login.pack_forget()
        btn_reg.pack_forget()


    def handle_login(event):
        logged = False

        try:
            user = login(col_users, ent_email.get(), ent_pw.get())
            logged = True
        except Exception as e:
            user = str(e)

        if not logged:
            lbl_user.config(text=user, bg="red")

        if logged:
            hide()
            main_screen(col_users, col_posts, col_reacts, 
                        col_friend_req, col_friends,
                        col_comments, col_comment_reacts,
                        window, user)

    def handle_reg(event):
        hide()
        reg_screen(col_users, col_posts, col_reacts, 
                   col_friend_req, col_friends,
                   col_comments, col_comment_reacts,
                   window)
        
    btn_login = tk.Button(text="Login")
    btn_login.bind("<Button-1>", handle_login)
    btn_login.pack()

    btn_reg = tk.Button(text="Register")
    btn_reg.bind("<Button-1>", handle_reg)
    btn_reg.pack()

def reg_screen(col_users, col_posts, col_reacts, 
               col_friend_req, col_friends,
               col_comments, col_comment_reacts,
               window):
    window.title("Register")

    lbl_welcome = tk.Label(text="Register to MongoNet",
                           width=20,
                           height = 10)
    lbl_welcome.pack()

    lbl_email = tk.Label(text="Email*:")
    ent_email = tk.Entry(width=50)

    lbl_pw = tk.Label(text="Password*:")
    ent_pw = tk.Entry(width=50)

    lbl_fn = tk.Label(text="First name*:")
    ent_fn = tk.Entry(width=50)
    
    lbl_ln = tk.Label(text="Last name*:")
    ent_ln = tk.Entry(width=50)

    lbl_in = tk.Label(text="Interests:")
    ent_in = tk.Entry(width=50)

    lbl_email.pack()
    ent_email.pack()
    lbl_pw.pack()
    ent_pw.pack()
    lbl_fn.pack()
    ent_fn.pack()
    lbl_ln.pack()
    ent_ln.pack()
    lbl_in.pack()
    ent_in.pack()

    lbl_err = tk.Label(text="")
    lbl_err.pack()
    
    def hide():
        lbl_welcome.pack_forget()
        lbl_email.pack_forget()
        lbl_pw.pack_forget()
        lbl_err.pack_forget()
        lbl_fn.pack_forget()
        lbl_ln.pack_forget()
        lbl_in.pack_forget()
        ent_email.pack_forget()
        ent_pw.pack_forget()
        ent_fn.pack_forget()
        ent_ln.pack_forget()
        ent_in.pack_forget()
        btn_login.pack_forget()
        btn_reg.pack_forget()

    def handle_reg(event):
        email = ent_email.get()
        pw = ent_pw.get()
        fn = ent_fn.get()
        ln = ent_ln.get()
        interests = ent_in.get().split()

        if email and pw and fn and ln:
            insert_user(col_users, email, pw, fn, ln, interests)
            user = login(col_users, email, pw)
            hide()
            main_screen(col_users, col_posts, col_reacts, 
                        col_friend_req, col_friends,
                        col_comments, col_comment_reacts,
                        window, user)
        else:
            lbl_err.config(bg="red", text="Not all fields are filled!")

    def handle_login(event):
        hide()
        login_screen(col_users, col_posts, col_reacts, 
                     col_friend_req, col_friends,
                     col_comments, col_comment_reacts,
                     window)

    btn_reg = tk.Button(text="Register")
    btn_reg.bind("<Button-1>", handle_reg)
    btn_reg.pack()

    btn_login = tk.Button(text="Login")
    btn_login.bind("<Button-1>", handle_login)
    btn_login.pack()

def main_screen(col_users, col_posts, col_reacts, 
                col_friend_req, col_friends,
                col_comments, col_comment_reacts,
                window, user):
    window.title("Mongonet")

    posts_raw = col_posts.find().sort("time", -1)
    posts = posts_to_str(col_posts)
    i = 0

    lbl_post = tk.Label(text=posts[i])
    lbl_post.place(relx=0.5, rely=0.5, anchor="center")

    lbl_react = tk.Label(text=get_reacts_str(col_reacts, posts_raw[i]))
    lbl_react.pack(side=tk.BOTTOM)

    def hide():
        btn_next.pack_forget()
        btn_prev.pack_forget()
        btn_write.pack_forget()
        btn_like.pack_forget()
        btn_view.pack_forget()
        btn_friend.pack_forget()
        lbl_post.destroy()
        lbl_react.destroy()
        btn_comment.destroy()

    def handle_next(event):
        nonlocal i

        i += 1
        lbl_post.config(text=posts[i])

        lbl_react.config(text=get_reacts_str(col_reacts, posts_raw[i]))

        if i == 1:
            btn_prev.pack(side=tk.LEFT)
        if i == len(posts) - 1:
            btn_next.pack_forget()

    def handle_prev(event):
        nonlocal i

        i -= 1
        lbl_post.config(text=posts[i])

        lbl_react.config(text=get_reacts_str(col_reacts, posts_raw[i]))

        if i == len(posts) - 2:
            btn_next.pack(side=tk.RIGHT)
        if i == 0:
            btn_prev.pack_forget()

    def handle_write(event):
        hide()
        post_screen(col_users, col_posts, col_reacts, 
                    col_friend_req, col_friends,
                    col_comments, col_comment_reacts,
                    window, user)

    def handle_like(event):
        if user not in get_users(col_reacts, posts_raw[i]):
            react(col_reacts, posts_raw[i], user)
        else:
            unreact(col_reacts, posts_raw[i], user)

        lbl_react.config(text=get_reacts_str(col_reacts, posts_raw[i]))

    def handle_view(event):
        hide()
        user_screen(col_users, col_posts, col_reacts, 
                    col_friend_req, col_friends,
                    col_comments, col_comment_reacts,
                    window, user, posts_raw[i]["user"])

    def handle_friend(event):
        hide()
        friend_screen(col_users, col_posts, col_reacts, 
                      col_friend_req, col_friends,
                      col_comments, col_comment_reacts,
                      window, user)

    def handle_comment(event):
        hide()
        comment_screen(col_users, col_posts, col_reacts, 
                       col_friend_req, col_friends,
                       col_comments, col_comment_reacts,
                       window, user, posts_raw[i])

    btn_next = tk.Button(text="Next post >")
    btn_next.bind("<Button-1>", handle_next)
    if len(posts) > 1:
        btn_next.pack(side=tk.RIGHT)

    btn_prev = tk.Button(text="< Previous post")
    btn_prev.bind("<Button-1>", handle_prev)

    btn_write = tk.Button(text="Write a post")
    btn_write.bind("<Button-1>", handle_write)
    btn_write.pack(side=tk.TOP)

    btn_like = tk.Button(text="Like")
    btn_like.bind("<Button-1>", handle_like)
    btn_like.pack(side=tk.TOP)

    btn_view = tk.Button(text="View user profile")
    btn_view.bind("<Button-1>", handle_view)
    btn_view.pack(side=tk.TOP)

    btn_friend = tk.Button(text="Friend requests")
    btn_friend.bind("<Button-1>", handle_friend)
    btn_friend.pack(side=tk.TOP)

    btn_comment = tk.Button(text="View comments")
    btn_comment.bind("<Button-1>", handle_comment)
    btn_comment.pack(side=tk.TOP)

def post_screen(col_users, col_posts, col_reacts, 
                col_friend_req, col_friends,
                col_comments, col_comment_reacts,
                window, user):
    window.title("Post")

    lbl_title = tk.Label(text="Title:")
    lbl_title.pack()

    ent_title = tk.Entry()
    ent_title.pack()
    
    lbl_text = tk.Label(text="Text:")
    lbl_text.pack()

    txt_text = tk.Text()
    txt_text.pack()

    lbl_error = tk.Label(text="")
    lbl_error.pack()

    def handle_submit(event):
        title = ent_title.get()
        text = txt_text.get("1.0", "end")

        if title and text:
            write_post(col_posts, datetime.now(), title, text, user)
            to_main()
        else:
            lbl_error.config(text="Not all fields are filled!", bg="red")

    def handle_back(event):
        to_main()

    def to_main():
        lbl_title.pack_forget()
        ent_title.pack_forget()
        lbl_text.pack_forget()
        txt_text.pack_forget()
        btn_submit.pack_forget()
        btn_back.pack_forget()
        lbl_error.pack_forget()

        main_screen(col_users, col_posts, col_reacts, 
                    col_friend_req, col_friends,
                    col_comments, col_comment_reacts,
                    window, user)

    btn_submit = tk.Button(text="Submit")
    btn_submit.bind("<Button-1>", handle_submit)
    btn_submit.pack()

    btn_back = tk.Button(text = "< Back")
    btn_back.bind("<Button-1>", handle_back)
    btn_back.pack(side=tk.LEFT)

def user_screen(col_users, col_posts, col_reacts, 
                col_friend_req, col_friends,
                col_comments, col_comment_reacts,
                window, user, author):
    window.title(user_to_str(user))

    posts_raw = list(col_posts.find({"user": author}).sort("time", -1))
    posts = list(map(post_to_str, posts_raw))

    i = 0

    lbl_post = tk.Label(text=posts[i])
    lbl_post.place(relx=0.5, rely=0.5, anchor="center")

    lbl_react = tk.Label(text=get_reacts_str(col_reacts, posts_raw[i]))
    lbl_react.pack(side=tk.BOTTOM)

    def handle_next(event):
        nonlocal i

        i += 1
        lbl_post.config(text=posts[i])

        lbl_react.config(text=get_reacts_str(col_reacts, posts_raw[i]))

        if i == 1:
            btn_prev.pack(side=tk.LEFT)
        if i == len(posts) - 1:
            btn_next.pack_forget()

    def handle_prev(event):
        nonlocal i

        i -= 1
        lbl_post.config(text=posts[i])

        lbl_react.config(text=get_reacts_str(col_reacts, posts_raw[i]))

        if i == len(posts) - 2:
            btn_next.pack(side=tk.RIGHT)
        if i == 0:
            btn_prev.pack_forget()

    def handle_like(event):
        if user not in get_users(col_reacts, posts_raw[i]):
            react(col_reacts, posts_raw[i], user)
        else:
            unreact(col_reacts, posts_raw[i], user)

        lbl_react.config(text=get_reacts_str(col_reacts, posts_raw[i]))

    def handle_back(event):
        lbl_post.destroy()
        lbl_react.destroy()

        btn_next.pack_forget()
        btn_prev.pack_forget()
        btn_like.pack_forget()
        btn_back.destroy()

        main_screen(col_users, col_posts, col_reacts, 
                    col_friend_req, col_friends,
                    col_comments, col_comment_reacts,
                    window, user)

    btn_next = tk.Button(text="Next post >")
    btn_next.bind("<Button-1>", handle_next)
    if len(posts) > 1:
        btn_next.pack(side=tk.RIGHT)

    btn_prev = tk.Button(text="< Previous post")
    btn_prev.bind("<Button-1>", handle_prev)

    btn_like = tk.Button(text="Like")
    btn_like.bind("<Button-1>", handle_like)
    btn_like.pack(side=tk.TOP)

    btn_back = tk.Button(text="< Back")
    btn_back.bind("<Button-1>", handle_back)
    btn_back.place(anchor=tk.NW)

def friend_screen(col_users, col_posts, col_reacts, 
                  col_friend_req, col_friends,
                  col_comments, col_comment_reacts,
                  window, user):
    window.title("Friend requests")

    req_raw = get_requests(col_friend_req, user)
    req = list(map(request_to_str, req_raw))
    i = 0

    lbl_req = tk.Label(text=(req[i] if len(req) else ""))
    lbl_req.place(relx=0.5, rely=0.5, anchor="center")

    def hide():
        lbl_req.destroy()

        btn_next.pack_forget()
        btn_prev.pack_forget()
        btn_back.destroy()
        btn_accept.pack_forget()
        btn_deny.pack_forget()
        btn_add.pack_forget()


    def handle_next(event):
        nonlocal i

        i += 1
        lbl_req.config(text=req[i])

        if i == 1:
            btn_prev.pack(side=tk.LEFT)
        if i == len(req) - 1:
            btn_next.pack_forget()

    def handle_prev(event):
        nonlocal i

        i -= 1
        lbl_req.config(text=req[i])

        if i == len(req) - 2:
            btn_next.pack(side=tk.RIGHT)
        if i == 0:
            btn_prev.pack_forget()

    def handle_back(event):
        hide()
        main_screen(col_users, col_posts, col_reacts,
                    col_friend_req, col_friends,
                    col_comments, col_comment_reacts,
                    window, user)

    def handle_add(event):
        hide()
        add_screen(col_users, col_posts, col_reacts,
                   col_friend_req, col_friends,
                   col_comments, col_comment_reacts,
                   window, user)

    def handle_accept(event):
        accept(col_friend_req, col_friends, req_raw[i]["from"], user)
        hide()
        friend_screen(col_users, col_posts, col_reacts,
                      col_friend_req, col_friends,
                      col_comments, col_comment_reacts,
                      window, user)

    def handle_deny(event):
        deny(col_friend_req, col_friends, req_raw[i]["from"], user)
        hide()
        friend_screen(col_users, col_posts, col_reacts,
                      col_friend_req, col_friends,
                      col_comments, col_comment_reacts,
                      window, user)

    btn_next = tk.Button(text="Next request >")
    btn_next.bind("<Button-1>", handle_next)
    if len(req) > 1:
        btn_next.pack(side=tk.RIGHT)

    btn_prev = tk.Button(text="< Previous request")
    btn_prev.bind("<Button-1>", handle_prev)

    btn_back = tk.Button(text="< Back")
    btn_back.bind("<Button-1>", handle_back)
    btn_back.place(anchor=tk.NW)

    btn_add = tk.Button(text="Add a friend")
    btn_add.bind("<Button-1>", handle_add)
    btn_add.pack(side=tk.TOP)

    btn_accept = tk.Button(text="Accept")
    btn_accept.bind("<Button-1>", handle_accept)

    btn_deny = tk.Button(text="Deny")
    btn_deny.bind("<Button-1>", handle_deny)

    if len(req) > 0:
        btn_accept.pack(side=tk.BOTTOM)
        btn_deny.pack(side=tk.BOTTOM)

def add_screen(col_users, col_posts, col_reacts,
               col_friend_req, col_friends,
               col_comments, col_comment_reacts,
               window, user):
    lbl_find = tk.Label(text="Find a friend: ")
    lbl_find.pack(side=tk.TOP)

    lbl_fn = tk.Label(text="First name:")
    lbl_fn.pack(side=tk.TOP)

    ent_fn = tk.Entry()
    ent_fn.pack(side=tk.TOP)

    lbl_ln = tk.Label(text="Last name:")
    lbl_ln.pack(side=tk.TOP)

    ent_ln = tk.Entry()
    ent_ln.pack(side=tk.TOP)

    lbl_err = tk.Label()
    lbl_err.pack(side=tk.TOP)

    def hide():
        lbl_find.pack_forget()
        lbl_fn.pack_forget()
        lbl_ln.pack_forget()
        ent_fn.pack_forget()
        ent_ln.pack_forget()
        lbl_err.pack_forget()
        btn_submit.pack_forget()
        btn_back.destroy()

    def handle_submit(event):
        fn = ent_fn.get()
        ln = ent_ln.get()

        if not(fn or ln):
            lbl_err.config(text="Wrong values", bg="red")
        else:
            res = find_users(col_users, fn, ln)
            hide()

            search_result_screen(col_users, col_posts, col_reacts,
                                 col_friend_req, col_friends,
                                 col_comments, col_comment_reacts,
                                 window, user, res)

    def handle_back(event):
        hide()
        friend_screen(col_users, col_posts, col_reacts,
                      col_friend_req, col_friends,
                      col_comments, col_comment_reacts,
                      window, user)

    btn_submit = tk.Button(text="Submit")
    btn_submit.bind("<Button-1>", handle_submit)
    btn_submit.pack(side=tk.TOP)

    btn_back = tk.Button(text="< Back")
    btn_back.bind("<Button-1>", handle_back)
    btn_back.place(anchor=tk.NW)

def search_result_screen(col_users, col_posts, col_reacts,
                         col_friend_req, col_friends,
                         col_comments, col_comment_reacts,
                         window, user, fr):
    window.title("Results")

    fr_raw = fr
    fr = list(map(user_to_str, fr_raw))

    i = 0

    lbl_fr = tk.Label(text=(fr[i] if len(fr) else ""))
    lbl_fr.place(relx=0.5, rely=0.5, anchor="center")

    def hide():
        lbl_fr.destroy()

        btn_next.pack_forget()
        btn_prev.pack_forget()
        btn_back.destroy()

        try:
            btn_add.destroy()
        except: 
            pass

    def handle_next(event):
        nonlocal i

        i += 1
        lbl_fr.config(text=fr[i])

        btn_add.config(text=rel_text(col_friend_req, col_friends, fr_raw[i],
                                     user))

        if i == 1:
            btn_prev.pack(side=tk.LEFT)
        if i == len(fr) - 1:
            btn_next.pack_forget()

    def handle_prev(event):
        nonlocal i

        i -= 1
        lbl_fr.config(text=fr[i])
        
        btn_add.config(text=rel_text(col_friend_req, col_friends, fr_raw[i],
                                     user))

        if i == len(fr) - 2:
            btn_next.pack(side=tk.RIGHT)
        if i == 0:
            btn_prev.pack_forget()

    def handle_back(event):
        hide()
        add_screen(col_users, col_posts, col_reacts,
                   col_friend_req, col_friends,
                   col_comments, col_comment_reacts,
                   window, user)

    def handle_add(event):
        rel = relation(col_friend_req, col_friends, fr_raw[i], user)

        if rel == 1:
            remove_friend(col_friends, user, fr_raw[i])
        elif rel == 2:
            accept(col_friend_req, col_friends, fr_raw[i], user)
        else:
            if not did_request(col_friend_req, user, fr_raw[i]):
                send_request(col_friend_req, user, fr_raw[i])

        hide()
        search_result_screen(col_users, col_posts, col_reacts,
                             col_friend_req, col_friends,
                             col_comments, col_comment_reacts,
                             window, user, fr_raw)

    btn_next = tk.Button(text="Next result >")
    btn_next.bind("<Button-1>", handle_next)

    if len(fr) > 1:
        btn_next.pack(side=tk.RIGHT)

    btn_prev = tk.Button(text="< Previous result")
    btn_prev.bind("<Button-1>", handle_prev)

    btn_back = tk.Button(text="< Back")
    btn_back.bind("<Button-1>", handle_back)
    btn_back.place(anchor=tk.NW)

    if len(fr_raw):
        btn_add = tk.Button(text=rel_text(col_friend_req, col_friends, fr_raw[i],
                                      user))
        btn_add.bind("<Button-1>", handle_add)

    if len(fr):
        btn_add.pack(side=tk.BOTTOM)

def comment_screen(col_users, col_posts, col_reacts,
                   col_friend_req, col_friends,
                   col_comments, col_comment_reacts,
                   window, user, post):
    comments_raw = get_comments(col_comments, post)
    comments = list(map(comment_to_str, comments_raw))

    i = 0
    
    lbl_comment = tk.Label(text=(comments[i] if len(comments) else ""))
    lbl_comment.place(relx=0.5, rely=0.5, anchor="center")

    lbl_react = tk.Label(text=get_reacts_str(col_comment_reacts, 
                                             comments_raw[i]) if len(comments)
                                                              else "")
    lbl_react.pack(side=tk.BOTTOM)

    def handle_next(event):
        nonlocal i

        i += 1
        lbl_comment.config(text=comments[i])

        if i == 1:
            btn_prev.pack(side=tk.LEFT)
        if i == len(comments) - 1:
            btn_next.pack_forget()

        lbl_react.config(text=get_reacts_str(col_comment_reacts,
                                             comments_raw[i]))

    def handle_prev(event):
        nonlocal i

        i -= 1
        lbl_comment.config(text=comments[i])
        
        if i == len(comments) - 2:
            btn_next.pack(side=tk.RIGHT)
        if i == 0:
            btn_prev.pack_forget()

        lbl_react.config(text=get_reacts_str(col_comment_reacts,
                                             comments_raw[i]))

    def handle_like(event):
        if user not in get_users(col_comment_reacts, comments_raw[i]):
            react(col_comment_reacts, comments_raw[i], user)
        else:
            unreact(col_comment_reacts, comments_raw[i], user)

        lbl_react.config(text=get_reacts_str(col_comment_reacts,
                                             comments_raw[i]))

    def hide():
        btn_back.destroy()
        btn_next.destroy()
        btn_prev.destroy()
        btn_write.destroy()
        lbl_comment.destroy()
        btn_like.destroy()
        lbl_react.destroy()

    def handle_back(event):
        hide()
        main_screen(col_users, col_posts, col_reacts,
                    col_friend_req, col_friends,
                    col_comments, col_comment_reacts,
                    window, user)

    def handle_write(event):
        hide()
        write_comment_screen(col_users, col_posts, col_reacts,
                             col_friend_req, col_friends,
                             col_comments, col_comment_reacts,
                             window, user, post)

    btn_back = tk.Button(text="< Back")
    btn_back.bind("<Button-1>", handle_back)
    btn_back.place(anchor=tk.NW)

    btn_next = tk.Button(text="Next result >")
    btn_next.bind("<Button-1>", handle_next)

    if len(comments) > 1:
        btn_next.pack(side=tk.RIGHT)

    btn_prev = tk.Button(text="< Previous result")
    btn_prev.bind("<Button-1>", handle_prev)

    btn_write = tk.Button(text="Write a comment")
    btn_write.bind("<Button-1>", handle_write)
    btn_write.pack(side=tk.TOP)

    btn_like = tk.Button(text="Like")
    btn_like.bind("<Button-1>", handle_like)
    btn_like.pack(side=tk.TOP)

def write_comment_screen(col_users, col_posts, col_reacts,
                         col_friend_req, col_friends,
                         col_comments, col_comment_reacts,
                         window, user, post):
    lbl_title = tk.Label(text="Write a comment:")
    lbl_title.pack()

    txt_text = tk.Text()
    txt_text.pack()

    lbl_err = tk.Label()
    lbl_err.pack()

    def hide():
        lbl_title.pack_forget()
        btn_back.destroy()
        txt_text.pack_forget()
        lbl_err.pack_forget()
        btn_submit.pack_forget()

    def handle_submit(event):
        text = txt_text.get("1.0", "end")

        if not text:
            lbl_err.config(text="Fill the textbox")
            return

        hide()
        write_comment(col_comments, post, user, text)
        comment_screen(col_users, col_posts, col_reacts,
                       col_friend_req, col_friends,
                       col_comments, col_comment_reacts,
                       window, user, post)

    def handle_back(event):
        hide()
        comment_screen(col_users, col_posts, col_reacts,
                       col_friend_req, col_friends,
                       col_comments, col_comment_reacts,
                       window, user, post)

    btn_back = tk.Button(text="< Back")
    btn_back.bind("<Button-1>", handle_back)
    btn_back.place(anchor=tk.NW)

    btn_submit = tk.Button(text="Submit")
    btn_submit.bind("<Button-1>", handle_submit)
    btn_submit.pack()

