import glob, os, shutil, subprocess, threading, time, uuid
import flask

app = flask.Flask(__name__)

ip_limit = {}

def safe_remove(file):
    if os.path.exists(file):
        os.remove(file)

def safe_move(src, dst):
    if os.path.exists(src):
        shutil.move(src, dst)

def process_tex(save, content):
    os.chdir('data')

    with open(f'{save}.tex', 'w') as inf:
        inf.write(content)
    
    with subprocess.Popen(['../../dlatex.py', f'{save}.tex', 'json'], stdout=subprocess.PIPE) as dlatex:
        reply = dlatex.stdout.read().decode('utf-8', 'ignore')

        pdf = 'true' if os.path.exists(f'data/{save}.pdf') else 'false'
        reply = reply[:-2] + f', "save": "{save}", "pdf": {pdf}}}'

        os.chdir('..')
        return flask.Response(reply, mimetype = 'application/json')

    os.chdir('..')
    return flask.jsonify({'fail' : 'Could not run dLaTeX.'})

def clean_files(save):
    for file in glob.glob(f'data/{save}.*'):
        safe_remove(file)

    safe_remove(f'static/{save}.pdf')
    safe_remove(f'static/{save}.txt')

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
    safe_move(f'data/{save}.pdf', f'static/{save}.pdf')
    safe_move(f'data/{save}.log', f'static/{save}.txt')

    clean = threading.Timer(15.0, clean_files, args = (save, ))
    clean.start()
    
    return resp

if __name__ == '__main__':
    app.run()