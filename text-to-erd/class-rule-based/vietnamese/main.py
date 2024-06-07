import os
from class_rule_base_vietnamese import UMLGenerator

if __name__ == "__main__":
    puml_output_directory = f"export/puml/rule-based-solution"
    os.makedirs(puml_output_directory, exist_ok=True)  # Create export directory if it doesn't exist
    sql_output_directory = f"export/sql/rule-based-solution"
    os.makedirs(sql_output_directory, exist_ok=True)  # Create export directory if it doesn't exist
    for root, dirs, files in os.walk('data/De_074'):
        uml_generator = UMLGenerator()
        modified_file = None
        for file in files:
            if file.endswith("_modified.txt"):
                path_file = os.path.join(root, file)
                modified_file = file
                with open(path_file, encoding="utf-8") as f:
                    paragraph = f.read()
                sentences = uml_generator.split_sentences(" ".join([uml_generator.clean_sentence(s) for s in uml_generator.split_sentences(paragraph)]))
                uml_generator.extract_information_text(sentences)
                uml_generator.add_attribute_from_reference()
                uml_generator.check_many_many_rela(paragraph)
                
                # Construct output file name
                output_file_name = modified_file.replace("_modified.txt", "-rule-based-solution")
                uml_generator.save_puml(uml_generator.print_uml(), puml_output_directory, output_file_name)
                uml_generator.save_sql(uml_generator.print_sql(), sql_output_directory, output_file_name)