# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:35:19 2022

@author: Stang
"""

from flask import Flask, render_template, jsonify, request, send_file

from src.imagelego_utils import ImageToLego


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/build",methods=["POST"])
def build():
    if request.method == 'POST':
        
        file = request.files['image']
        converter = ImageToLego(file.stream)
        
        instructions = converter.get_instructions()
        
        return jsonify(instructions)


if __name__ == "__main__":
    app.run(debug=True)
