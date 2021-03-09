import json
import os

from flask import Flask, request, render_template

from dataloader import SingleImageEvalDataset
from eval_utils.dialog_generate import run_single_dialog
from web_demo import setup
from web_demo.setup import MODELS


models = {model: setup.setup(model) for model in MODELS.keys()}

app = Flask(__name__)


@app.route("/")
def index():
    # data = {
    #     "dialog": [
    #         {
    #             "answer": "yes",
    #             "question": "is the photo in color ?",
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "no",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "i ca n't see his face , i do n't know",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "shorts and t shirt",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "brown",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "no",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "brown",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "no",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "brown",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #         {
    #             "answer": "no",
    #             "question": "is the photo close up ?",
    #             "C": -0.50,
    #             "NP": 0.02,
    #             "H": 1.73,
    #             "N": 2.84,
    #             "image_id": 480851,
    #             "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #             "caption": "a man riding a ski board while holding onto a rope",
    #         },
    #     ],
    #     "image_id": 480851,
    #     "image_filename": "https://pbs.twimg.com/profile_images/1310968517961740289/m9wp7-vJ_400x400.jpg",
    #     "caption": "a man riding a ski board while holding onto a rope",
    # }
    # return render_template(
    #     "index.html",
    #     dialogs=data["dialog"],
    #     image_id=data["image_id"],
    #     image_filename=data["image_filename"],
    #     caption=data["caption"],
    # )
    return render_template("index.html")


@app.route("/api/images")
def image_list():
    model_name = request.args.get("model", "diversity_RL")
    params, base_dataset, qBot, aBot = models[model_name]
    result = []
    for key, val in base_dataset.data.items():
        if key.endswith("img_fnames"):
            result += [os.path.splitext(img)[0][-6:] for img in val]
    return json.dumps(result)


@app.route("/api/models")
def model_list():
    return json.dumps([{"model": m} for m in models.keys()])


@app.route("/api/dialog/<int:img_id>")
def dialog(img_id):
    model_name = request.args.get("model", "diversity_RL")
    params, base_dataset, qBot, aBot = models[model_name]
    dataset = SingleImageEvalDataset(base_dataset, img_id)
    dialog = run_single_dialog(params, dataset, aBot, qBot)
    return json.dumps(dialog)


if __name__ == "__main__":
    app.run()
