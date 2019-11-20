import datetime
import random
import sqlite3 as sql

conn = sql.connect('experiences.db')

conn.execute("CREATE TABLE experiences ( \
	exp_id	TEXT NOT NULL, \
	place	TEXT,\
	category TEXT,\
	experience	TEXT, \
	PRIMARY KEY(exp_id)\
);")

conn.execute("CREATE TABLE sentiments (\
	exp_id	TEXT NOT NULL, \
	sentiment TEXT,\
	PRIMARY KEY(exp_id)\
	);")


places = ['alwar', 'kulumanali', 'nainital', 'shilong', 'almora', 'coorg', 'darjeeling', 'dharamsala', 'allepey', 'chandigarh', 'chikmagalur', 'kochi']
categories = ['family', 'hills', 'leisure']

s = "abcdefghijklmnopqrstuvwxyz"

l = [i for i in s]
alphabets = dict()

for i in range(1,27):
    alphabets[i] = l[i-1]

def get_exp():
	exp = []
	length = random.randint(1,100)
	for i in range(length):
		aplha_index = random.randint(1,26)
		exp.append(alphabets[aplha_index])

	return ''.join(exp)

sentiments = ['Negative', 'Positive']

# for i in range(120):
# 	insert_command = "INSERT INTO experiences (exp_id, place, category, experience) values ('"+str(i)+"','"+places[i%12]+"','"+categories[(i%12)//4]+"','"+get_exp()+"')"
# 	conn.execute(insert_command)
# 	conn.commit()

# 	sentiment_command = "INSERT INTO sentiments (exp_id,sentiment) values ('"+str(i)+"','"+sentiments[random.randint(0,1)]+"')"
# 	conn.execute(sentiment_command)
# 	conn.commit()


