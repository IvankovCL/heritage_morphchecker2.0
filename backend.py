DEFAULT_PORT = 9000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID


from flask import Flask, render_template, request, jsonify
from morphchecker import Morphchecker

flask_app = Flask(__name__)

def do_some_morphchecking(text):
    m = Morphchecker()
    results = m.text_mcheck(text)

    to_save = ''
    for result in results:
        to_save += str(result) + '\n'

    to_show = " ".join([result[0]
                      if len(result[1]) == 1 and result[1][0][0] == 0
                      else '<error title="{0}">{1}</error>'.format("\n".join([r[1] for r in result[1]]), result[0])
                      for result in results])

    return to_save, to_show

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/about')
def about():
    return render_template('about.html')

@flask_app.route('/data', methods=['GET', 'POST'])
def data():
    request.get_data()
    given_text = request.data.decode('utf-8')
    try:
        to_save, to_show = do_some_morphchecking(given_text)
    except:

        return jsonify({
            'to_show': 'none',
            'to_save': ''
        })

    return jsonify({
            'to_show': to_show,
            'to_save': to_save
    })

if __name__ == '__main__':
    flask_app.run(port=getuid() + ADDITIVE_FOR_UID)