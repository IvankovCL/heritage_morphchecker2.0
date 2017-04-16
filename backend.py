DEFAULT_PORT = 9000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID

from time import sleep
from flask import Flask, render_template, request, jsonify
# import sys
# sys.path.insert(0, '.\morphchecker')
from morphchecker import Morphchecker
import re

flask_app = Flask(__name__)

def do_some_morphchecking(word):
    m = Morphchecker()
    return m.mcheck(word)


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/data', methods=['GET', 'POST'])
def data():
    request.get_data()
    givenWord = request.data.decode('utf-8')
    task_id = do_some_morphchecking(givenWord)

    return jsonify({
         'result': str(task_id)
    })

if __name__ == '__main__':
    flask_app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)
