from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


@app.route("/pounds", methods=["POST"])
def pounds():
    form = request.get_json(force=True)
    print(form)
    code = form["code"]
    requests_per_day = form["requests_per_day"]

    response = {}
    response["pounds"] = 0 # TODO: alfredo(code, requests_per_day)
    return jsonify(response)

if __name__ == "__main__":
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.run()
