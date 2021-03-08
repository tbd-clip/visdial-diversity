import json

from flask import Flask

from dataloader import SingleImageEvalDataset
from eval_utils.dialog_generate import run_single_dialog
from web_demo import setup


params, base_dataset, qBot, aBot = setup.setup()

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello!'

@app.route('/api/images')
def image_list():
    pass

@app.route('/api/dialog/<int:img_id>')
def dialog(img_id):
    global base_dataset

    # print("Performing single dialog generation...")
    dataset = SingleImageEvalDataset(base_dataset, img_id)
    split = 'single'
    dialog = run_single_dialog(params, dataset, split, aBot, qBot)

    return json.dumps(dialog)


if __name__ == '__main__':
    app.run()
