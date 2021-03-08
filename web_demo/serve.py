import json
import os

from flask import Flask, request

from dataloader import SingleImageEvalDataset
from eval_utils.dialog_generate import run_single_dialog
from web_demo import setup
from web_demo.setup import MODELS


models = {
    model: setup.setup(model) for model in MODELS.keys()
}
# params, base_dataset, qBot, aBot = setup.setup('CLIP_fake_RL')

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/images')
def image_list():
    global base_dataset
    result = []
    for key, val in base_dataset.data.items():
        if key.endswith('img_fnames'):
            result += [os.path.splitext(img)[0][-6:] for img in val]
    return json.dumps(result)


@app.route('/api/models')
def model_list():
    return json.dumps(MODELS.keys())


@app.route('/api/dialog/<int:img_id>')
def dialog(img_id):
    global models

    model_name = request.args.get('model', 'Das_OG')
    params, base_dataset, qBot, aBot = models[model_name]

    # print("Performing single dialog generation...")
    dataset = SingleImageEvalDataset(base_dataset, img_id)
    dialog = run_single_dialog(params, dataset, aBot, qBot)

    return json.dumps(dialog)


if __name__ == '__main__':
    app.run()
