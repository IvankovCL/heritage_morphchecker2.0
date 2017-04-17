DEFAULT_PORT = 9000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID


from flask import Flask, render_template, request, jsonify
from morphchecker import Morphchecker
import re

flask_app = Flask(__name__)

def do_some_morphchecking(word):
    m = Morphchecker()
    results = m.text_mcheck(word)
    return " ".join([result[0]
                      if len(result[1]) == 1 and result[1][0][0] == 0
                      else '<error title="{0}">{1}</error>'.format("\n".join([str(r) for r in result[1]]), result[0])
                      for result in results])



@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/data', methods=['GET', 'POST'])
def data():
    request.get_data()
    given_text = request.data.decode('utf-8')
    task_id = do_some_morphchecking(given_text)

    return jsonify({
         'result': str(task_id)
    })

@flask_app.route('/show_file', methods=['GET', 'POST'])
def show_file():
    request.get_data()
    given_file = request.data.decode('utf-8')

    return 

if __name__ == '__main__':
    flask_app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)