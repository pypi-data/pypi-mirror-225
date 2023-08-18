# Contents

- [Contents](#contents)
- [Introduction](#introduction)
- [Using the diffusers fine-tuner](#using-the-diffusers-fine-tuner)
  - [Curating a dataset](#curating-a-dataset)
    - [Using prior preservation](#using-prior-preservation)
  - [Deploying a finetuning job](#deploying-a-finetuning-job)
    - [Description of the optional parameters to deploy your model with](#description-of-the-optional-parameters-to-deploy-your-model-with)
    - [Supported training kwargs reference](#supported-training-kwargs-reference)
- [Retrieving your training results](#retrieving-your-training-results)
- [Using your Fine-tuned Diffuser](#using-your-fine-tuned-diffuser)
- [Retrieving the info on your most recent training jobs](#retrieving-the-info-on-your-most-recent-training-jobs)
- [Checking the status of your fine-tuning job](#checking-the-status-of-your-fine-tuning-job)

# Introduction

The fine-tuner package allows you to quickly and conveniently fine-tune your diffusion model on Cerebrium with one command.  
Our method of finetuning focuses on the attention processors of the unet in the diffuser model to obtain high quality results with fast training times.

<!-- The fine-tuner leverages the fine-tune any PEFT and LoRA compatible causal language model from the Huggingface transformers library.
However, we have focused on the finetuning llama using the alpaca prompting templates for the MVP.

In future, we plan to release capabilities for custom prompting templates, however, at the moment we use the well-proven Alpaca-Lora prompt templating.
For more information, see -->

<!-- TODO link to templates. -->

# Using the diffusers fine-tuner

Currently, the models that have been tested on the diffuser trainer are:

> - [runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5)

## Curating a dataset

The follorwing are a set of guidelines to keep in mind when curating your dataset:

- image size of 512 x 512
- images should be upright
- Keep the number of training images low. Aim for between 10 and 15 as your model may not converge if you use too many.
- For style-based fine-tuning, try keep the style and colouring consistent.
- For object focused fine-tuning, each of your images should contribute new information on the subject.  
  You can do this by varying:
  - camera angle (although try keep the side of the object consistent. i.e. only take photos from the front)
  - pose
  - props or styles
  - background in the photos (if you would like varied backgrounds in your outputs.)

### Using prior preservation

Stable diffusion models are prone to catastrophic forgetting of classes when training. For example, if you have finetuned your model on a prompt of "Photo of a sdf dog" and supplied photos of a Labrador, your model may only predict photos of a labrador when asked for photos of a dog.

Therefore prior preservation works as a kind of regularizer for stable diffusion models that will still be generating other prompts in the same class.

The idea is to supervise the fine-tuning process with the model's own generated samples of the class noun.
In practice, this means having the model fit both the new images and the generated images simultaneously during training.

To use a prior class in training, you need to supply a number of class images as well as a prompt to generate these images with.  
Alternatively, you can generate these images beforehand and upload that prompt dataset and a prompt. When curating a prior class dataset, the goal is to select a wide variety of outputs from your model.

See [this section](#description-of-the-optional-parameters-to-deploy-your-model-with) for more information on the parameters to use.

## Deploying a finetuning job

```bash
cerebrium train-diffuser <<YOUR_JOB_NAME>> <<API_KEY_IF_NOT_LOGGED_IN>> <<HUGGINGFACE_MODEL_PATH>>  <<PATH_TO_YOUR_TRAINING_DATASET_IMAGES>> <<TRAINING_PROMPT>>
```

 <!-- Usage: cerebrium train-diffuser [OPTIONS] NAME HF_MODEL_PATH LOCAL_DATASET_PATH TRAINING_PROMPT                                    
╭─ Arguments 
│ *    name                    TEXT  A unique name you would like to describe this fine-tuning of your diffuser. [default: None] [required]
│ *    hf_model_path           TEXT  Huggingface model path to use. [default: None] [required]
│ *    local_dataset_path      TEXT  Path to your local dataset JSON file. [default: None] [required]
│ *    training_prompt         TEXT  Prompt to generate images during training. [default: None] [required] -->

This will create a training config and upload your job and dataset to Cerebrium to start your training on an A10 instance!

<br>

### Description of the optional parameters to deploy your model with

| Option Parameter         | Type    | Description                                                                                                        |
| ------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------ |
| --api-key                | TEXT    | Private API key for the user.                                                                                      |
| --prior-class-image-dir  | TEXT    | Path to directory containing images generated prior to training using a class prompt.                              |
| --prior-class-prompt     | TEXT    | Prompt to generate images prior to training for the class.                                                         |
| --num-prior-class-images | INTEGER | Number of images to generate prior to training for the class. [default: 0]                                         |
| --training-args          | TEXT    | Json string of training keyword arguments for the model. Example: '{"num_train_epochs": 5, "learning_rate": 1e-4}' |
| --revision               | TEXT    | Huggingface revision of the model to use. [default: main]                                                          |
| --log-level              | TEXT    | Log level for the builder deployment. Can be one of 'DEBUG' or 'INFO' [default: INFO]                              |

<!-- For added control, a finetuning task can be deployed using the python functions. If this is required, please contact the team for documentation and instructions. -->
<br>

### Supported training kwargs reference

<!-- **Table of possible training kwargs** -->

| Key                         | Default    | Description                                                                                                                                     |
| --------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| gradient_accumulation_steps | 1          | Number of update steps to accumulate the gradient over before the backward/update pass.                                                         |
| learning_rate               | 0.0005     | Initial learning rate to use in training.                                                                                                       |
| lr_schedule                 | "constant" | Schedule for the learning rate to follow. Can be:["linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"] |
| max_train_steps             | None       | Total number of training steps to perform. Overrides num_train_epochs if provided.                                                              |
| num_train_epochs            | 30         | Number of epochs to train for where one epoch is an iteration over the dataset                                                                  |
| train_batch_size            | 2          | Batch size per device to be used by the training image dataloader                                                                               |
| scale_lr                    | False      | Scale the learning rate by the number of GPUs, gradient accumulation steps, and batch size.                                                     |
| warmup_steps                | 0          | Number of gradient warmup steps before training                                                                                                 |
| validation_epochs           | 10         | Number of epochs before each validation step.                                                                                                   |
| use_8bit_adam               | True       | Use 8-bit adam from bitsandbytes for the optimisation                                                                                           |

<br>

---

# Retrieving your training results

Once your training is complete, you can download the training results using:

```bash
cerebrium download-model <<JOB_ID>> <<API_KEY>>
```

This will return a zip file which contains your attention processors and the validation images generated by your model during training.

# Using your Fine-tuned Diffuser

Using your finetuning results is done as follows:

```python

from diffusers import (
    DiffusionPipeline,
    DPMSolverMultistepScheduler,
)
import torch

# Boilerplate loading of model
pipeline = DiffusionPipeline.from_pretrained(
    your_model_name, revision=your_model_revision, torch_dtype=torch.float16
)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
pipeline = pipeline.to("cuda")


# LOAD IN YOUR TRAINING RESULTS
# load attention processors from where they are saved in your_results/checkpoints/final/attn_procs/pytorch_lora_weights.bin
pipeline.unet.load_attn_procs(os.path.join(final_output_dir, "attn_procs"))
# And that's all you need to do to load in the finetuned result!
# Now you can run your inference as you would like with the pipeline.


# some inference variables
your_prompt = "Your training prompt that you would like to use here"
num_images =  4 # number of images to generate
your_manual_seed = 42 # a manual seed if you would like repeatable results

# run inference as you normally would
generator = torch.Generator(device="cuda").manual_seed(your_manual_seed)
images = [
    pipeline(your_prompt, num_inference_steps=25, generator=generator).images[0]
    for _ in range(num_images)
]

```

# Retrieving the info on your most recent training jobs

Keeping track of the jobIds for all your different experiments can be challenging.  
To retrieve the status and information on your 10 most recent fine-tuning jobs, you can run the following command:

```bash
cerebrium get-most-recent-jobs <<PROJECT_ID>> <<API_KEY>>
```

Where your API_KEY is the key for the project under which your fine-tuning has been deployed.

# Checking the status of your fine-tuning job

To check the status of a specific fine-tuning job as well as retrieve the logs:

```bash
cerebrium check-job-status <<JOB_ID>> <<API_KEY>> --include-logs <<True|False>>
```
