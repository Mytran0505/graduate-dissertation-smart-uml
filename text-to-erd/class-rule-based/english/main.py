from class_rule_base import UMLGenerator

if __name__ == "__main__":
    uml_generator = UMLGenerator()
    path_file = "./data/script_new.txt"

    with open(path_file, "r") as f:
        paragraph = f.read()
    sentences = uml_generator.split_sentences(" ".join([uml_generator.clean_sentence(s) for s in uml_generator.split_sentences(paragraph)]))

    uml_generator.extract_information_text(sentences)
    #uml_generator.add_attribute_from_reference()

    #uml_generator.check_many_many_rela(paragraph)

    uml_generator.save_puml(uml_generator.print_uml(), "./result/", "check16")
    uml_generator.save_sql(uml_generator.print_sql(), "./result/", "sql16")