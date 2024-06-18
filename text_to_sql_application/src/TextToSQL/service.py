def generate_sql(model, tokenizer, question):
    # Encode the input question
    input_ids = tokenizer.encode(question, return_tensors='pt')
    
    # Generate the SQL query
    outputs = model.generate(input_ids=input_ids, max_length=100, num_beams=5, early_stopping=True)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return sql_query