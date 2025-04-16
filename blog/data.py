import sqlite3
from blog.models import Post, User
from datetime import datetime


def get_post_page(page, per_page):
    with sqlite3.connect('blog.db') as conn:  # Open connection
        if page == 1:
            has_prev_page = False
        else:
            has_prev_page = True    
        
        cursor = conn.cursor()
        cursor.execute("SELECT POST.*,USER.IMAGE FROM POST join  USER ON POST.USER_ID = USER.ID  LIMIT ? OFFSET ?;", (per_page+1, (page-1) * per_page))
        lista = cursor.fetchall()
        if len(lista) > per_page:
            has_next_page = True    
        else:
             has_next_page = False  

        lista_post = [] 
        for post in lista[:per_page]:
            new_post=post_from_list_to_obj(post)
            lista_post.append(new_post)
               
    return   lista_post, has_prev_page, has_next_page  # Connection is automatically closed here

def post_insert(post):
     with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO POST (user_id, title, description, body, markdown, image) \
                        VALUES (?, ?, ?, ?, ?, ?);",( post.user_id, post.title, post.description, post.body, post.markdown, post.image  ))
        conn.commit()
        return cursor.lastrowid

def get_user(username):
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USER WHERE USERNAME = ?;", (username,))
        lista = cursor.fetchall()
        if len(lista) > 0:  
            return  user_from_list_to_obj(lista[0]) 
        else:
            return None

def get_user_by_id(id):
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USER WHERE ID = ?;", (id,))
        #print(id)
        lista = cursor.fetchall()
        return  user_from_list_to_obj(lista[0])                

def user_insert(user):
     with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO USER (nome, cognome, username, email, password, image) \
                        VALUES (?, ?, ?, ?, ?, ?);",( user.nome, user.cognome, user.username, user.email, user.password,  user.image  ))
        conn.commit()   

def get_post(post_id):
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM POST WHERE ID = ?;", (str(post_id)))
        lista = cursor.fetchall()
        if len(lista) > 0:  
            return post_from_list_to_obj(lista[0]) 
        else:
            return None

def upadate_post(post):
     with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE POST SET user_id= ?, title= ?, description= ?, body= ?, markdown=?, image=? WHERE id =?",
                       (post.user_id, post.title, post.description, post.body, post.markdown, post.image, post.id))
        conn.commit()

def delete_post(post_id):
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM POST WHERE ID = ?;", (post_id,))
        conn.commit()

def post_from_list_to_obj(post):
    new_post =  Post()
    new_post.id=post[0]
    new_post.user_id=post[1]
    formato = "%Y-%m-%d %H:%M:%S.%f"
    if post[2]==None:
        new_post.created_at  =  datetime.now()
    else:
        new_post.created_at = datetime.strptime(post[2], formato)
    
    new_post.title=post[3]
    new_post.description=post[4]
    new_post.body=post[5]
    new_post.image=post[6]
    new_post.markdown=post[7] 
    return new_post

def user_from_list_to_obj(user):
    new_user =  User()
    new_user.id = user[0]
    formato = "%Y-%m-%d %H:%M:%S.%f"
    if user[1]==None:
        new_user.created_at  =  datetime.now()
    else:
        new_user.created_at = datetime.strptime(user[1], formato)
    new_user.username=user[2]
    new_user.email=user[3]
    new_user.password=user[4]
    new_user.nome= user[5]
    new_user.cognome=user[6]  
    new_user.image = user[7]
    return new_user
    
