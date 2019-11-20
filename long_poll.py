import datetime
import os
from flask import Flask,render_template ,redirect, url_for , request, jsonify
from flask_cors import CORS
import sqlite3 as sql
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
import numpy as np
import re


app = Flask(__name__)
CORS(app)


@app.route('/',methods = ["POST","GET","DELETE","PUT"])
def home():
	if(request.method == 'GET'):
		f = open('db/home.txt')
		data = f.read()
		end_len = len(data)
		old_m_time = os.path.getmtime('db/home.txt')

		while(True):
			new_m_time = os.path.getmtime('db/home.txt')
			if(new_m_time > old_m_time):
				f = open('db/home.txt')
				data = f.read()
				new_data = {'text':''.join(list(data)[end_len:])}
				#new_data = {'text' : data}
				end_len = len(data)
				old_m_time = new_m_time
				print(new_data)

				return jsonify(new_data)

@app.route('/contact',methods = ["POST","GET","DELETE","PUT"])
def contact():
	contact_info = "<p>Contact : </p> <p>+91 9881422115 </p> <p>pruthvipatnala@gmail.com</p>"
	if(request.method == 'GET'):
		data = {'text': contact_info}
		return jsonify(data)


@app.route('/experiences/<place>/<count>', methods = ["POST","GET","DELETE","PUT"])
def experiences(place,count):

	if(request.method == 'GET'):
		conn = sql.connect('db/experiences.db')

		command = "SELECT * FROM experiences WHERE place='"+str(place)+"';"
		l = list(conn.execute(command))
		conn.commit()
		#print(l)
		exps = []
		for i in l:
			exps.append(i[3])

		count = int(count)
		if(count*5 <= len(exps)+4):

			exps = exps[(count-1)*5:(count-1)*5+5]
			s = '**'.join(exps)
			data = {'text' : s}
			print(data)
			return jsonify(data)
		else:
			return jsonify({'text':''})


@app.route('/add_experience/<place>/<category>', methods = ["POST","GET","DELETE","PUT"])
def add_experience(place,category):

	if(request.method == 'POST'):
		data = request.form['new_exp']
		#data = request.get_json(force=True)
		#print(data)

		conn = sql.connect('db/experiences.db')
		command = "SELECT COUNT(*) FROM experiences"
		count = list(conn.execute(command))[0][0]
		conn.commit()
		
		exp_id = str(count+1)
		experience = data

		command = "INSERT INTO experiences (exp_id, place, category, experience) values ('"+exp_id+"','"+place+"','"+category+"','"+experience+"')"
		conn.execute(command)
		conn.commit()

		# update the sentiment of the experience
		update_sentiment(exp_id,experience)

		return jsonify({'exp_id':exp_id, 'place':place, 'category':category, 'experience':experience})
		#return render_template(place+'.html')

def update_sentiment(exp_id,experience):

	#database part
	conn = sql.connect('db/experiences.db')

	experience = experience.lower()
	twt = [experience]
	twt = tokenizer.texts_to_sequences(twt)
	twt = pad_sequences(twt, maxlen=369, dtype='int32', value=0)

	sentiment = loaded_model.predict(twt,batch_size=1,verbose = 2)[0]

	if(np.argmax(sentiment) == 0):
		command = "INSERT INTO sentiments (exp_id, sentiment) values ('" +exp_id+ "','Negative')"
	elif(np.argmax(sentiment) == 1):
		command = "INSERT INTO sentiments (exp_id, sentiment) values ('" +exp_id+ "','Positive')"
	conn.execute(command)
	conn.commit()

@app.route('/get_trends', methods=["POST","GET","DELETE","PUT"])
def get_trends():

	#database connection
	conn = sql.connect('db/experiences.db')

	get_places = "SELECT DISTINCT place from experiences"
	places = list(conn.execute(get_places))
	places = [i[0] for i in places]
	conn.commit()


	categories = {"family": ['alwar', 'kulumanali', 'nainital', 'shilong'], "hills": ['almora', 'coorg', 'darjeeling', 'dharamsala'], "leisure" : ['allepey', 'chandigarh', 'chikmagalur', 'kochi']}
	place_ids_map = {}
	place_sentiment_map = {}
	for place in places:
		get_exp_ids = "SELECT exp_id FROM experiences WHERE place = '"+place+"'"
		exp_ids = list(conn.execute(get_exp_ids))
		exp_ids = [i[0] for i in exp_ids]
		conn.commit()
		place_ids_map[place] = exp_ids

		neg_count = 0
		pos_count = 0
		for exp_id in exp_ids:
			get_sentiments = "SELECT sentiment FROM sentiments WHERE exp_id = '"+str(exp_id)+"'"
			try:
				sentiment = list(conn.execute(get_sentiments))[0][0]
				conn.commit()
			except:
				sentiment = "Don't Know"
			if sentiment == "Negative":
				neg_count += 1
			elif sentiment == 'Positive':
				pos_count += 1

		place_sentiment_map[place] = {'Negative' : neg_count, 'Positive' : pos_count}

	positive_percent = lambda x : round(x['Positive']/(x['Positive'] + x['Negative']) * 100,2)
	trending_places_by_category = {}
	for category in categories.keys():
		pos_counts = [(i,positive_percent(place_sentiment_map[i])) for i in categories[category]]
		pos_counts.sort(key = lambda x: x[1])
		pos_counts.reverse()
		pos_counts = [{i[0]: i[1]} for i in pos_counts]
		trending_places_by_category[category] = pos_counts



	return jsonify({'data':trending_places_by_category})



@app.route('/test',methods = ["POST","GET","DELETE","PUT"])
def test():
	return jsonify({})

if __name__ == '__main__':
	data = pd.read_csv('sentiment_analysis/processed_reviews.csv')
	data['text'] = data['text'].apply(lambda x: x.lower())
	data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
	max_fatures = 2000
	tokenizer = Tokenizer(num_words=max_fatures, split=' ')
	tokenizer.fit_on_texts(data['text'].values)

	# load model
	
	# load json and create model
	json_file = open('sentiment_analysis/model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights("sentiment_analysis/model.h5")
	loaded_model._make_predict_function()




	app.run(debug=False,host='0.0.0.0',port = 8000,threaded=True)

