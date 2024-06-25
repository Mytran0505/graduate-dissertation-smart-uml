import transformers
from transformers import (
    MT5ForConditionalGeneration,
    Seq2SeqTrainer, MT5Tokenizer, MT5Config
)
import re
import datasets
import pandas as pd
from transformers import DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
import numpy as np
from datasets import load_metric
import gc
import datasets
import os
import torch

checkpoint = "VietAI/vit5-base"
model = MT5ForConditionalGeneration.from_pretrained(checkpoint)
model.load_state_dict(torch.load('src/model/TextToERD/transform_model.pt'))
model.eval()
tokenizer = MT5Tokenizer.from_pretrained(checkpoint)

def split_sentences(paragraph):
        return re.split(r'(?<!\w\.\w.)(?<=\.|\?)\s', paragraph)

def paraphase(text):
    inputs = tokenizer(text, padding='longest', max_length=64, return_tensors='pt')
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask
    output = model.generate(input_ids, attention_mask=attention_mask, max_length=64)
    return tokenizer.decode(output[0], skip_special_tokens=True)