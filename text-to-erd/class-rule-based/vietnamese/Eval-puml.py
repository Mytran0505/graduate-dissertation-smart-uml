import os
import csv
import re


def parse_file(filename):
    entities = {}
    relationships = set()
    count = 0
    #​symbols
    with open(filename, 'r') as file:
        content = file.read()
        # Tìm tất cả các khối entity
        entity_blocks = re.findall(r'entity "(.*?)" as (.*?) {(.*?)}', content, re.DOTALL)
        for entity_match in entity_blocks:
            entity_name = entity_match[1]
            count = count+1
            attributes = [attr.strip() for attr in entity_match[2].split('\n') if attr.strip()]
            entities[entity_name] = attributes
            count = count+ len(attributes)
        
        # Tìm tất cả các quan hệ
        pattern = re.compile(r'(\w+)\s*(\|o--\|\{|\|\|--o\{|}\|\.\.\|\||\|o--\|\||}o..o\||}\|--o\|)\s*(\w+)')
        matches = re.findall(pattern, content)
        for match in matches:
            relationships.add((match[0], match[1], match[2]))
            count = count +1
    
    return entities, relationships, count
# Hàm để so sánh hai tập entities, attributes và relationships
def compare(expert_entities, expert_relationships, machine_entities, machine_relationships):
    equivalent_entities = set()
    equivalent_attributes = {}
    equivalent_relationships = set()
    count = 0
    # So sánh entities và attributes
    for machine_entity, machine_attributes in machine_entities.items():
        if machine_entity in expert_entities:
            equivalent_entities.add(machine_entity)
            expert_attributes = expert_entities[machine_entity]
            matching_attributes = set(machine_attributes) & set(expert_attributes)
            if matching_attributes:
                equivalent_attributes[machine_entity] = matching_attributes
        count += len(matching_attributes)
    # So sánh relationships
    for relationship in machine_relationships:
        entity1_machine, symbol, entity2_machine = relationship
        if (symbol in ["|o--|{", "}|--o|"] and 
            any(rel[1] in ["|o--|{", "}|--o|"] and rel[0] == entity2_machine and rel[2] == entity1_machine for rel in expert_relationships)):
            equivalent_relationships.add(relationship)
        elif relationship in expert_relationships:
            equivalent_relationships.add(relationship)
    count += len(equivalent_entities) + len(equivalent_relationships)
    return equivalent_entities, equivalent_attributes, equivalent_relationships, count

expert_folder = "export/puml/expert-solution/"
machine_folder = "export/puml/rule-based-solution/"
result_folder = "evaluation-result/puml/"
result_csv = "evaluation-result/puml-evaluation-result.csv"
correct_result = 0
results = []

if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# Iterate through each file in the expert_folder directory
for expert_file_name in os.listdir(expert_folder):
    expert_file = os.path.join(expert_folder, expert_file_name)
    test_number = expert_file_name.split('-')[0].replace('test', '')
    machine_file = os.path.join(machine_folder, f"test{test_number}-rule-based-solution.puml")
    
    if not os.path.exists(expert_file) or not os.path.exists(machine_file):
        continue

    expert_entities, expert_relationships, expert_count = parse_file(expert_file)
    machine_entities, machine_relationships, machine_count = parse_file(machine_file)
    
    equivalent_entities, equivalent_attributes, equivalent_relationships, compare_count = compare(expert_entities, expert_relationships, machine_entities, machine_relationships)
    
    output_txt = os.path.join(result_folder, f"test{test_number}-evaluation-result.txt")
    with open(output_txt, "w", encoding="utf-8") as file:
        file.write("Equivalent Entities:\n" + str(equivalent_entities) + "\n")
        # Printing equivalent attributes
        file.write("Equivalent Attributes:\n")
        for entity, attrs in equivalent_attributes.items():
            file.write(entity + ": " + ", ".join(attrs) + "\n")
        # Printing equivalent relationships
        file.write("Equivalent Relationships:\n")
        for relationship in equivalent_relationships:
            file.write(f"{relationship[0]} - {relationship[2]}\n")
        correct_result = (compare_count/expert_count)*100 if expert_count > 0 else 0
        file.write(f"The expert's number of elements = {expert_count}\n")
        file.write(f"The number of elements in the machine is correct with the machine's number of elements = {compare_count}\n")
        file.write(f"The correct result = {correct_result}%\n")

    results.append({
        "Test": f"test{test_number}",
        "The expert's number of elements": expert_count,
        "The number of elements in the machine is correct with the machine's number of elements": compare_count,
        "The correct result (%)": correct_result
    }) 

with open(result_csv, "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ["Test", "The expert's number of elements", "The number of elements in the machine is correct with the machine's number of elements", "The correct result (%)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)

# Calculate the average correct result
total_correct_result = sum(result["The correct result (%)"] for result in results)
average_correct_result = total_correct_result / len(results)

print(f"The average correct result is: {average_correct_result}%")