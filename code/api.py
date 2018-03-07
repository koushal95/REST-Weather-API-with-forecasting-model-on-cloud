import csv
import json
from flask import Flask, request
from flask_restful import Resource, Api, abort
from datetime import datetime
import pandas as pd
import numpy as np
from fbprophet import Prophet

csvfile = open('../data/daily.csv', 'r')
jsonfile = open('../data/out/weather.json', 'w')

reader = csv.DictReader(csvfile)
out = json.dumps([row for row in reader])
jsonfile.write(out)
data = json.loads(out)

app = Flask(__name__)
api = Api(app)

class ListAllDates(Resource):
    def get(self):
        res = []
        for i in range(len(data)):
            res.append({"DATE" : data[i]["DATE"]})
        return res

    def post(self):
        data.append(request.get_json(force=True))
        return {"DATE" : request.get_json(force=True)["DATE"]}, 201

api.add_resource(ListAllDates, '/historical/')

class InfoForDate(Resource):
    def get(self, date):
        for i in range(len(data)):
            if data[i]['DATE'] == date:
                return data[i]
        abort(404, message="No weather information for date {} is available.".format(date))

    def delete(self, date):
        for i in range(len(data)):
            if data[i]['DATE'] == date:
                del data[i]
                break
        return "", 204

api.add_resource(InfoForDate, '/historical/<string:date>')

class Forecast(Resource):
    def get(self, date):
        res = []
        for i in range(len(data)):
            if data[i]['DATE'] == date:
                if i + 6 <= len(data)-1:
                    # whole data is already available
                    for j in range(7):
                        res.append(data[i + j])
                    return res
                elif i == len(data)-1:
                    # input date is last value in our data
                    res.append(data[i])
                    periods = 6
                    return_value = make_predictions(periods, date, True)
                    prediction_json = json.loads(return_value)
                    for j in range(6):
                        res.append(prediction_json[j])
                    return res
                else:
                    # few dates available
                    last_date_string = data[len(data)-1]['DATE']
                    last_date = datetime.strptime(last_date_string, '%Y%m%d')
                    input_date = datetime.strptime(date, '%Y%m%d')
                    days_available = (last_date - input_date).days + 1 ## increment 1 if including date in URL
                    periods = 7 - days_available
                    return_value = make_predictions(periods, last_date_string, True)
                    prediction_json = json.loads(return_value)
                    for j in range(days_available):
                        res.append(data[i+j])
                    for k in range(periods):
                        res.append(prediction_json[k])
                    return res

        #date not found that means future date
        last_date_string = data[len(data)-1]['DATE']
        last_date = datetime.strptime(last_date_string, '%Y%m%d')
        future_date = datetime.strptime(date, '%Y%m%d')
        periods = (future_date - last_date).days + 6
        return_value = make_predictions(periods, date, False)
        res = json.loads(return_value)
        return res

api.add_resource(Forecast, '/forecast/<string:date>')

def make_predictions(periods, input_date, next):
    weather_data = pd.read_csv("../data/daily.csv")
    # converting date string to datetime object
    weather_data["DATE"] = pd.to_datetime(weather_data["DATE"], format='%Y%m%d')
    # creating dataframe for Tmax
    tmax_df = weather_data.loc[:, 'DATE':'TMAX']
    # changing column names for Prophet
    tmax_df.columns = ['ds', 'y']
    # creating dataframe for Tmin
    tmin_df = weather_data.loc[:, ['DATE', 'TMIN']]
    # changing column names for Prophet
    tmin_df.columns = ['ds', 'y']
    # creating model for Tmax
    model_tmax = Prophet()
    model_tmax.fit(tmax_df)
    # creating model for Tmin
    model_tmin = Prophet()
    model_tmin.fit(tmin_df)
    # creating future dataframe (date indices) for Tmax
    future_tmax = model_tmax.make_future_dataframe(periods=periods, include_history=False)
    # making predictions for Tmax
    predictions_tmax = model_tmax.predict(future_tmax)
    # creating future dataframe for Tmin
    future_tmin = model_tmin.make_future_dataframe(periods=periods, include_history=False)
    # making predictions for Tmin
    predictions_tmin = model_tmin.predict(future_tmin)
    # pretty predictions
    predictions_tmax_res = predictions_tmax.loc[:, ['ds', 'yhat']]
    predictions_tmin_res = predictions_tmin.loc[:, ['ds', 'yhat']]
    # concatenating the predictions of Tmax and Tmin
    frames = [predictions_tmax_res, predictions_tmin_res.yhat]
    result = pd.concat(frames, axis=1)
    # resetting column names to our format
    result.columns = ["DATE", "TMAX", "TMIN"]
    # returing only the result we need 
    if next == True:
        return_value = result.loc[result['DATE'] > datetime.strptime(input_date, '%Y%m%d')]
    else:
        return_value = result.loc[result['DATE'] >= datetime.strptime(input_date, '%Y%m%d')]
    # since json exporting makes date objects messy, converting datetime as string
    return_value['DATE'] = return_value['DATE'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
    # exporting the result dataframe to json format
    json_format_result = return_value.to_json(orient='records', double_precision=1)
    return json_format_result

if __name__ == '__main__':
	app.run()