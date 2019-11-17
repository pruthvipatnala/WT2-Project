import datetime
import os
from flask import Flask,render_template ,redirect, url_for , request, jsonify
from flask_cors import CORS
import sqlite3 as sql


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

			exps = exps[(count-1)*5:(count-1)*5+4]
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

		return jsonify({'exp_id':exp_id, 'place':place, 'category':category, 'experience':experience})
		#return render_template(place+'.html')


@app.route('/test',methods = ["POST","GET","DELETE","PUT"])
def test():
	return jsonify({})

if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0',port = 8000,threaded=True)

