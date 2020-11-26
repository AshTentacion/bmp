from flask import Flask, request
from db import Db
import json
import time

app = Flask(__name__)


@app.route('/')
def get_all_infos():
    print("heell")
    ret = test_db.select_all()
    dict = {}
    for index, data in enumerate(ret):
        data_dict = {}
        data_dict['id'] = data[0]
        data_dict['temp'] = data[1]
        data_dict['pressure'] = data[2]
        data_dict['time'] = data[3].strftime("%Y-%m-%d %H:%M:%S")
        data_dict['creator'] = data[4]
        dict['data' + str(index)] = data_dict
    return json.dumps(dict)


@app.route('/insert')
def insert_data():
    now = int(time.time())
    timeArray = time.localtime(now)
    data = [request.args.get('temp'), request.args.get('pressure'),
            time.strftime("%Y-%m-%d %H:%M:%S", timeArray), request.args.get('creator')]
    test_db.insert(data)

    return 'ok'


if __name__ == '__main__':
    test_db = Db()
    test_db.create_table()
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )
