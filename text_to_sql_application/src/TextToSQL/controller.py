from flask import Flask, request, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from src.TextToSQL.service import generate_sql
# Load the model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-base')
model.load_state_dict(torch.load('src/model/TextToSQL/spider/spider_model.pt'))
model.eval()
tokenizer = T5Tokenizer.from_pretrained('t5-base')

def generate_sql_endpoint():
    # Get the input question from the POST request
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Generate SQL query using the function
    sql_query = generate_sql(model, tokenizer, question)
    
    # Return the generated SQL query
    return sql_query