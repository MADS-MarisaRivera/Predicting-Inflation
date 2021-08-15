
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/MADS-MarisaRivera/Predicting-Inflation">
    <img src="images/logo.jpg" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Predicting Inflation</h3>

  <p align="center">
    Data Products Creation & Deployment - Final Project
    <br />
    <a href="https://github.com/MADS-MarisaRivera/Predicting-Inflation"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#dataset-inputs">Dataset Inputs</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#dev">Dev</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

According to <a href="http://www.banguat.gob.gt/page/inflacion-total">Banco de Guatemala</a>, nowadays the country is reporting a 3.82% inflation at July2021, which is 0.94pp more than last year at July2020. At this point, it is important to enhance that inflation will always exist in our society, people have to learn to live with it. However, if we look at the definition of inflation itself:
<br/>
"<a href="https://www.investopedia.com/terms/i/inflation.asp">Inflation</a> is the decline of purchasing power of a given currency over time. A quantitative estimate of the rate at which the decline in purchasing power occurs can be reflected in the increase of an average price level of a basket of selected goods and services in an economy over some period of time. The rise in the general level of prices, often expressed as a percentage, means that a unit of currency effectively buys less than it did in prior periods."
<br/> 
<br/> 
In other words, inflation makes us feel that we can't afford as much as we could last year, mostly, when our incomes remain static from one year to another. This is why companies and customers must be open-eyed when it comes to inflation, because it has a direct impact on their purchasing power. 
<br/> 
<br/> 
Therefore, as a team of passionate members about analytics, we are seeking to predict the porcentual variance, between next month's inflation value and its last year's value, meaning -12 months, so that we can anticipate increasing inflation or decreasing inflation (deflation) periods. 
For example, when we predict deflation periods, we may promote in our companies & personal expenses, the perks of deflation, and buy more for less or, save the remaining money that we didn't spend in our regular purchases.
<br/> 
<br/> 
*This is how we learn to coexist with inflation behavior, in a way that we can also take the most of it when it's behavior moves in our favor.*


### Built With

