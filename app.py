from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from profiler_parser import profile_and_parse
from energyConsumed import CO2e, metric
from grammar import from_profile

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
    code = form["code"]
    requests_per_day = int(form["requests_per_day"])
    inst_name = form["inst_name"]

    print(code)
    print(requests_per_day)
    print(inst_name)

    profiler_output = profile_and_parse(code)
    print(profiler_output)
    pounds = CO2e(profiler_output.total_time, requests_per_day, inst_name)

    suggestions = from_profile(profiler_output.lines)
    suggestions_dict = map(lambda x: { line: x[0], start: x[1], end: x[2] })
    print(suggestions)
    response = {}
    response["pounds"] = pounds
    respinse["suggestions"] = suggestions_dict
    return jsonify(response)


@app.route("/metrics", methods=["GET"])
def getMetrics():
    pounds = float(request.args.get('pounds'))
    metrics = metric(pounds)

    response = {}
    response["impacts"] = metrics
    return jsonify(response)


if __name__ == "__main__":
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.run()
