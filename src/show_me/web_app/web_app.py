from flask import Flask, request, render_template
from show_me.image_generation.stability_config import *
from show_me.image_generation.image_generate import *
from show_me.inky_display.image_display import *
import base64
from io import BytesIO

configPath = 'config/stability_config.json'
app = Flask(__name__)

def image_to_data_url(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return "data:image/jpeg;base64," + img_str.decode()

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        stabilityConfig = StabilityConfig(request.form['steps'], request.form['seed'], request.form['cfg_scale'], request.form['sampler'])
        save_stability_config(configPath, stabilityConfig)
    else:
        stabilityConfig = get_stability_config(configPath)
    return render_template('config.html', stabilityConfig=stabilityConfig)

@app.route('/', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        prompt = request.form['prompt']
        width = int(request.form['width'])
        height = int(request.form['height'])
        config = get_stability_config(configPath)
        image = generate_image(config, prompt, width, height)
        display_prompt(prompt)
        return render_template('generate.html', image=image_to_data_url(image), prompt=prompt, width=width, height=height)
    
    return render_template('generate.html', image=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')