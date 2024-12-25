from xml.dom import minidom
from lxml import etree

# Load the XML file
def load_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return minidom.parse(file)

# Save the modified XML back to a file
def save_xml(document, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        document.writexml(file, indent="  ", addindent="  ", newl="\n")

# Add a new element
def add_element(document):
    characters = document.getElementsByTagName('characters')[0]
    new_character = document.createElement('character')
    new_character.setAttribute('role', 'neutral')
    new_character.appendChild(document.createTextNode('Торгівець'))
    characters.appendChild(new_character)

# Modify an existing element
def modify_element(document):
    description = document.getElementsByTagName('description')[0]
    description.firstChild.nodeValue += " Гра включає багатокористувацький режим."

# Add a new attribute
def add_attribute(document):
    release = document.getElementsByTagName('release')[0]
    release.setAttribute('platform', 'PC and Xbox')

# Remove an existing attribute
def remove_attribute(document):
    title = document.getElementsByTagName('title')[0]
    if title.hasAttribute('status'):
        title.removeAttribute('status')

# Modify an existing attribute
def modify_attribute(document):
    location = document.getElementsByTagName('location')[0]
    location.setAttribute('danger', 'середня')

# Add a hierarchy of elements
def add_hierarchy(document):
    artifacts = document.getElementsByTagName('artifacts')[0]
    new_artifact = document.createElement('artifact')
    new_artifact.setAttribute('name', 'Золотий компас')
    new_artifact.setAttribute('rarity', 'дуже висока')

    sub_element = document.createElement('details')
    sub_element.setAttribute('discovered', '2023')
    sub_element.appendChild(document.createTextNode('Знайдений у Рудому лісі.'))

    new_artifact.appendChild(sub_element)
    artifacts.appendChild(new_artifact)

# Count elements without children
def count_leaf_elements(document):
    return sum(1 for element in document.getElementsByTagName('*') if not element.hasChildNodes())

# Count attributes matching criteria
def count_attributes(document, criterion):
    return sum(
        1 for element in document.getElementsByTagName('*')
        for attr in element.attributes.keys()
        if criterion in element.attributes[attr].value
    )

# Validate XML against XSD
def validate_xml(xml_path, xsd_path):
    with open(xsd_path, 'rb') as schema_file:
        schema_root = etree.XML(schema_file.read())
    schema = etree.XMLSchema(schema_root)

    with open(xml_path, 'rb') as xml_file:
        xml_doc = etree.parse(xml_file)

    try:
        schema.assertValid(xml_doc)
        print("XML документ є валідним відповідно до XSD-схеми.")
    except etree.DocumentInvalid as e:
        print("Помилка валідації XML документа:", e)

# Main execution
def main():
    file_path = 'XmStalker2.xml'  # Path to the XML file
    xsd_path = 'XsStalker2.xsd'  # Path to the XSD file
    document = load_xml(file_path)

    add_element(document)
    modify_element(document)
    add_attribute(document)
    remove_attribute(document)
    modify_attribute(document)
    add_hierarchy(document)

    leaf_count = count_leaf_elements(document)
    attribute_count = count_attributes(document, 'висока')

    save_xml(document, 'modified_game.xml')

    print(f"Кількість елементів без дочірніх: {leaf_count}")
    print(f"Кількість атрибутів, що відповідають критерію: {attribute_count}")

    # Validate the modified XML against the XSD schema
    validate_xml('modified_game.xml', xsd_path)

if __name__ == "__main__":
    main()
