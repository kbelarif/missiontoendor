#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 2 11:26:01 2019

@author: kamel
"""
from flask import Flask, render_template, request
from werkzeug import secure_filename
import functions as f
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/',methods = ['POST','GET'])
def result():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == 'empire.json':
            file.save(secure_filename(file.filename))
            l= list()
            l = f.CreateDataList()
            if l == False or l[-1].proba == 0:
                return render_template('doom.html')
            else:
                li = list()
                proba = l[-1].proba
                for elt in l:
                    if elt.proba == proba:
                        li.append(elt.path)
                le = len(li)
                return render_template('result.html', proba = l[-1].proba, li=li,le=le)
        else:
            return render_template('wrong_file.html')

if __name__ == '__main__':
   app.run(debug = True)