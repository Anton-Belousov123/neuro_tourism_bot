import json

def get_order_info(chat_id):
    db = json.load(open(file='database.json', mode='r', encoding='UTF-8'))
    if chat_id not in db.keys():
        db[chat_id] = 1
        with open(file='database.json', mode='w', encoding='UTF-8') as f:
            f.write(json.dumps(db))
        f.close()
    return db[chat_id]



def plus_one(chat_id):
    db = json.load(open(file='database.json', mode='r', encoding='UTF-8'))
    db[chat_id] += 1
    with open(file='database.json', mode='w', encoding='UTF-8') as f:
        f.write(json.dumps(db))
    f.close()


def restart(chat_id):
    db = json.load(open(file='database.json', mode='r', encoding='UTF-8'))
    db.pop(chat_id)
    with open(file='database.json', mode='w', encoding='UTF-8') as f:
        f.write(json.dumps(db))
    f.close()