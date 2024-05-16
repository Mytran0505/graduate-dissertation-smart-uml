import re
import os
import spacy
import nltk
from nltk.corpus import conll2000
from POS_RuleBased import NGramTagChunker

data_types = {
    'code': 'INT',
    'name': 'VARCHAR(100)',
    'text': 'VARCHAR(255)',
    'number': 'INT',
    'decimal': 'DECIMAL(10, 2)',
    'date': 'DATE',  
    'time': 'TIME',
    'datetime': 'DATETIME',
    'float': 'FLOAT',
    'int' : 'INT'
}

nltk.download('conll2000')
train_data = conll2000.chunked_sents()
ntc = NGramTagChunker(train_data)

class UMLGenerator:
    KEYWORDS_FLOAT = ["capacity", "size", "length", "speed"]
    KEYWORDS_INT = ["duration"]
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.entities = {}
        self.relationships = []
        self.attributeReference = {}
        self.entityReference ={}

    def convert_name(self, noun_chunk):
        common_noun_pattern = re.compile(r'\b(?:a|an|the|this|that|these|those|each|one|many) \b', re.IGNORECASE)
        space_pattern = re.compile(r'\b \b')
        word = re.sub(space_pattern, '_', re.sub(common_noun_pattern, '', noun_chunk))

        if self.nlp(word)[0].pos_ == "NOUN" and self.nlp(word)[0].tag_ == "NNS":
            return self.nlp(word)[0].text.rstrip("s")
        return word

    def split_sentences(self, paragraph):
        return [str(sentence) for sentence in self.nlp(paragraph).sents]

    def clean_sentence(self, sentence):
        sentence = sentence.replace(" also", "")
        if "," in sentence:
            sentence = sentence.replace("and ", "")
        else:
            sentence = sentence.replace("and ", ". \n")
        sentence = sentence.replace(" or", ",")
        return sentence

    def print_relationship(self, entity_1, entity_2):
        if self.nlp(entity_2)[0].pos_ == "NOUN" and self.nlp(entity_2)[0].tag_ == "NNS":
            self.relationships.append(f"{self.convert_name(entity_1.lower())} |o--|{'{'} {self.convert_name(entity_2.lower())}\n\n")
        elif self.nlp(entity_2)[0].pos_ == "NOUN" and self.nlp(entity_2)[0].tag_ == "NN":
            self.relationships.append(f"{self.convert_name(entity_1.lower())} |o--|| {self.convert_name(entity_2.lower())}\n\n")
        elif (self.nlp(entity_2.split()[-1])[0].pos_ == "PROPN") and self.nlp(entity_2.split()[-1])[0].tag_ == "NNP":
            self.relationships.append(f"{self.convert_name(entity_1.lower())} |o--|{'{'} {self.convert_name(entity_2.lower())}\n\n")

    def print_relationship_reference(self, entity_1, entity_2):
        entityReference ={}
        if self.nlp(entity_2)[0].pos_ == "NOUN" and self.nlp(entity_2)[0].tag_ == "NN":
            entityReference[entity_2] = entity_1.lower()
            self.relationships.append(f"{self.convert_name(entity_1.lower())} |o--|| {self.convert_name(entity_2.lower())}\n\n")
            self.entityReference.update(entityReference)


    def there_are_entity_relationship_entity_match(self, sentence):
        entity_has_entity_1 = r"There are (\d+|many|some|few|a few) (\w+(\s\w+)*) in (\w+(\s\w+)*)"
        ehe1_matches = re.findall(entity_has_entity_1, sentence)
        return ehe1_matches

    def there_are_entity_relationship_entity(self, sentence, match):
        entity_1 = self.convert_name(match[0][-1].strip())
        entity_2 = self.convert_name(match[0][1].strip())
        if entity_1 not in self.entities:
            self.entities[entity_1] = []
        if entity_2 not in self.entities:
            self.entities[entity_2] = []
        self.print_relationship(match[0][-1].strip(), match[0][1].strip())

    def noun_has_entity_relationship_entity_match(self, sentence):
        entity_has_entity_2 = r"[The|Each|An|An|This|That|These|Those] (\w+(\s\w+)*) has (\d+|many|some|few|a few|a|an|one) (\w+(\s\w+)*)"
        ehe2_matches = re.findall(entity_has_entity_2, sentence)
        return ehe2_matches

    def noun_has_entity_relationship_entity(self, sentence, match):
        entity_1 = self.convert_name(match[0][0].strip())
        entity_2 = self.convert_name(match[0][3].strip())
        if entity_1 not in self.entities:
            self.entities[entity_1] = []
        if entity_2 not in self.entities:
            self.entities[entity_2] = []
        self.print_relationship(match[0][0].strip(), match[0][3].strip())

    def many_many_relationship_entity_match(self, sentence):
        entity_has_entity_2 = r"[The|Each|An|An|This|That|These|Those] (\w+(\s\w+)*) can be (\w+) (\w+) (\d+|many|some|few|a few|a|an|one) (\w+(\s\w+)*)"
        ehe2_matches = re.findall(entity_has_entity_2, sentence)
        return ehe2_matches

    def many_many_relationship_entity(self, sentence, match):
        entity_1 = self.convert_name(match[0][0].strip())
        entity_2 = self.convert_name(match[0][5].strip())
        verb = self.convert_name(match[0][2].strip())
        if entity_1 not in self.entities:
            self.entities[entity_1] = []
        if entity_2 not in self.entities:
            self.entities[entity_2] = []
        self.print_relationship_reference(match[0][0].strip(), match[0][5].strip())
        return verb

    # def noun_can_have_entity_relationship_entity_match(self, sentence):
    #     entity_has_entity_3 = r"[The|Each|An|An|This|That|These|Those] (\w+(\s\w+)*) (can|may|would|might|could) have (\d+|many|some|few|a few|a|an|one) (\w+(\s\w+)*)"
    #     ehe3_matches = re.findall(entity_has_entity_3, sentence)
    #     return ehe3_matches

    # def noun_can_have_entity_relationship_entity(self, sentence, match):
    #     entity_1 = self.convert_name(match[0][0].strip())
    #     entity_2 = self.convert_name(match[0][4].strip())
    #     if entity_1 not in self.entities:
    #         self.entities[entity_1] = []
    #     if entity_2 not in self.entities:
    #         self.entities[entity_2] = []
    #     self.print_relationship(match[0][0].strip(), match[0][4].strip())
    
    def entity_or_attribute_of_entity_match(self, sentence):
        entity_has_attributes_3 = r"The ([\w\s]+) of ([\w\s]+) is ([\w\s]+)"
        ehe3_matches = re.findall(entity_has_attributes_3, sentence)
        return ehe3_matches
    
    def entity_or_attribute_of_entity(self, sentence, match):
        if self.nlp(match[0][2])[0].pos_ == 'PROPN':
            entity_1 = self.convert_name(match[0][0].strip())
            entity_2 = self.convert_name(match[0][1].strip())
            if entity_1 not in self.entities:
                self.entities[entity_1] = []
            if entity_2 not in self.entities:
                self.entities[entity_2] = []
            self.print_relationship(match[0][0].strip(), match[0][1].strip())
        else:
            attribute = self.convert_name(match[0][0].strip())
            entity = self.convert_name(match[0][1].strip())
            self.entities[self.convert_name(entity)] = []
            self.entities[entity].extend([self.convert_name(match[0][0].strip())])
    
    def concate_word(self, chunk_tree, index):
        arr_item = []
        for i in chunk_tree[index]:
            arr_item.append(i[0])
        return " ".join(arr_item)

    def structure_sentence(self, sentence):
        chunk_tree = ntc.parse(nltk.pos_tag(sentence.split()))
        labels = []
        for i in chunk_tree:
            if isinstance(i[0], str): 
                continue
            elif i.label() in ['NP', 'PP', 'VP', 'and']:
                labels.append(i.label())
        if labels == ['NP', 'VP', 'PP', 'NP'] or labels == ['NP', 'VP', 'NP']:
            if len(self.concate_word(chunk_tree, len(chunk_tree) - 1).split(", ")) > 1:
                entity = self.convert_name(self.concate_word(chunk_tree, 0).strip())
                attribute = self.concate_word(chunk_tree, len(chunk_tree) - 1).split(", ")
                if entity not in self.entities:
                    self.entities[self.convert_name(entity)] = []
                self.entities[entity].extend([self.convert_name(attr) for attr in attribute])
            else:
                entity_1 = self.concate_word(chunk_tree, 0).strip()
                entity_2 = self.concate_word(chunk_tree, len(chunk_tree) - 1).strip()
                self.print_relationship(entity_1, entity_2)
                
    # def noun_belong_entity_relationship_entity_match(self, sentence):
    #     entity_has_entity_4 = r"[The|Each|An|An|This|That|These|Those] (\w+) (belongs|belong) to only one (\w+)"
    #     ehe4_matches = re.findall(entity_has_entity_4, sentence)
    #     return ehe4_matches

    # def noun_belong_entity_relationship_entity(self, sentence, match):
    #     entity_1 = self.convert_name(match[0][2].strip())
    #     entity_2 = self.convert_name(match[0][0].strip())
    #     if entity_1 not in self.entities:
    #         self.entities[entity_1] = []
    #     if entity_2 not in self.entities:
    #         self.entities[entity_2] = []
    #     self.print_relationship(match[0][2].strip(), match[0][0].strip())
        
    # def self_entity_relationship_entity_match(self, sentence):
    #     entity_has_entity_5 = r"[The|Each|An|An|This|That|These|Those] (\w+(\s\w+)*) in the (\w+(\s\w+)*) can be (\w+(\s\w+)*) by another (\w+(\s\w+)*)"
    #     ehe5_matches = re.findall(entity_has_entity_5, sentence)
    #     return ehe5_matches

    # def self_entity_relationship_entity(self, sentence, match):
    #     entity_1 = self.convert_name(match[0][-2].strip())
    #     entity_2 = self.convert_name(match[0][0].strip())
    #     self.relationships.append(f"{entity_1.lower()} |o--|{'{'} {entity_2.lower()}\n\n")
        
    # def has_entity_relationship_attributes_match(self, sentence):
    #     entity_has_attributes_1 = r"[The|Each|An|An|This|That|These|Those] (\w+) (?:is assigned an?|is identified by a unique) (\w+(?:,\s?\w+)*)"
    #     ehe6_matches = re.findall(entity_has_attributes_1, sentence)
    #     return ehe6_matches

    # def has_entity_relationship_attributes(self, sentence, match):
    #     entity = self.convert_name(match[0][0].strip())
    #     attribute = match[0][1].split(", ")
    #     key_attribute_identified = r"[The|Each|An|An|This|That|These|Those] (\w+) (?:is identified by a unique?) (\w+)"
    #     key_attribute_match = re.findall(key_attribute_identified, sentence)
    #     if (len(key_attribute_match)==1):
    #         attribute[0] = '* ' + attribute[0]
    #         for i in range(1,len(attribute)):
    #             attribute[i] = '+ ' + attribute[i]
    #     else:
    #         for i in range(0,len(attribute)):
    #             attribute[i] = '+ ' + attribute[i]
    #     if entity not in self.entities:
    #         self.entities[entity] = []
    #     self.entities[entity].extend([self.convert_name(attr) for attr in attribute])

    def add_attribute_from_reference(self):
        for entity, reference in self.entityReference.items():
            if reference in self.entities and entity in self.entities:
                key_attribute = None
                for attr in self.entities[reference]:
                    if attr.startswith('*'):
                        key_attribute = attr[2:]
                        break
                if key_attribute:
                    self.entities[entity].append(f'. {key_attribute}')

    # def check_many_many_rela(self, paragraph):
    #     many_many = r"[The|Each|An|An|This|That|These|Those] (\w+(\s\w+)*) can be (\w+) (\w+) (\d+|many|some|few|a few|a|an|one) (\w+(\s\w+)*)"
    #     rela_name = r"When (\w+), you must know the (\w+(?:,\s?\w+)*)"
    #     match_rela_name = re.findall(rela_name, paragraph)
    #     match_many_many = re.findall(many_many, paragraph)
    #     entity_1 = self.convert_name(match_many_many[0][0].strip())
    #     entity_2 = self.convert_name(match_many_many[0][5].strip())
    #     verb = self.convert_name(match_many_many[0][2].strip())
    #     if(entity_1 == self.convert_name(match_many_many[1][5].strip()) and entity_2 == self.convert_name(match_many_many[1][0].strip())):
    #         if(len(match_rela_name) == 1):
    #             table_rela_name = match_rela_name[0][0]
    #             attribute = match_rela_name[0][1].split(", ")
    #             for i in range(0,len(attribute)):
    #                 attribute[i] = '+ ' + attribute[i]
    #             self.entities[table_rela_name] = []
    #             self.entities[table_rela_name].extend([self.convert_name(attr) for attr in attribute])
    #             self.relationships.append(f"{self.convert_name(entity_1.lower())} |o--|{'{'} {self.convert_name(table_rela_name.lower())}\n\n")
    #             self.relationships.append(f"{self.convert_name(entity_2.lower())} |o--|{'{'} {self.convert_name(table_rela_name.lower())}\n\n")
    #         else:
    #             self.entities[verb] = []
    #             self.relationships.append(f"{self.convert_name(verb.lower())} |o--|{'{'} {self.convert_name(entity_1.lower())}\n\n")
    #             self.relationships.append(f"{self.convert_name(verb.lower())} |o--|{'{'} {self.convert_name(entity_2.lower())}\n\n")
    def check_many_many_rela(self, paragraph):
        many_many = r"[The|Each|An|An|This|That|These|Those] (\w+(\s\w+)*) can be (\w+) (\w+) (\d+|many|some|few|a few|a|an|one) (\w+(\s\w+)*)"
        rela_name = r"When (\w+), you must know the (\w+(?:,\s?\w+)*)"
        match_rela_name = re.findall(rela_name, paragraph)
        match_many_many = re.findall(many_many, paragraph)
        if (len(match_many_many) != 0):
            entity_1 = self.convert_name(match_many_many[0][0].strip())
            entity_2 = self.convert_name(match_many_many[0][5].strip())
            verb = self.convert_name(match_many_many[0][2].strip())
            key_attributes = {'': '', '': ''}
            if (entity_1 == self.convert_name(match_many_many[1][5].strip()) and entity_2 == self.convert_name(match_many_many[1][0].strip())):
                if(len(match_rela_name) == 1):
                    table_rela_name = match_rela_name[0][0]
                    attribute = match_rela_name[0][1].split(", ")
                    
                    for i, entities in enumerate([entity_1, entity_2]):
                        if entities in self.entities:
                            for attr in self.entities[entities]:
                                if attr.startswith('*'):
                                    key_attributes[i] = attr[2:]
                                    attribute.append(attr[2:])
                                    break
                    
                    for i in range(len(attribute)):
                        if attribute[i] in key_attributes.values():
                            attribute[i] = '- ' + attribute[i]
                            self.attributeReference[attribute[i]] = entity_1 if attribute[i] == key_attributes[0] else entity_2
                        else:
                            attribute[i] = '+ ' + attribute[i]
                    
                    self.entities[table_rela_name] = []
                    self.entities[table_rela_name].extend([self.convert_name(attr) for attr in attribute])
                    self.relationships.append(f"{self.convert_name(entity_1.lower())} |o--|{'{'} {self.convert_name(table_rela_name.lower())}\n\n")
                    self.relationships.append(f"{self.convert_name(entity_2.lower())} |o--|{'{'} {self.convert_name(table_rela_name.lower())}\n\n")
                else:
                    self.entities[verb] = []
                    self.relationships.append(f"{self.convert_name(verb.lower())} |o--|{'{'} {self.convert_name(entity_1.lower())}\n\n")
                    self.relationships.append(f"{self.convert_name(verb.lower())} |o--|{'{'} {self.convert_name(entity_2.lower())}\n\n")

    def extract_information_text(self, sentences):
        for sentence in sentences:
            # if len(self.there_are_entity_relationship_entity_match(sentence)) == 1:
            #     self.there_are_entity_relationship_entity(sentence, self.there_are_entity_relationship_entity_match(sentence))
            # el
            # if len(self.noun_has_entity_relationship_entity_match(sentence)) == 1:
            #     self.noun_has_entity_relationship_entity(sentence, self.noun_has_entity_relationship_entity_match(sentence))
            # elif len(self.many_many_relationship_entity_match(sentence)) == 1:
            #     self.many_many_relationship_entity(sentence, self.many_many_relationship_entity_match(sentence))
            # elif len(self.entity_or_attribute_of_entity_match(sentence)) == 1:
            #     self.entity_or_attribute_of_entity(sentence, self.entity_or_attribute_of_entity_match(sentence))
            # else:
                self.structure_sentence(sentence)
            

    def print_uml(self):
        content_uml = ""
        for key, values in self.entities.items():
            content_uml += f'entity "{key}" as {key.lower()} {{\n'
            if len(values) > 0:
                for attr in values:
                    if (attr[0] != '-' and attr[0] != '.'): 
                        content_uml += f'   {attr.lower()}\n'
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
            if re.search(r'number', word, re.IGNORECASE):
                return data_types['number']
            elif re.search(r'date', word, re.IGNORECASE):
                return data_types['date']
            else:
                if re.search(r'code', word, re.IGNORECASE):
                    return data_types['code']
                elif re.search(r'name', word, re.IGNORECASE):
                    return data_types['name']
                else:
                    return data_types['text']

    def print_sql(self):
        sql = ""
        total_entities = len(self.entities)
        for idx, (key, values) in enumerate(self.entities.items()):
            attributes = []
            sql += f'CREATE TABLE {key.lower()} (\n'
            if len(values) > 0:
                for attr in values:
                    attr_type = self.get_sql_data_type(attr)
                    if attr[0] == '*':
                        sql += f'  {attr[2:]} {attr_type} CONSTRAINT PK_{key.lower()} PRIMARY KEY,\n'
                    elif attr[0] == '-':
                        attributes.append(attr[2:])
                        sql += f'  {attr[2:]} {attr_type},\n'
                        sql += f'  CONSTRAINT FK_{key.lower()}_{self.attributeReference[attr]} FOREIGN KEY({attr[2:]}) REFERENCES {self.attributeReference[attr]}({attr[2:]}),\n'
                    elif attr[0] == '.':
                        sql += f'  {attr[2:]} {attr_type},\n'
                        sql += f'  CONSTRAINT FK_{key.lower()}_{self.entityReference[key.lower()]} FOREIGN KEY({attr[2:]}) REFERENCES {self.entityReference[key.lower()]}({attr[2:]}),\n'                       
                    else:
                        sql += f'  {attr[2:]} {attr_type},\n'
                if attributes:
                    sql += f'  CONSTRAINT PK_{key.lower()} PRIMARY KEY('
                    sql += ', '.join(attributes) + "),\n"
            sql = sql[:-2] + "\n"
            if idx == total_entities - 1:
                sql += ");\n\n"
            else:
                sql += ");\n\n"
        return sql
    
    def save_puml(self, content, output_folder, file_name):
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, f"{file_name}.puml")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"UML content saved to file {file_path}")
        
    def save_sql(self, content, output_folder, file_name):
        os.makedirs(output_folder, exist_ok=True)
        file_path = os.path.join(output_folder, f"{file_name}.sql")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"UML content saved to file {file_path}")