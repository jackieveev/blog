from flask import Response, json, request, abort
from functools import wraps

# json response
def json_response(data):
  res = data if isinstance(data, dict) else { 'data': data }
  return Response(json.dumps(res), mimetype='application/json')