import datetime
import os
from flask import Flask,render_template ,redirect, url_for , request, jsonify
from flask_cors import CORS


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



if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0',port = 8000,threaded=True)

