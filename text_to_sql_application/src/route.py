from flask import Blueprint

from src.rulebase.controller import process_paragraph_to_UML_DDL

UML_DDL = Blueprint("UML_DDL", __name__)

@UML_DDL.route('/process-paragraph', methods=['POST'])
def process_paragraph():
    return process_paragraph_to_UML_DDL()