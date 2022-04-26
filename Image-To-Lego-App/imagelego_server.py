# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:35:19 2022

@author: Stang
"""

from flask import Flask, render_template, jsonify, request, send_file

from src.imagelego_utils import ImageToLego


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


_question_key = [
    f"clue_{i+1}_{j+1}" for i in range(10) for j in range(5)
]

""" _question_key = list(zip(_question_key, [
    f"answer_{i+1}_{j+1}" for i in range(10) for j in range(5)
])) """

_question_key.extend([
    "clue_f_j"
   # "answer_f_j"
])

_categories = [
    f"category_{i+1}" for i in range(10)
]

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
