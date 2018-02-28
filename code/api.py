import csv
import json
from flask import Flask, request
from flask_restful import Resource, Api, abort

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

if __name__ == '__main__':
	app.run()