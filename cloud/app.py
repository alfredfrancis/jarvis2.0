import os

# Disable Deprecation Warnings
import warnings
warnings.simplefilter('ignore', DeprecationWarning)

# Flask
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Response
import pandas as pd

# Sci-kit learn libraries for Logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

import csv
import json

# Initialize Flask
app =Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
data_log = 'datasets/data.csv'
json_file = 'datasets/switch.json'

#*************************************Login & Sessions*************************************
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['user'] = 'admin'
			return redirect(url_for('home'))		
	return render_template('index.html', error = error)

@app.route('/home', methods=['GET'])
def home():
	if session.get('user') == 'admin':
		return render_template('home.html')
	return redirect(url_for('login'))		

@app.route('/logout', methods=['GET'])
def logout():
	session['user'] = None
	session.clear()	
	return redirect(url_for('login'))	

# Read json database
def read_db():
    json_db = open(json_file, 'r')
    json_db.seek(0);
    data = json_db.read()
    json_db.close()	
    return data

def write_db(data):
    json_db = open(json_file, 'w')
    json_db.seek(0)
    json_db.write(data)
    json_db.close()	
    return "1"

#*************************************Request processing*************************************
@app.route('/req', methods=['GET'])
def req():
	python_obj = json.loads(read_db())
	python_obj[request.args['bname']] = request.args['bstatus']	
	write_db(json.dumps(python_obj, ensure_ascii=False))
	return "1"


@app.route('/req_rasp', methods=['GET'])
def req_rasp():
    python_obj = json.loads(read_db())
    python_obj['t'] = request.args['t']
    python_obj['h'] = request.args['h']
    python_obj['m'] = request.args['m']
    python_obj['l'] = request.args['l']
    python_obj['c'] = request.args['c']
    data= json.dumps(python_obj, ensure_ascii=False)	
    write_db(data)
    return "1"	

@app.route('/instance', methods=['GET'])
def instance():
    data = read_db()
    return Response(response=data,status=200,mimetype="application/json")

#*************************************Machine learning**************************************
@app.route("/dump",methods=['GET'])
def dump():
    csvfile = open(data_log, 'rb')
    output = csvfile.read()
    csvfile.close()
    return Response(output, mimetype='text')

@app.route("/reset",methods=['GET'])
def reset():
    json_db = open(json_file, 'w+')
    json_db.write('{"f1": "0", "c": "0", "ai": "0", "h": "0", "m": "0", "l": "0", "t": "0", "b2": "0", "b1": "0"}')
    json_db.close()
    return "1"

@app.route("/insert", methods=['GET'])
def insert():	
    python_obj = json.loads(read_db())
    out_file = open(data_log,'a+')																													
    out_file.write('\n'+str(python_obj['l']) + ','
    			+ str(python_obj['m']) + ','
	    		+ str(python_obj['t']) + ','
	    		+ str(python_obj['h']) + ','
	    		+ str(python_obj['c']) + ','
	    		+ str(python_obj['b1']) + ','
	    		+ str(python_obj['b2']) + ','
	    		+ str(python_obj['f1']))
    out_file.close()
    return '1'


@app.route("/predict", methods=['GET'])
def predict():
    python_obj = json.loads(read_db())
    if(python_obj['ai'] !='1'): 		
    	return "0"
    features_input = [
        float(python_obj['l']),
        float(python_obj['c']),
        float(python_obj['m'])
    ]

  	#	Prediction using Model
    _model = joblib.load('models/b1.pkl')
    python_obj['b1'] = _model.predict(features_input)[0]

    _model = joblib.load('models/b2.pkl')
    python_obj['b2'] = _model.predict(features_input)[0]

    features_input = [
	    float(python_obj['t']),
	    float(python_obj['h']),
	    float(python_obj['m'])
    ]
    _model = joblib.load('models/f1.pkl')
    python_obj['f1'] = _model.predict(features_input)[0]

    write_db(json.dumps(python_obj, ensure_ascii=False)) 	
    return "1" 


@app.route("/generate", methods=['GET'])
def generate():
	data = pd.read_csv(data_log)

	# setting target value
	_bulb1 = data['b1']
	target = _bulb1.values

	# setting features for prediction
	numerical_features = data[['l', 'c', 'm']]

	# converting into numpy arrays
	features_array = numerical_features.values

	# performing logistic regression,creating model
	logreg = LogisticRegression(C=1)
	logreg.fit(features_array, target)

	# dump generated model to file
	joblib.dump(logreg, 'models/' +'b1.pkl', compress=3)

	# Generate Model for Bulb2
	_bulb2 = data['b2']
	target = _bulb2.values
	numerical_features = data[['l', 'c', 'm']]
	features_array = numerical_features.values

	logreg = LogisticRegression(C=1)
	logreg.fit(features_array, target)
	joblib.dump(logreg, 'models/' +'b2.pkl', compress=3)

	# Generate Model for Fan1
	_fan1 = data['f1']
	target = _fan1.values
	numerical_features = data[['t', 'h', 'm']]
	features_array = numerical_features.values

	logreg = LogisticRegression(C=1)
	logreg.fit(features_array, target)
	joblib.dump(logreg, 'models/' +'f1.pkl', compress=3)

	return 'Models Generated'


if __name__ == "__main__":
	app.debug = True
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port,debug=True)
