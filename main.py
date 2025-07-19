from flask import Flask, json, request, send_from_directory
from werkzeug.utils import secure_filename
import os

api = Flask(__name__)
api.debug = True if os.environ.get('DEBUG') else False
api.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', '/uploads')
port = os.environ.get('port', 3000)

@api.route('/filer', methods=['PUT', 'POST'])
def put():
    if 'file' not in request.files:
        return json.dumps({'code': 400, 'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return json.dumps({'code': 400, 'message':'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(api.config['UPLOAD_FOLDER'], filename))
        return json.dumps({'code': 201, 'message': filename}), 201
    return json.dumps({'code': 400, 'message':'Bad request'}), 400

@api.route('/filer/<path:filename>', methods=['GET'])
def get(filename):
    return send_from_directory(api.config['UPLOAD_FOLDER'], filename)

@api.route('/filer/<path:filename>', methods=['DELETE'])
def delete(filename):
    if not os.path.isfile(os.path.join(api.config['UPLOAD_FOLDER'], filename)):
       return json.dumps({'code': 404, 'message':'Not found'}), 404 
    os.remove(os.path.join(api.config['UPLOAD_FOLDER'], filename))
    return json.dumps({'code': 200, 'message':'OK'}), 200


@api.route('/filer-list', methods=['GET'])
def list():
    try: 
        result = os.listdir(os.path.join(api.config['UPLOAD_FOLDER']))
    except OSError as error:
        print(error)
        result = []
        pass #ignore errors
    return json.dumps({'files': result}), 200


if __name__ == '__main__':
    print('App running for "'+api.config['UPLOAD_FOLDER']+'" direcctory and listening on port "'+str(port)+'".')
    api.run('0.0.0.0', port=port)