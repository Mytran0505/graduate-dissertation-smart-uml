import re
import os
import spacy
import unidecode

data_types = {
    'mã': 'INT',
    'tên': 'VARCHAR(100)',
    'text': 'VARCHAR(255)',
    'số': 'INT',
    'decimal': 'DECIMAL(10, 2)',
    'ngày': 'DATE',  
    'giờ': 'TIME',
    'ngày_giờ': 'DATETIME',
    'float': 'FLOAT',
    'int' : 'INT'
}

class UMLGenerator:
    KEYWORDS_FLOAT = ["dung_lượng", "cỡ", "độ_dài", "tốc_độ"]
    KEYWORDS_INT = ["thời_gian"]
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.entities = []
        self.relationships = []
        self.attributeReference = []
        self.entityReference = []
        self.entityReferenceOptional = []
        self.processed_pairs = set()

    def convert_name(self, noun_chunk):
        common_noun_pattern = re.compile(r'\b(?:mỗi|một) \b', re.IGNORECASE)
        space_pattern = re.compile(r'\b \b')
        word = re.sub(space_pattern, '_', re.sub(common_noun_pattern, '', noun_chunk))
        return word

    def split_sentences(self, paragraph):
        return re.split(r'(?<!\w\.\w.)(?<=\.|\?)\s', paragraph)

    def clean_sentence(self, sentence):
        if "," in sentence:
            sentence = sentence.replace("và ", "")
        else:
            sentence = sentence.replace("và ", ". \n")
        sentence = sentence.replace(" hoặc", ",")
        return sentence

    def noun_has_entity_relationship_entity_match(self, sentence):
        entity_has_entity_2 = r"[Mỗi|Một] (\w+) có nhiều (\w+)"
        ehe2_matches = re.findall(entity_has_entity_2, sentence)
        return ehe2_matches

    def noun_has_entity_relationship_entity(self, sentence, match):
        entity_1 = self.convert_name(match[0][0].strip())
        entity_2 = self.convert_name(match[0][1].strip())
        if not any(ent == entity_1 for ent, attrs in self.entities):
            self.entities.append((entity_1, []))
        if not any(ent == entity_2 for ent, attrs in self.entities):
            self.entities.append((entity_2, []))
        self.entityReference.append((entity_2, entity_1.lower()))
        self.relationships.append(f"{self.convert_name(unidecode.unidecode(entity_1.lower()))} |o--|{'{'} {self.convert_name(unidecode.unidecode(entity_2.lower()))}\n\n")

    def one_to_one_relationship_match(self, sentence):
        one_to_one = r"[Mỗi|Một] (\w+) chỉ có duy nhất một (\w+) (?:\w+ )*(.+)\."
        oto_matches = re.findall(one_to_one, sentence)
        return oto_matches

    def one_to_one_relationship(self, sentence, match):
        entity_1 = self.convert_name(match[0][0].strip())
        entity_2 = self.convert_name(match[0][1].strip())
        optionalAtrribute = self.convert_name(match[0][2].strip())
        if not any(ent == entity_1 for ent, attrs in self.entities):
            self.entities.append((entity_1, []))
        if not any(ent == entity_2 for ent, attrs in self.entities):
            self.entities.append((entity_2, []))
        optionalAtrribute = f'^ Mã_{entity_2}_' + optionalAtrribute
        self.entityReferenceOptional.append((entity_1, entity_2))
        for i, (ent, attrs) in enumerate(self.entities):
            if ent == entity_1:
                attrs.append(optionalAtrribute)
                break
        self.relationships.append(f"{self.convert_name(unidecode.unidecode(entity_1.lower()))} ||--o| {self.convert_name(unidecode.unidecode(entity_2.lower()))}\n\n")

    def self_entity_relationship_entity_match(self, sentence):
        entity_has_entity_5 = r"(Mỗi|Một) (\w+(?:\s(?!chỉ\s)\w+)*) (?:bị|chỉ được|được) .*?(\w+(?:_\w+)*).*?(?:bởi một|cho một) (\w+(?:\s\w+)*) khác"
        ehe5_matches = re.findall(entity_has_entity_5, sentence)
        return ehe5_matches

    def self_entity_relationship_entity(self, sentence, match):
        entity_1 = self.convert_name(match[0][1].strip())
        entity_2 = self.convert_name(match[0][3].strip())
        selfAtrribute = self.convert_name(match[0][2].strip())
        if entity_1 == entity_2:
            selfAtrribute = f'^ Mã_{entity_2}_' + selfAtrribute
            self.entityReferenceOptional.append((entity_1, entity_2))
            for i, (ent, attrs) in enumerate(self.entities):
                if ent == entity_1:
                    attrs.append(selfAtrribute)
                    break
            self.relationships.append(f"{self.convert_name(unidecode.unidecode(entity_1.lower()))} |o--|{'{'} {self.convert_name(unidecode.unidecode(entity_2.lower()))}\n\n")

    def has_entity_relationship_attributes_match(self, sentence):
        entity_has_attributes_1 = r"[Mỗi|Một] (\w+) (?:được gán?|được xác định bởi duy nhất một) (\w+(?:,\s?\w+)*)"
        ehe6_matches = re.findall(entity_has_attributes_1, sentence)
        return ehe6_matches

    def has_entity_relationship_attributes(self, sentence, match):
        entity = self.convert_name(match[0][0].strip())
        attribute = match[0][1].split(", ")
        key_attribute_identified = r"[Mỗi|Một] (\w+) (?:được xác định bởi duy nhất một?) (\w+)"
        key_attribute_match = re.findall(key_attribute_identified, sentence)
        if len(key_attribute_match) == 1:
            attribute[0] = '* ' + attribute[0]
            for i in range(1, len(attribute)):
                attribute[i] = '+ ' + attribute[i]
        else:
            for i in range(len(attribute)):
                attribute[i] = '+ ' + attribute[i]
        for i, (ent, attrs) in enumerate(self.entities):
            if ent == entity:
                attrs.extend([self.convert_name(attr) for attr in attribute])
                break
        else:
            self.entities.append((entity, [self.convert_name(attr) for attr in attribute]))

    def add_attribute_from_reference(self):
        for entity, reference in self.entityReference:
            ref_attrs = None
            for ent, attrs in self.entities:
                if ent == reference:
                    ref_attrs = attrs
                    break
            if ref_attrs:
                key_attribute = next((attr[2:] for attr in ref_attrs if attr.startswith('*')), None)
                if key_attribute:
                    for ent, attrs in self.entities:
                        if ent == entity:
                            if f'. {key_attribute}' not in attrs:
                                attrs.append(f'. {key_attribute}')
                            break

    def check_many_many_rela(self, paragraph):
        many_many_pattern = r"[Mỗi|Một] (\w+) có thể.*?(\w+(?:_\w+)*).*?nhiều (\w+)"
        rela_name_pattern = r"Khi (\w+), phải biết (\w+(?:,\s?\w+)*)"
        
        match_many_many = re.findall(many_many_pattern, paragraph)
        match_rela_name = re.findall(rela_name_pattern, paragraph)
        
        for match in match_many_many:
            entity_1 = self.convert_name(match[0].strip())
            entity_2 = self.convert_name(match[2].strip())
            verb = self.convert_name(match[1].strip())

            # Check if this pair has already been processed
            if (entity_1, entity_2) in self.processed_pairs or (entity_2, entity_1) in self.processed_pairs:
                continue

            key_attributes = {'': '', '': ''}
            attribute = []

            for i, entities in enumerate([entity_1, entity_2]):
                for ent, attrs in self.entities:
                    if ent == entities:
                        key_attribute = next((attr[2:] for attr in attrs if attr.startswith('*')), None)
                        if key_attribute:
                            key_attributes[i] = key_attribute
                            attribute.append(key_attribute)
                            break

            if len(match_rela_name) == 1:
                table_rela_name = match_rela_name[0][0]
                attributes_to_add = match_rela_name[0][1].split(", ")
                attribute.extend(attributes_to_add)

            for i in range(len(attribute)):
                if attribute[i] in key_attributes.values():
                    attribute[i] = '- ' + attribute[i]
                    self.attributeReference.append((attribute[i], entity_1 if attribute[i][2:] == key_attributes[0] else entity_2))
                else:
                    attribute[i] = '+ ' + attribute[i]

            if len(match_rela_name) == 1:
                self.entities.append((table_rela_name, [self.convert_name(attr) for attr in attribute]))
                self.relationships.append(f"{self.convert_name(unidecode.unidecode(entity_1.lower()))} |o--|{'{'} {self.convert_name(unidecode.unidecode(table_rela_name.lower()))}\n\n")
                self.relationships.append(f"{self.convert_name(unidecode.unidecode(entity_2.lower()))} |o--|{'{'} {self.convert_name(unidecode.unidecode(table_rela_name.lower()))}\n\n")
            else:
                self.entities.append((verb, [self.convert_name(attr) for attr in attribute]))
                self.relationships.append(f"{self.convert_name(unidecode.unidecode(entity_1.lower()))} |o--|{'{'} {self.convert_name(unidecode.unidecode(verb.lower()))}\n\n")
                self.relationships.append(f"{self.convert_name(unidecode.unidecode(entity_2.lower()))} |o--|{'{'} {self.convert_name(unidecode.unidecode(verb.lower()))}\n\n")
            # Mark this pair as processed
            self.processed_pairs.add((entity_1, entity_2))

    def extract_information_text(self, sentences):
        for sentence in sentences:
            if len(self.noun_has_entity_relationship_entity_match(sentence)) == 1:
                self.noun_has_entity_relationship_entity(sentence, self.noun_has_entity_relationship_entity_match(sentence))
            elif len(self.one_to_one_relationship_match(sentence)) == 1:
                self.one_to_one_relationship(sentence, self.one_to_one_relationship_match(sentence))
            elif len(self.self_entity_relationship_entity_match(sentence)) == 1:
                self.self_entity_relationship_entity(sentence, self.self_entity_relationship_entity_match(sentence))
            elif len(self.has_entity_relationship_attributes_match(sentence)) == 1:
                self.has_entity_relationship_attributes(sentence, self.has_entity_relationship_attributes_match(sentence))

    def print_uml(self):
        content_uml = ""
        for key, values in self.entities:
            content_uml += f'entity "{unidecode.unidecode(key)}" as {unidecode.unidecode(key).lower()} {{\n' 
            if len(values) > 0:
                # doan code nay de dam bao khoa chinh luon nam o vi tri [0]
                for value in values:
                    if value.startswith("*") and values.index(value) != 0:
                        pos = values.index(value)
                        temp = values[pos]
                        for i in reversed(range(pos)):
                            values[i+1] = values[i]
                        values[0] = temp

                #in ra cac attribute
                for attr in values:
                    if (attr[0] != '-' and attr[0] != '.' and attr[0] != '^'):
                        content_uml += f'\t{unidecode.unidecode(attr).lower()}\n'
            content_uml += "}\n\n"
        for relation in self.relationships:
            content_uml += relation
        return "@startuml\n\n" + content_uml + "@enduml"

    def get_sql_data_type(self, word):
            word = word.lower()
            for kw in self.KEYWORDS_FLOAT:
                if kw in word:
                    return data_types['float']
            for kw in self.KEYWORDS_INT:
                if kw in word:
                    return data_types['int']
            if re.search(r'số', word, re.IGNORECASE):
                return data_types['số']
            elif re.search(r'ngày', word, re.IGNORECASE):
                return data_types['ngày']
            else:
                if re.search(r'mã', word, re.IGNORECASE):
                    return data_types['mã']
                elif re.search(r'tên', word, re.IGNORECASE):
                    return data_types['tên']
                else:
                    return data_types['text']

    def print_sql(self):
        sql = ""
        total_entities = len(self.entities)
        for idx, (key, values) in enumerate(self.entities):
            entity_name = unidecode.unidecode(key.lower())
            sql += f'CREATE TABLE {entity_name} (\n'
            attributes = []
            for attr in values:
                attr_name = unidecode.unidecode(attr[2:].lower())
                attr_type = self.get_sql_data_type(attr)
                
                if attr[0] == '*':
                    sql += f'\t{attr_name} {attr_type} CONSTRAINT PK_{entity_name} PRIMARY KEY,\n'
                elif attr[0] == '-':
                    attributes.append(attr_name)
                    foreign_entity_name = self.find_entity_by_attribute(attr)
                    sql += f'\t{attr_name} {attr_type},\n'
                    sql += f'\tCONSTRAINT FK_{entity_name}_{foreign_entity_name} FOREIGN KEY({attr_name}) REFERENCES {foreign_entity_name}({attr_name}),\n'
                elif attr[0] == '.':
                    referenced_entity_name, key_referenced_entity_name = self.find_entity_reference_by_attr(key.lower(), attr)
                    sql += f'\t{attr_name} {attr_type},\n'
                    sql += f'\tCONSTRAINT FK_{entity_name}_{referenced_entity_name} FOREIGN KEY({attr_name}) REFERENCES {referenced_entity_name}('
                    sql += key_referenced_entity_name
                    sql += '),\n'
                elif attr[0] == '^':
                    referenced_entity_name, key_optional_attribute  = self.find_entities_and_optional_attribute(key.lower())
                    sql += f'\t{attr_name} {attr_type},\n'
                    sql += f'\tCONSTRAINT FK_{entity_name}_{referenced_entity_name} FOREIGN KEY({attr_name}) REFERENCES {referenced_entity_name}('
                    sql += key_optional_attribute
                    sql += '),\n'
                else:
                    sql += f'\t{attr_name} {attr_type},\n'
            
            if attributes:
                sql += f'\tCONSTRAINT PK_{entity_name} PRIMARY KEY('
                sql += ', '.join(attributes) + "),\n"
            
            sql = sql.rstrip(',\n') + "\n"
            if idx == total_entities - 1:
                sql += ");\n\n"
            else:
                sql += ");\n\n"
        
        return sql
    
    def find_entity_by_attribute(self, attr):
        for attribute, entity in self.attributeReference:
            if attribute == attr:
                return unidecode.unidecode(entity)
        return ""
    
    def find_entity_reference_by_attr(self, key, attr_name):
        for ref in self.entityReference:
            if ref[0] == key:
                entity_name = ref[1]
                for entity in self.entities:
                    if entity[0] == entity_name:
                        for attribute in entity[1]:
                            if attribute == attr_name:
                                continue
                            if attribute[2:] == attr_name[2:]:
                                return unidecode.unidecode(ref[1]), unidecode.unidecode(attribute[2:])
        return "", ""

    def find_entities_and_optional_attribute(self, key):
        for entity, selfEntity in self.entityReferenceOptional:
            if entity == key:
                for ent in self.entities:
                    if ent[0] == selfEntity:
                        for attribute in ent[1]:
                            if attribute[0] == "*":
                                return unidecode.unidecode(selfEntity), unidecode.unidecode(attribute[2:])
        return ""

    def save_puml(self, content, output_folder, file_name):
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, f"{file_name}.puml")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
    def save_sql(self, content, output_folder, file_name):
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, f"{file_name}.sql")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