* [Python](https://www.python.org)
* [Shap](https://shap.readthedocs.io/en/latest/index.html)
* [Bayesian Ridge Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_bayesian_ridge.html)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [PythonAnywhere](https://www.pythonanywhere.com)


<!-- DATASET -->
## Dataset Inputs
* [Data Source (JSON Output)](https://www.bls.gov/developers/api_python.htm#python1)
  ```sh
  import requests
  import json
  import prettytable
  import pandas as pd 
  headers = {'Content-type': 'application/json'}
  data = json.dumps({"seriesid": ['SUUR0000SA0'],"startyear":"2012", "endyear":"2021"})
  p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
  json_data = json.loads(p.text)
  for series in json_data['Results']['series']:
      cols=["series id","year","period","value","footnotes"]
      x=pd.DataFrame(columns = cols)
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
              x.append([seriesId,year,period,value,footnotes])
  ```
* Raw Data Sample
  ```
  {'status': 'REQUEST_SUCCEEDED',
   'responseTime': 230,
   'message': [],
   'Results': {'series': [{'seriesID': 'SUUR0000SA0',
      'data': [{'year': '2021',
        'period': 'M07',
        'periodName': 'July',
        'latest': 'true',
        'value': '153.424',
        'footnotes': [{'code': 'I', 'text': 'Initial'}]},
       {'year': '2021',
        'period': 'M06',
        'periodName': 'June',
        'value': '152.720',
        'footnotes': [{'code': 'U', 'text': 'Interim'}]},
       {'year': '2021',
        'period': 'M05',
        'periodName': 'May',
        'value': '151.405',
        'footnotes': [{'code': 'U', 'text': 'Interim'}]},
       {'year': '2021',
        'period': 'M04',
        'periodName': 'April',
        'value': '150.221',
        'footnotes': [{'code': 'U', 'text': 'Interim'}]}
  ]}]}}
  ```
* Model Input - Data Preparation Sample
    - series id: key
    - year: year
    - period: month
    - value: price index
    - footnotes: attached features
    - value-1: value from last month
    - value-3: value from 3 months ago
    - value-6: value from 6 months ago
    - value-12: value from 12 months ago
    - var-1: percentual delta from value and value-1
    - var-3: percentual delta from value and value-3
    - var-6: percentual delta from value and value-6
    - var-12: percentual delta from value and value-12

  | series id | year | period | value | footnotes | value-1	| value-3	| value-6 | value-12 | var-1 | var-3 | var-6 | var-12 | var-1_lag | var-3_lag	| var-6_lag	| var-12_lag |
  | --- | --- | --- | --- | --- | ---	| ---	| --- | --- | --- | --- | --- | --- | --- | ---	| ---	| --- |
  | SUUR0000SA0	| 2021 | M07 | 153.424 | Initial | 152.720 | 150.221 | 147.123 | 145.747 | 0.004610 | 0.021322 | 0.042828 | 0.052673 | 0.008685 |	0.025049 | 0.042621 | 0.054354 |
  | SUUR0000SA0	| 2021 | M06 | 152.720 | Interim | 151.405 | 148.988 | 146.477 | 144.847 | 0.008685 | 0.025049 | 0.042621 | 0.054354 | 0.007882 | 0.023373 | 0.034526 | 0.051292 |
  | SUUR0000SA0	| 2021 | M05 | 151.405 | Interim | 150.221 | 147.947 | 146.352 | 144.018 | 0.007882 | 0.023373 | 0.034526 | 0.051292 | 0.008276 | 0.021057 | 0.025672 | 0.042174 |
  | SUUR0000SA0	| 2021 | M04 | 150.221 | Interim | 148.988 | 147.123 | 146.461 | 144.142 | 0.008276 | 0.021057 | 0.025672 | 0.042174 | 0.007036 | 0.017143 | 0.017559	| 0.028120 |
  | SUUR0000SA0	| 2021 | M03 | 148.988 | Interim | 147.947 | 146.477 | 146.417 | 144.913 | 0.007036 | 0.017143 | 0.017559 | 0.028120 | 0.005601 | 0.010898 | 0.011465	| 0.018968 |


<!-- GETTING STARTED -->
## Getting Started

Follow this instructions to setup project.

### Prerequisites
* [python3.8 or later](https://www.python.org/downloads/)
* **shap**
  ```sh
  pip install shap
  ```
* **flask**
  ```sh
  pip install flask
  ```  
* **pandas**
  ```sh
  pip install pandas
  ```
* **numpy**
  ```sh
  pip install numpy
  ```
* **sklearn**
  ```sh
  pip install sklearn
  ```  
* **joblib**
  ```sh
  pip install joblib
  ```   
* **requests**
  ```sh
  pip install requests
  ```
* **json**
  ```sh
  pip install json
  ```
* **prettytable**
  ```sh
  pip install prettytable
  ```


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/MADS-MarisaRivera/Predicting-Inflation.git
   ```
2. Install Python 3.8 or later and Libraries
3. Open in any Python IDE, file app.py
4. Run this command at python console:
   ```sh
      python app.py
   ```
5. [PythonAnywhere Output](http://jrs.pythonanywhere.com)
  <img src="images/model_output.png" alt="App" width="850" height="300">


<!-- USAGE EXAMPLES -->
## Dev

* app.route/
  ```
  @app.route('/')
  def home():
      headers = {'Content-type': 'application/json'}
      data = json.dumps({"seriesid": ['SUUR0000SA0'],"startyear":"2012", "endyear":"2021"})
      p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
      json_data = json.loads(p.text)    

      x = []

      for series in json_data['Results']['series']:
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

      shap_plot(0,X,model_xg)


      data_drift_report = Dashboard(tabs = [DataDriftTab])

      data_drift_report.calculate(X,X, column_mapping = None)
      data_drift_report.save("templates/drift.html")

      preds = X.values.tolist()[0]
      model=open("model_inf.pkl","rb")
      lr_model=joblib.load(model)
      model_prediction=lr_model.predict([preds])			
      model_prediction=round(float(model_prediction),4)
      return render_template('home_temp.html',prediction=model_prediction)
  ```
  
* app.route/drift
  ```
  @app.route('/drift')
  def drift():
      return render_template('drift.html')
  ```
  
* app.route/predict
  ```
  @app.route('/predict',methods=['GET','POST'])

  def predict():
    if request.method =='POST':
      print(request.form.get('var_1'))
      print(request.form.get('var_2'))
      print(request.form.get('var_3'))
      print(request.form.get('var_4'))
      try:
        var_1=float(request.form['var_1'])
        var_2=float(request.form['var_2'])
        var_3=float(request.form['var_3'])
        var_4=float(request.form['var_4'])
        pred_args=[var_1,var_2,var_3,var_4]
        pred_arr=np.array(pred_args)
        preds = pred_arr
        print(pred_arr)

        model=open("model_inf.pkl","rb")
        lr2_model=joblib.load(model)
        model_prediction=lr2_model.predict([preds])			
        model_prediction=round(float(model_prediction),2)
      except ValueError:
        return "Please Enter valid values"
    return render_template('predict2.html',prediction=model_prediction)
  ```
  
* __main__  
  ```
  if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False)
  ```
