import datetime
import os
from flask import Flask,render_template ,redirect, url_for , request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/',methods = ["POST","GET","DELETE","PUT"])
def home():
	if(request.method == 'GET'):
		data = {'text' : "lalalalala"}

		return jsonify(data)


	text = "hahahahahahaha"
	return render_template("sup.html",rows = [text])

if __name__ == '__main__':
	app.run(debug=False,host='0.0.0.0',port = 8000,threaded=True)

