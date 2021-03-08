from utils import utilities as utils
from dataloader import VisDialDataset


MODELS = {
    'CLIP_fake_RL': {
        'startFrom': 'checkpoints/CLIP_fake_RL_abot_ep_1.vd',
        'qstartFrom': 'checkpoints/CLIP_fake_RL_qbot_ep_1.vd',
        'imgFeatureSize': 512,
        'inputImg': 'data/visdial/data_img_clip.h5',
    },
    'CLIP_RL': {
        'startFrom': 'checkpoints/CLIP_RL_abot_ep_1.vd',
        'qstartFrom': 'checkpoints/CLIP_RL_qbot_ep_1.vd',
        'imgFeatureSize': 512,
        'inputImg': 'data/visdial/data_img_clip.h5',
    },
    'CLIP': {
        'startFrom': 'checkpoints/CLIP_sl_abot_ep_85.vd',
        'qstartFrom': 'checkpoints/CLIP_sl_div_qbot_ep_85.vd',
        'imgFeatureSize': 512,
        'inputImg': 'data/visdial/data_img_clip.h5',
    },
    'Das_fake_RL': {
        'startFrom': 'checkpoints/Das_fake_RL_abot_ep_2.vd',
        'qstartFrom': 'checkpoints/Das_fake_RL_qbot_ep_2.vd',
    },
    'Das_OG': {
        'startFrom': 'checkpoints/Das_OG_SL_ABOT.vd',
        'qstartFrom': 'checkpoints/Das_OG_SL_QBOT.vd',
    },
    'Das_RL': {
        'startFrom': 'checkpoints/Das_RL_abot_ep_2.vd',
        'qstartFrom': 'checkpoints/Das_RL_qbot_ep_2.vd',
    },
    'diversity_fake_RL_abot_ep_2': {
        'startFrom': 'checkpoints/diversity_fake_RL_abot_ep_2.vd',
        'qstartFrom': 'checkpoints/diversity_fake_RL_qbot_ep_2.vd',
    },
    'diversity_OG': {
        'startFrom': 'checkpoints/diversity_OG_SL_ABOT.vd',
        'qstartFrom': 'checkpoints/diversity_OG_SL_QBOT.vd',
    },
    'diversity_RL': {
        'startFrom': 'checkpoints/diversity_RL_RL_DIV_ABOT.vd',
        'qstartFrom': 'checkpoints/diversity_RL_RL_DIV_QBOT.vd',
    },
}

DEFAULTS = {
    # model-specific
    'startFrom': 'checkpoints-release/RL_DIV_ABOT.vd',
    'qstartFrom': 'checkpoints-release/RL_DIV_QBOT.vd',
    'imgFeatureSize': 4096,

    # installation-specific
    'cocoDir': '~/hpc-share/data/coco/images',
    'cocoInfo': 'coco.json',
    'inputImg': 'data/visdial/data_img.h5',
    'inputQues': 'data/visdial/chat_processed_data.h5',
    'inputJson': 'data/visdial/chat_processed_params.json',
    'inputDenseJson': 'data/visdial/visdial_1.0_val_dense_annotations.json',

    'evalModeList': 'single_dialog',
    'beamSize': 5,
    'useGPU': True,

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
    'embedSize': 300,
    'rnnHiddenSize': 512,
    'numLayers': 2,
    'imgNorm': 1,

    'useNDCG': False,
    'useHistory': True,
    'useIm': 'late',
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

# TODO : 031673 - this happens for images in the test split
#   File "/nfs/hpc/share/lallya/nlp-project/eval_utils/dialog_generate.py", line 645, in run_single_dialog
#     for idx, batch in enumerate(dataloader):
#   File "/nfs/hpc/share/lallya/.conda/envs/visdial-diversity/lib/python3.6/site-packages/torch/utils/data/dataloader.py", line 259, in _
# _next__
#     batch = self.collate_fn([self.dataset[i] for i in indices])
#   File "/nfs/hpc/share/lallya/.conda/envs/visdial-diversity/lib/python3.6/site-packages/torch/utils/data/dataloader.py", line 259, in <
# listcomp>
#     batch = self.collate_fn([self.dataset[i] for i in indices])
#   File "/nfs/hpc/share/lallya/nlp-project/dataloader.py", line 308, in __getitem__
#     item = self.getIndexItem(self._split, idx)
#   File "/nfs/hpc/share/lallya/nlp-project/dataloader.py", line 389, in getIndexItem
#     ansId = self.data[dtype + '_ans_ind'][idx]
#   File "/nfs/hpc/share/lallya/.conda/envs/visdial-diversity/lib/python3.6/collections/__init__.py", line 883, in __getitem__
#     return self.__missing__(key)            # support subclasses that define __missing__
#   File "/nfs/hpc/share/lallya/.conda/envs/visdial-diversity/lib/python3.6/collections/__init__.py", line 875, in __missing__
#     raise KeyError(key)
# KeyError: 'single_ans_ind'



def _get_dataset(params):
    if not hasattr(_get_dataset, 'cache'):
        _get_dataset.cache = {}
    key = params['inputImg']
    result = _get_dataset.cache.get(key)
    if not result:
        result = VisDialDataset(params, ['train', 'val', 'test'])
        _get_dataset.cache[key] = result
    return result


def setup(model_name):
    params = DEFAULTS.copy()
    params.update(MODELS[model_name])

    dlparams = params.copy()
    dlparams['useIm'] = True
    dataset = _get_dataset(dlparams)

    # Transferring dataset parameters
    transfer = ['vocabSize', 'numOptions', 'numRounds']
    for key in transfer:
        if hasattr(dataset, key):
            params[key] = getattr(dataset, key)

    excludeParams = ['batchSize', 'visdomEnv', 'startFrom', 'qstartFrom',
                     'trainMode', 'evalModeList', 'evalSplit', 'inputImg',
                     'inputQues', 'inputJson', 'evalTitle', 'beamSize',
                     'enableVisdom', 'visdomServer', 'visdomServerPort',
                     'savePath', 'saveName']

    # load aBot
    aBot, loadedParams, _ = utils.loadModel(params, 'abot', overwrite=True)
    assert aBot.encoder.vocabSize == dataset.vocabSize, "Vocab size mismatch!"
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

    return params, dataset, qBot, aBot
