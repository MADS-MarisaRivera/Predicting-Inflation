import pandas as pd
import numpy as np
import sklearn
import joblib
from flask import Flask,render_template,request
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from gevent.pywsgi import WSGIServer
import requests
import json
import prettytable
import pickle
import shap
from io import BytesIO
import matplotlib.pyplot as plt
import base64
from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab, CatTargetDriftTab, RegressionPerformanceTab


#with open('data_dev.txt', 'w') as outfile:
#    json.dump(json_data, outfile)

#### produccion descomentar
#headers = {'Content-type': 'application/json'}
#data = json.dumps({"seriesid": ['SUUR0000SA0'],"startyear":"2012", "endyear":"2021"})
#p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
#json_data = json.loads(p.text)
#### produccion descomentar

#### produccion comentar:
with open('data_dev.txt') as json_file:
    json_data = json.load(json_file)
#### produccion comentar


x = []

for series in json_data['Results']['series']:
    #x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','

                
        if 'M01' <= period <= 'M12':
            #x.add_row([seriesId,year,period,value,footnotes[0:-1]])
            y = [seriesId,year,period,value,footnotes[0:-1]]
            x.append(y)


data_inf = pd.DataFrame(x)
cols=["series id","year","period","value","footnotes"]
data_inf.columns = cols
data_inf['value-1'] = data_inf['value'].shift(-1)
data_inf['value-3'] = data_inf['value'].shift(-3)
data_inf['value-6'] = data_inf['value'].shift(-6)
data_inf['value-12'] = data_inf['value'].shift(-12)
data_inf = data_inf.astype ({"series id": str,"year": int,"period":str,"value": float,"footnotes":str, "value-1": float, "value-3": float, "value-6": float, "value-12": float})
data_inf['var-1'] = data_inf['value']/data_inf['value-1']-1
data_inf['var-3'] = data_inf['value']/data_inf['value-3']-1
data_inf['var-6'] = data_inf['value']/data_inf['value-6']-1
data_inf['var-12'] = data_inf['value']/data_inf['value-12']-1
data_inf['var-1_lag'] = data_inf['var-1'].shift(-1)
data_inf['var-3_lag'] = data_inf['var-3'].shift(-1)
data_inf['var-6_lag'] = data_inf['var-6'].shift(-1)
data_inf['var-12_lag'] = data_inf['var-12'].shift(-1)
data_inf

X = data_inf[['var-1_lag','var-3_lag','var-6_lag','var-12_lag']][1:101]


with open(r"./model_xg.pkl", "rb") as input_file:
    model_xg = pickle.load(input_file)


def shap_plot (ind):
    explainer = shap.Explainer(model_xg)
    shap_values = explainer(X)
    p = shap.plots.waterfall(shap_values[ind], show = False )
    plt.savefig('static/shap.jpg')
    plt.close()
    return p

shap_plot(0)


data_drift_report = Dashboard(tabs = [DataDriftTab])
# modificar a data Lectura vs data modelo
data_drift_report.calculate(X,X, column_mapping = None)
data_drift_report.save("templates/drift.html")


#####
#buf = BytesIO()
#plt.savefig(buf,
#            format = "png",
#            dpi = 150,
#            bbox_inches = 'tight')
#dataToTake = base64.b64encode(buf.getbuffer()).decode("ascii")
#return dataToTake
#####

app=Flask(__name__)





@app.route('/')
def home():
    #test = 99
    preds = X.values.tolist()[0]
    model=open("model_inf.pkl","rb")
    lr_model=joblib.load(model)
    model_prediction=lr_model.predict([preds])			
    model_prediction=round(float(model_prediction),4)
    return render_template('home_temp.html',prediction=model_prediction)


@app.route('/drift')
def drift():
    return render_template('drift.html')


@app.route('/predict',methods=['GET','POST'])

def predict():
	if request.method =='POST':
		print(request.form.get('var_1'))
		print(request.form.get('var_2'))
		print(request.form.get('var_3'))
		print(request.form.get('var_4'))
#		print(request.form.get('var_5'))
		try:
			var_1=float(request.form['var_1'])
			var_2=float(request.form['var_2'])
			var_3=float(request.form['var_3'])
			var_4=float(request.form['var_4'])
#			var_5=float(request.form['var_5'])
			pred_args=[var_1,var_2,var_3,var_4]
			pred_arr=np.array(pred_args)
			preds = pred_arr
			print(pred_arr)
            
#			preds=pred_arr.reshape(1,-1)
#			preds = X.values.tolist()[0]
			model=open("model_inf.pkl","rb")
			lr2_model=joblib.load(model)
			model_prediction=lr2_model.predict([preds])			
			model_prediction=round(float(model_prediction),2)
		except ValueError:
			return "Please Enter valid values"
	return render_template('predict2.html',prediction=model_prediction)

if __name__=='__main__':
	app.run(host='0.0.0.0', debug=False)

	# Serve the app with gevent
    #http_server = WSGIServer(('0.0.0.0', 5000), app)
    #http_server.serve_forever()
