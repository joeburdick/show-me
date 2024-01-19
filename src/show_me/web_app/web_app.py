import sys
print(sys.path)

from flask import Flask, render_template
from show_me.image_generation.stability_config import get_stability_config

app = Flask(__name__)

@app.route('/')
def index():
    stabilityConfig = get_stability_config()

    return render_template('config.html', stabilityConfig=stabilityConfig)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')