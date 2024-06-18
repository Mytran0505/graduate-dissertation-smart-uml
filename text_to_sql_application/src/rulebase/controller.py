import os
from src.rulebase.service import UMLGenerator
from flask import Flask, request, jsonify
from flask import Response

def process_paragraph_to_UML_DDL():
    data = request.json
    if 'paragraph' not in data:
        return jsonify({"error": "No paragraph provided"}), 400
    
    paragraph = data['paragraph']
    uml_generator = UMLGenerator()

    sentences = uml_generator.split_sentences(" ".join([uml_generator.clean_sentence(s) for s in uml_generator.split_sentences(paragraph)]))
    uml_generator.extract_information_text(sentences)
    uml_generator.add_attribute_from_reference()
    uml_generator.check_many_many_rela(paragraph)
    uml = uml_generator.print_uml()
    sql = uml_generator.print_sql()
    return jsonify({"uml": uml, "sql": sql})
