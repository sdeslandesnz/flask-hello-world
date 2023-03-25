import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
"""from flask_session import Session"""
from tempfile import mkdtemp
import datetime
import pandas as pd
from lastfm import lastfm
from werkzeug.wrappers import Response
from io import StringIO
import csv


# Configure application
app = Flask(__name__)

@app.route("/", methods =["GET","POST"])

def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        """print("hello")"""
        username = request.form.get('username')
        songs = request.form.get('songs')
        period = request.form.get('period')
        pc = request.form.get('pc')
        filter = request.form.get('filter')



        file = lastfm(username, songs, period, filter)
        """print(file)"""

        def generate(x):
            data = StringIO()
            w = csv.writer(data)

            # write header
            if pc == 'T':
                w.writerow(('Song', 'Artist','Playcount'))
            else:
                w.writerow(('Song', 'Artist'))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

            # write each log item
            for item in x:
                if pc =='T':
                    w.writerow((
                        item[0],
                        item[1],
                        item[2]
                    ))
                else:
                    w.writerow((
                        item[0],
                        item[1],
                    ))

                yield data.getvalue()
                data.seek(0)
                data.truncate(0)

            # stream the response as the data is generated
        response = Response(generate(file), mimetype='text/csv')
        # add a filename
        response.headers.set("Content-Disposition", "attachment", filename=username+"'s Top "+str(songs)+" "+period+".csv")
        return response

        """return render_template('index.html')"""





@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return redirect('/')

"""if __name__=="__main__":
    app.run(debug=True)"""
