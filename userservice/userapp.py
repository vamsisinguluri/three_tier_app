import os
from flask import Flask, jsonify
from utils.database import PostgresDatabase
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/')
def index():
    try:
        app_name = os.environ['APP_STATE']
        conn, host = PostgresDatabase().get_db_connection()
        if not conn:
            raise Exception("Could not able to connect to Database.")
        cur = conn.cursor()
        cur.execute('SELECT * FROM users;')
        records = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"data": records, "APPLICATION": app_name, "DB_HOST": host, "status": "success"})
    except Exception as e:
        print ("EXXXXXXXXXXXXXX", str(e))
        return jsonify({"status": "something wrong with service please try later"})



@app.route("/hello", methods=['GET'])
def hello():
    return jsonify({"message" : "Hello user!!..."})




# Route for the default page
@app.route("/insert", methods=['GET'])
@metrics.do_not_track()
def home():
    app_name = os.environ['APP_STATE']
    host = None
    obj = PostgresDatabase()
    try:
        host = obj.insert_userdata()
    except Exception as e:
        print("EEEEEEEEEEEEEEEEEEEEEEE", str(e))
        return jsonify({"data" : "Failed to insert data", "error": str(e)})
    return jsonify({"data": "successfully inserted data", "APPLICATION": app_name, "DB_HOST": host})



if __name__ == '__main__':
    app.run(debug=True)