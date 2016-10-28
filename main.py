# -*- coding: utf-8 -*-

DEFAULT_PORT = 9000
ADDITIVE_FOR_UID = 1000

try:
    from os import getuid

except ImportError:
    def getuid():
        return DEFAULT_PORT - ADDITIVE_FOR_UID

from time import sleep

from celery import Celery
from flask import Flask, render_template, request, jsonify
import sys
sys.path.insert(0, '.\morphchecker')
import morphchecker

flask_app = Flask(__name__)
flask_app.config.update({
    'CELERY_BACKEND': 'rpc://', #'mongodb://localhost/celery',
    'CELERY_BROKER_URL': 'amqp://guest:guest@localhost:5672//'
})


def make_celery(app):
    celery = Celery('main', backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(flask_app)


@celery.task
def our_function(word):
    errors, isCorrect = morphchecker.spellcheck(word)
    return morphchecker.morphcheck(errors, isCorrect)


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/data', methods=['GET', 'POST'])
def data():
    request.get_data()
    givenWord = request.data.decode('utf-8')
    #task_id = our_function(givenWord)
    task_id = our_function.delay(givenWord)
    #async_result = celery.AsyncResult(task_id)

    return jsonify({
        #'answer': str(task_id.result),
        'task_id': str(task_id)
        #'answer': str(task_id[givenWord])
    })
	
@flask_app.route('/result/<task_id>')
def result(task_id):
    async_result = celery.AsyncResult(task_id)

    return jsonify({
        'ready': async_result.ready(),
        'status': async_result.status,
        'result': str(async_result.result),
        'task_id': str(async_result.task_id)
    })

if __name__ == '__main__':
    flask_app.run(port=getuid() + ADDITIVE_FOR_UID, debug=True)
