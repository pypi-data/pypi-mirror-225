# Contents

- [Contents](#contents)
- [Introduction](#introduction)
- [Using the fine-tuner](#using-the-fine-tuner)
  - [Curating a dataset](#curating-a-dataset)
  - [Deploying a finetuning job](#deploying-a-finetuning-job)
  - [Finetuning a different model](#finetuning-a-different-model)
- [Retrieving the info on your most recent training jobs](#retrieving-the-info-on-your-most-recent-training-jobs)
- [Checking the status of your fine-tuning job](#checking-the-status-of-your-fine-tuning-job)
- [Retrieving your training results](#retrieving-your-training-results)
- [Using your Fine-tuned Adaptor](#using-your-fine-tuned-adaptor)

# Introduction

The fine-tuner package allows you to quickly and conveniently fine-tune your LLM on Cerebrium with one command.  
The fine-tuner leverages the fine-tune any PEFT and LoRA compatible causal language model from the Huggingface transformers library.  
However, we have focused on the finetuning llama using the alpaca prompting templates for the MVP.

In future, we plan to release capabilities for custom prompting templates, however, at the moment we use the well-proven Alpaca-Lora prompt templating.
For more information, see

<!-- TODO link to templates. -->

# Using the fine-tuner

## Curating a dataset

The finetuning library has been built to leverage Parameter Efficient Finetuning and Low Rank Approximation to reduce the number of trainable parameters by >99.9% while, as shown by multiple experiments in the literature, providing results that are comparable to full fine-tuning.  
Due to the much lower number of trainable parameters, the datasets used do not need to be greater than 1000 examples. In most situations, a dataset of 100-500 prompts is more than adequate to achieve good performance.

For your convenience, an example dataset has been provided for Beta testing [here](../../examples/training-job/dataset.json). The dataset is a JSON or JSONL file which contains a "prompt", "completion", and if needed "context".

## Deploying a finetuning job

Deploying a finetuning job is done using one simple command in the Cerebrium CLI.

```bash
cerebrium train <<YOUR_JOB_NAME>> <<API_KEY>> <<HUGGINGFACE_MODEL_PATH>> <<PATH_TO_YOUR_FINETUNING_DATASET>>
```

This will create a training config and upload your job and dataset to Cerebrium to start your training on an A10 instance!

<!-- For added control, a finetuning task can be deployed using the python functions. If this is required, please contact the team for documentation and instructions. -->

## Finetuning a different model

At present, the models that have been tested on the fine-tuner environment are:

> - Llama 7B

<!-- TODO: Add to this list as we test.  -->

To fine-tune a model that is not loaded with `transformers.AutoModelForCausalLM`, you can set the model type using the `--model-type` flag.  
For example, to fine-tune a model such as T5 which requires `transformers.T5ForConditionalGeneration` you would use:

```bash
cerebrium train my-t5-conditional <<YOUR_API_KEY>> "google/flan-t5-large" <<PATH_TO_YOUR_FINETUNING_DATASET>> --model-type "T5ForConditionalGeneration"
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

# Retrieving your training results

Once your training is complete, you can download the training results using:

```bash
cerebrium download-model <<JOB_ID>> <<API_KEY>>
```

This will return a zip file which contains your **adapter** and **adapter config** which should be in the order of 10MB for your 7B parameter model due to the extreme efficiency of PEFT fine-tuning.

# Using your Fine-tuned Adaptor

Using your adapter can be done simply by adding two lines as shown here:

```python
  from transformers import AutoModelForCausalLM
  from peft import PeftModel, PeftConfig # Add the peft libraries we need for the adapter

  peft_model_id = "path/toYourAdapter"
  config = PeftConfig.from_pretrained(peft_model_id)
  model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path)
  model = PeftModel.from_pretrained(model, peft_model_id) # Add the adapter to the model
  tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)

  model = model.to("cuda")
  model.eval() # set the model to inference mode

```

Now for inference, you just need to place the prompt into the template used for training. In this example we do it as follows

```python
  template =  "### Instruction:\n{instruction}\n\n### Response:\n"
  question = template.format(instruction=prompt)
  inputs = tokenizer(question, return_tensors="pt")

  with torch.no_grad():
    outputs = model.generate(input_ids=inputs["input_ids"].to("cuda"), max_new_tokens=10)
    print(tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0])

```

These adapters can be combined with others when using your model at inference time.  
For more information, see
[Using Adapter Transformers at Hugging Face](https://huggingface.co/docs/hub/adapter-transformers#exploring-adaptertransformers-in-the-hub)
