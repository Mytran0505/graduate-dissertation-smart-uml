from flask import Blueprint

from src.rulebase.controller import process_paragraph_to_UML_DDL
from src.TextToSQL.controller import generate_sql_endpoint

UML_DDL = Blueprint("UML_DDL", __name__)
SQL = Blueprint("SQL", __name__)

@UML_DDL.route('/process-paragraph', methods=['POST'])
def process_paragraph():
    return process_paragraph_to_UML_DDL()

@SQL.route('/generate_sql', methods=['POST'])
def process_query():
    return generate_sql_endpoint()