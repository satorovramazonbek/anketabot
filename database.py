import sqlite3 as sq


async def db_start():
    global db, cur
    db = sq.connect('anketa_bot_database.db')
    cur = db.cursor()
    cur.execute(
          "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, count_parent INTEGER, fio TEXT, study TEXT, birthday TEXT, country TEXT, millati TEXT, partiyaviylik TEXT, malumoti TEXT, tamomlagan TEXT, mutaxassislik TEXT, language TEXT, mukofot TEXT, saylov TEXT, mehnat_faoliyati TEXT, qarindoshlari TEXT)")
    db.commit()

async def create_parentbase(user_id):
    db = sq.connect("anketa_bot_database.db")
    cur = db.cursor()
    query = f"CREATE TABLE IF NOT EXISTS parent{user_id} (id INTEGER PRIMARY KEY AUTOINCREMENT, qarindoshligi TEXT, fio TEXT, birthday TEXT, work TEXT, location TEXT)"
    cur.execute(query)
    db.commit()

# create_parentbase("l123","отаси,онаси,укаси,акаси")

async def insert_parentbase(user_id, qarindosh):
    cur.execute(
        f"INSERT INTO parent{user_id}(qarindoshligi, fio, birthday, work, location) VALUES(?, ?, ?, ?, ?)",
        (qarindosh, 'o', 'o', 'o', 'o'))
    db.commit()
async def update_parent(user_id, columname, parent, qiymat):
    cur.execute(f"UPDATE parent{user_id} SET {columname} = ? WHERE qarindoshligi = ?", (qiymat, parent))
    db.commit()

async def update_user(user_id, columname, columvalue):
    cur.execute(f"UPDATE users SET {columname} = ? WHERE user_id = ?", (columvalue, int(user_id)))
    db.commit()

async def add_acet(user_id, count_parent):
    cur.execute(
        'INSERT INTO users(user_id,count_parent, fio, study, birthday, country, millati, partiyaviylik, malumoti, tamomlagan, mutaxassislik, language, mukofot, saylov, mehnat_faoliyati, qarindoshlari) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (int(user_id), count_parent, '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0','otasi, onasi'))
    db.commit()

async def check_user(user_id):
    cur.execute(
        "SELECT count_parent FROM users WHERE user_id = ?", (int(user_id),)
    )
    count_parent = cur.fetchone()
    return count_parent[0] if count_parent else None

async def select_user(user_id, value):
    cur.execute(
        f"SELECT {value} FROM users WHERE user_id = ?", (user_id,)
    )
    valuser = cur.fetchone()
    return valuser[0] if valuser else None

# async def sele_parent(user_id, value,parent): #parent bazasidan qiymatni olish
#     cur.execute(
#         f"SELECT {value} FROM parent{user_id}  WHERE qarindoshligi = ?", (parent)
#     )
#     valparent = cur.fetchone()
#     return valparent if valparent else None
async def sele_parent(user_id, value, parent):
    # Use parameterized query to avoid SQL injection
    cur.execute(
        f"SELECT {value} FROM parent{user_id} WHERE qarindoshligi = ?",
        (parent,)
    )
    valparent = cur.fetchone()
    return valparent[0] if valparent else None


def remove_db(user_id):
    db = sq.connect("anketa_bot_database.db")
    cur = db.cursor()
    try:
        cur.execute(f"DROP TABLE IF EXISTS parent{user_id}")
        print(f"Таблица parent{user_id} успешно удалена из базы данных.")
    except sq.Error as e:
        print(f"Ошибка при удалении таблицы parent{user_id}: {e}")
    finally:
        db.commit()
        db.close()

# remove_db("123")