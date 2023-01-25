import os
from typing import Callable
from shutil import rmtree
from tempfile import mkdtemp
from subprocess import call
from modules import sd_models

load_model_weights: Callable


def alternate_load_model_weights(model, checkpoint_info: sd_models.CheckpointInfo):
    print('Copying model into temporary directory.')

    temp_dir = mkdtemp()
    copied_checkpoint_file = os.path.join(temp_dir, checkpoint_info.name)
    call(['rsync', '-aP', checkpoint_info.filename, copied_checkpoint_file])

    print(f'Successfully copied model to {copied_checkpoint_file}')

    try:
        sd = load_model_weights(model, checkpoint_info)
    finally:
        print('Discarding temporary model file.')
        rmtree(temp_dir, True)

    return sd


if not sd_models.load_model_weights == alternate_load_model_weights:
    print('Applying alternate load_model_weights.')
    load_model_weights = sd_models.load_model_weights
    sd_models.load_model_weights = alternate_load_model_weights