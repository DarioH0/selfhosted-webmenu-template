# Required:
try:
    from flask import Flask, jsonify, render_template, send_from_directory
except:
    print("Error: Flask Module is missing:")
    print("Please install the \"Flask\" module as it is required for the webserver to work.")
    exit(1)

# Built in:
import importlib, json, os, logging

# Will run without, but will give a notice in the webserver that they're missing:
to_import = []
failed_imports = []

for to_install in to_import:
    try:
        importlib.import_module(to_install)
    except ImportError:
        failed_imports.append(to_install)

# === END OF IMPORTS ===

# === WEBSERVER: ===
app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

try:
    with open('webserver-config.json') as config_file:
        config_data = json.load(config_file)
        host = config_data.get("host", "127.0.0.1")
        port = config_data.get("port", 8080)
        initialized = config_data.get("initialized", 0)
except FileNotFoundError:
    print("Error: webserver-config.json not found.")
    exit(1)

@app.errorhandler(404)
def page_not_found(error):
    return send_from_directory(os.path.join(app.root_path, 'frontend_templates', 'errors'), '404.html'), 404

@app.route('/styles.css')
def styles_css():
    return send_from_directory(os.path.join(app.root_path, 'frontend_templates', 'firstIndex'), 'styles.css')

@app.route('/')
def index_html():
    with open('webserver-config.json', 'r') as config_file:
        config_data = json.load(config_file)

    initialized = config_data.get("initialized", 0)
    template_folder = 'index' if initialized == 1 else 'firstIndex'

    return send_from_directory(os.path.join(app.root_path, 'frontend_templates', template_folder), 'index.html')



@app.route('/api/v1/failed_imports')
def get_failed_imports():
    if not failed_imports:
        with open('webserver-config.json', 'r') as config_file:
            config_data = json.load(config_file)

        config_data['initialized'] = 1
        initialized = 1

        with open('webserver-config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=2)

    return failed_imports

@app.route('/script.js')
def script_js():
    return send_from_directory(os.path.join(app.root_path, 'frontend_templates', 'firstIndex'), 'script.js')

if initialized == 0:
    print(f'\n=== finish the initialization process at http://{host}:{port}/ ===')
    print('do not close this screen!!!\n')
else:
    print(f'\n=== webmenu available at http://{host}:{port}/ ===')
    print('if you close this screen then the app will no longer work\n')
if __name__ == '__main__':
    app.run(host=host, port=port)
