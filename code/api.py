import csv
import json

csvfile = open('../data/daily.csv', 'r')
jsonfile = open('../data/out/weather.json', 'w')

reader = csv.DictReader(csvfile)
out = json.dumps([row for row in reader])
jsonfile.write(out)
data = json.loads(out)
