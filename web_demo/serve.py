import json

from flask import Flask

from utils import utilities as utils
from dataloader import SingleImageEvalDataset, VisDialDataset
from eval_utils.dialog_generate import run_single_dialog
from options import readCommandLine


params = {
    'useGPU': True,
    'startFrom': 'checkpoints-release/RL_DIV_ABOT.vd',
    'qstartFrom': 'checkpoints-release/RL_DIV_QBOT.vd',
    'evalModeList': 'single_dialog',
    'cocoDir': '~/hpc-share/data/coco/images',
    'cocoInfo': 'coco.json',
    'beamSize': 5,

    'useNDCG': False,

    'inputImg': 'data/visdial/data_img.h5',
        'inputQues': 'data/visdial/chat_processed_data.h5',
    'inputJson': 'data/visdial/chat_processed_params.json',
        'inputDenseJson': 'data/visdial/visdial_1.0_val_dense_annotations.json',

    'verbose': 1,
    'savePath': 'checkpoints/',
    'saveName': '',
    'continue': False,
    'enableVisdom': 0,
        'visdomEnv': '',
    'visdomServer': '127.0.0.1',
        'visdomServerPort': 8893,

    'randomSeed': 32,
        'imgEmbedSize': 300,
    'imgFeatureSize': 4096,
        'embedSize': 300,
    'rnnHiddenSize': 512,
        'numLayers': 2,
    'imgNorm': 1,

        'AbotMCTS': 0,
    'encoder': 'hre-ques-lateim-hist',
        'decoder': 'gen',
    'qencoder': 'hre-ques-lateim-hist',
        'qdecoder': 'gen',
    'trainMode': 'rl-full-QAf',
        'numRounds': 10,
    'batchSize': 20,
        'learningRate': 1e-3,
    'minLRate': 5e-5,
        'dropout': 0.0,
    'numEpochs': 85,
        'lrDecayRate': 0.9997592083,
    'CELossCoeff': 1,
        'RLLossCoeff': 20000,
    'useCosSimilarityLoss': 1,
        'CosSimilarityLossCoeff': 0.1,

    'useHuberLoss': 1,
        'HuberLossCoeff': 1,

    'featLossCoeff': 1000,
        'useCurriculum': 1,
    'freezeQFeatNet': 0,
        'rlAbotReward': 1,
    'annealingEndRound': 3,
        'annealingReduceEpoch': 1,
        'numWorkers': 2,
    'evalSplit': 'val',
        'evalTitle': 'eval',
    'startEpoch': 1,
        'endEpoch': 1,
        'discountFactor': 0.5,

}

# check if history is needed
params['useHistory'] = True if 'hist' in params['encoder'] else False

# check if image is needed
if 'lateim' in params['encoder']:
    params['useIm'] = 'late'
elif 'im' in params['encoder']:
    params['useIm'] = True
else:
    params['useIm'] = False

dlparams = params.copy()
dlparams['useIm'] = True
dlparams['useHistory'] = True
dlparams['numRounds'] = 10
splits = ['train','val', 'test']

base_dataset = VisDialDataset(dlparams, splits)

# Transferring dataset parameters
transfer = ['vocabSize', 'numOptions', 'numRounds']
for key in transfer:
    if hasattr(base_dataset, key):
        params[key] = getattr(base_dataset, key)

excludeParams = ['batchSize', 'visdomEnv', 'startFrom', 'qstartFrom',
                 'trainMode', 'evalModeList', 'evalSplit', 'inputImg',
                 'inputQues', 'inputJson', 'evalTitle', 'beamSize',
                 'enableVisdom', 'visdomServer', 'visdomServerPort','savePath',
                 'saveName']

# load aBot
aBot, loadedParams, _ = utils.loadModel(params, 'abot', overwrite=True)
assert aBot.encoder.vocabSize == base_dataset.vocabSize, "Vocab size mismatch!"
for key in loadedParams:
    params[key] = loadedParams[key]
aBot.eval()

# Retaining certain dataloder parameters
for key in excludeParams:
    params[key] = dlparams[key]

# load qBot
qBot, loadedParams, _ = utils.loadModel(params, 'qbot', overwrite=True)
assert qBot.encoder.vocabSize == params[
    'vocabSize'], "Vocab size mismatch!"
for key in loadedParams:
    params[key] = loadedParams[key]
qBot.eval()


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