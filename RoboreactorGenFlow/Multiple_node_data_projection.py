import os
import sys
import json
from flask import Flask, request, jsonify, render_template, url_for, redirect
app = Flask(__name__)
data_transfer = {}


@app.route('/Multiplenode_logic', methods=['GET', 'POST'])
def index():
    input_json = request.get_json(force=True)
    head_function = list(input_json)[0]
    data_transfer[head_function] = input_json.get(head_function)
    return jsonify(data_transfer)


@app.route('/get_Multiplenode_logic')
def get_multiple_node():
    return jsonify(data_transfer)


app.run(debug=True, threaded=True, host='0.0.0.0', port=5340)
