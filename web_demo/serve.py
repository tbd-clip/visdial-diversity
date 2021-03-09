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

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/images')
def image_list():
    model_name = request.args.get('model', 'diversity_RL')
    params, base_dataset, qBot, aBot = models[model_name]
    result = []
    for key, val in base_dataset.data.items():
        if key.endswith('img_fnames'):
            result += [os.path.splitext(img)[0][-6:] for img in val]
    return json.dumps(result)


@app.route('/api/models')
def model_list():
    return json.dumps([{'model': m} for m in models.keys()])


@app.route('/api/dialog/<int:img_id>')
def dialog(img_id):
    model_name = request.args.get('model', 'diversity_RL')
    params, base_dataset, qBot, aBot = models[model_name]
    dataset = SingleImageEvalDataset(base_dataset, img_id)
    dialog = run_single_dialog(params, dataset, aBot, qBot)
    return json.dumps(dialog)


if __name__ == '__main__':
    app.run()
