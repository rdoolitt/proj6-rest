import acp_times 
import config
import arrow
import flask
import csv
import os
import io
from flask import request, jsonify, Response, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient

app = flask.Flask(__name__)
api = Api(app)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

client = MongoClient("192.168.16.1", 27017)
db = client['controle_times']

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('calc.html')

@app.route("/_calc_times")
def _calc_times():
    km = request.args.get('km', 999, type=float)
    distance = request.args.get('distance', type=int)
    begin_date = request.args.get('begin_date')
    begin_time = request.args.get('begin_time')

    datetime_str = f"{begin_date} {begin_time}"
    start_time = arrow.get(datetime_str, "YYYY-MM-DD HH:mm")

    open_time = acp_times.open_time(km, distance, start_time.isoformat())
    close_time = acp_times.close_time(km, distance, start_time.isoformat())

    result = {"open": open_time, "close": close_time}
    return jsonify(result=result)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    controls = data.get('controls')
    distance = data.get('distance')
    begin_date = data.get('begin_date')
    begin_time = data.get('begin_time')

    if not controls:
        return jsonify(error="No entries provided")

    brevet = {
        "distance": distance,
        "begin_date": begin_date,
        "begin_time": begin_time,
        "controls": controls
    }
    
    db.brevets.insert_one(brevet)
    return jsonify(status="success")

@app.route("/display")
def display():
    brevets = list(db.brevets.find())
    if not brevets:
        return jsonify(error="No entries in the database")

    controls = []
    for brevet in brevets:
        controls.extend(brevet.get("controls", []))

    if not controls:
        return jsonify(error="No controls found in the database")

    return render_template('todo.html', items=controls)

class ListAll(Resource):
    def serialize_doc(self, doc):
        doc.pop('_id', None)
        return doc
    
    def to_csv(self, data, headers):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        for row in data:
            writer.writerow([row.get(header, '') for header in headers])
        return output.getvalue()

    def get(self, format=None):
        brevets = list(db.brevets.find())
        serialized_brevets = [self.serialize_doc(brevet) for brevet in brevets]

        if format == 'csv':
            headers = ['distance', 'begin_date', 'begin_time', 'controls']
            csv_data = self.to_csv(serialized_brevets, headers)
            response = Response(csv_data, mimetype='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=listAll.csv'
            return response
        else:
            return jsonify(serialized_brevets)

class ListOpenOnly(ListAll):
    def serialize_doc(self, doc):
        serialized_doc = super().serialize_doc(doc)
        for control in serialized_doc['controls']:
            control.pop('close', None)
        top = request.args.get('top', default=None, type=int)
        if top is not None:
            serialized_doc['controls'] = sorted(serialized_doc['controls'], key=lambda x: x['open'])[:top]
        else:
            serialized_doc['controls'] = sorted(serialized_doc['controls'], key=lambda x: x['open'])
        return serialized_doc

    def get(self, format=None):
        response = super().get(format=format)
        response.headers['Content-Disposition'] = 'attachment; filename=listOpenOnly.csv'
        if format != 'csv':
            serialized_brevets = response.json
            return jsonify(serialized_brevets)
        else:
            return response


class ListCloseOnly(ListAll):
    def serialize_doc(self, doc):
        serialized_doc = super().serialize_doc(doc)
        for control in serialized_doc['controls']:
            control.pop('open', None)
        top = request.args.get('top', default=None, type=int)
        if top is not None:
            serialized_doc['controls'] = sorted(serialized_doc['controls'], key=lambda x: x['close'])[:top]
        else:
            serialized_doc['controls'] = sorted(serialized_doc['controls'], key=lambda x: x['close'])
        return serialized_doc

    def get(self, format=None):
        response = super().get(format=format)
        response.headers['Content-Disposition'] = 'attachment; filename=listCloseOnly.csv'
        if format != 'csv':
            serialized_brevets = response.json
            return jsonify(serialized_brevets)
        else:
            return response


api.add_resource(ListAll, '/listAll', '/listAll/', '/listAll/<string:format>', '/listAll/<string:format>/')
api.add_resource(ListOpenOnly, '/listOpenOnly', '/listOpenOnly/', '/listOpenOnly/<string:format>', '/listOpenOnly/<string:format>/')
api.add_resource(ListCloseOnly, '/listCloseOnly', '/listCloseOnly/', '/listCloseOnly/<string:format>', '/listCloseOnly/<string:format>/')

if __name__ == '__main__':
    db.brevets.drop()
    app.run(host='0.0.0.0', port=5000, debug=True)