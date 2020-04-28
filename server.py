from flask_cors import CORS
import os
from flask import Flask, redirect, jsonify, send_from_directory, abort, request, redirect, url_for
from backend.generator import loadMetadata, loadHNSW, gen_random, gen_url_from_uid
app = Flask(__name__, static_folder='ui/build')

# Local Web Dev Allow CORS
CORS(app)

# API
@app.route('/gen/', defaults={'uid': None})
@app.route('/gen', defaults={'uid': None})
@app.route('/gen/<string:uid>', methods=["GET"])
def generateImages(uid):
    print(f'[GEN]', uid)
    pageNumber = request.args.get('pageNumber', default=1, type=int)
    srcDoc, res = gen_random(uid, pageNumber)
    if res is False:
        return abort(404)
    else:
        return jsonify(sample=res, srcDoc=srcDoc)


# Serve React App
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serveReact(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/url', defaults={'uid': ''})
@app.route('/url/<string:uid>')
def redirectToDocumentURL(uid):
    url = gen_url_from_uid(uid)
    print(f'{uid} -> {url}')

    if url is None:
        return abort(404)

    return redirect(url)


# Trigger Server
if __name__ == '__main__':
    # Preparation
    index = 57000
    loadMetadata(index)
    loadHNSW(index)
    # Production Mode
    app.run(
        host='0.0.0.0',
        port=1234,
        # debug=True  # Development Mode
    )
