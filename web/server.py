import os, shutil, subprocess, time, uuid
import flask

app = flask.Flask(__name__)

ip_limit = {}

def process_tex(save, content):
    os.chdir('data')

    with open(f'{save}.tex', 'w') as inf:
        inf.write(content)
    
    with subprocess.Popen(['../../dlatex.py', f'{save}.tex', 'json'], stdout=subprocess.PIPE) as dlatex:
        reply = dlatex.stdout.read().decode('utf-8', 'ignore')

        reply = reply[:-2] + f', "save": "{save}"}}'

        os.chdir('..')
        return flask.Response(reply, mimetype = 'application/json')

    os.chdir('..')
    return flask.jsonify({'fail' : 'Could not run dLaTeX.'})

@app.route('/')
def route_index():
    return flask.render_template('index.html')

@app.route('/dlatex', methods=['POST'])
def route_dlatex():
    if flask.request.remote_addr in ip_limit and (int(time.time()) - ip_limit[flask.request.remote_addr]) < 5:
        return 'Your IP is being rate-limited', 429
    
    ip_limit[flask.request.remote_addr] = int(time.time())

    save = str(uuid.uuid4())
    resp = process_tex(save, flask.request.data.decode('utf-8', 'ignore'))
    shutil.move(f'data/{save}.pdf', f'static/{save}.pdf')
    
    return resp

if __name__ == '__main__':
    app.run()