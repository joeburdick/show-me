from flask import Flask, request, render_template
from show_me.image_generation.stability_config import *

import os;
print(os.getcwd())

configPath = 'config/stability_config.json'
app = Flask(__name__)

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        stabilityConfig = StabilityConfig(request.form['steps'], request.form['seed'], request.form['cfg_scale'], request.form['sampler'])
        save_stability_config(configPath, stabilityConfig)
    else:
        stabilityConfig = get_stability_config(configPath)
    return render_template('config.html', stabilityConfig=stabilityConfig)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')