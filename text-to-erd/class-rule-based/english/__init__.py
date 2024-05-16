from class_rule_base import UMLGenerator

if __name__ == "__main__":
    uml_generator = UMLGenerator()
    path_file = "script.txt"

    with open(path_file, "r") as f:
        paragraph = f.read()
    sentences = uml_generator.split_sentences(" ".join([uml_generator.clean_sentence(s) for s in uml_generator.split_sentences(paragraph)]))

    uml_generator.extract_information_text(sentences)

    uml_generator.save_puml(uml_generator.print_uml(), "result/", "check2")