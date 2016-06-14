# hsc-countdown
# Copyright (C) 2016 Simon Shields
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import flask
import json
import os
import yaml

from flask import Flask, render_template, make_response, session, redirect, request
from functools import wraps

os.environ['TZ'] = 'Australia/Sydney' # force the right timezone

app = Flask(__name__)

with open('subjects.json') as f:
    subjects = sorted(json.loads(f.readline()))
with open('data.json') as f:
    exam_json = f.readline().strip()
    exam_data = json.loads(exam_json)

NUM_SUBJECT_COLS = 3
n = len(subjects)//NUM_SUBJECT_COLS
subject_cols = [subjects[i:i+n] for i in range(0, len(subjects), n)]
subject_cols[-2]+= (subjects[n*NUM_SUBJECT_COLS:])

with open('config.yml') as c:
    cfg = yaml.load(c)

def etagged(fn):
    get_hash = lambda s: 'W/"' + str(hash(s)) + "$" + str(len(s)) + '"'

    @wraps(fn)
    def tag(*args, **kwargs):
        test = None
        if 'If-None-Match' in flask.request.headers:
            test = flask.request.headers['If-None-Match']
        orig_resp = fn(*args, **kwargs)
        if type(orig_resp) == str:
            hash = get_hash(orig_resp)
            if hash == test:
                print("NOT MODIFIED")
                res = make_response()
                res.status = 'Not Modified'
                res.status_code = 304
                return res
            res = make_response(orig_resp)
            res.headers['ETag'] = hash
            return res
        elif orig_resp is not None:
            o = orig_resp.get_data(as_text=True)
            hash = get_hash(o)
            if hash == test:
                res = make_response()
                res.status = 'Not Modified'
                res.status_code = 304
                return res
            orig_resp.headers['ETag'] = hash
            return orig_resp
        print("None response from etagged function!")
        flask.abort(404)
    return tag

def nocache(fn):
    @wraps(fn)
    def uncache(*args, **kwargs):
        orig_resp = fn(*args, **kwargs)
        if type(orig_resp) != Flask.response_class:
            orig_resp = make_response(orig_resp)
        orig_resp.headers['Prgama'] = 'no-cache'
        orig_resp.headers['Expires'] = 'Sat, 26 Jul 1997 05:00:00 GMT'
        orig_resp.headers['Cache-Control'] = 'no-cache, must-revalidate'
        return orig_resp
    return uncache

# routes
@app.route('/')
@etagged
def root():
    if 'nord' not in request.args:
        if request.cookies.get('cursubject'):
            return redirect('/' + request.cookies.get('cursubject'), code=302)
    return render_template('index.html', cur_letter='0', all_subjs=subjects, subjects=subject_cols, len=len, edata=exam_json)

@app.route('/<int:subj_id>')
@etagged
def countdown(subj_id):
    if subj_id >= len(subjects):
        return redirect('/', code=302)
    key = str(subj_id+1)
    resp = make_response(render_template('countdown.html', subject=exam_data[key][0]))
    resp.set_cookie('cursubject', str(subj_id))
    return resp

if __name__ == '__main__':
    app.run(debug=cfg['app']['debug'], threaded=True, port=cfg['net']['port'], host='0.0.0.0')
