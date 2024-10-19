import xml.etree.ElementTree as ET

from types import SimpleNamespace

def parse_xml_to_obj(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    xml_dict = xml_to_dict(root)
    return dict_to_simplenamespace(xml_dict)


def xml_to_dict(element):
    """Recursively converts an XML element and its children into a dictionary-like structure."""
    result = {element.tag: {} if element.attrib else None}

    if element.attrib:
        for attr_name, attr_value in element.attrib.items():
            result[element.tag][attr_name] = attr_value

    children = list(element)  # Get child elements

    # If the element has children, process them recursively
    if children:
        if result[element.tag] is None:
            result[element.tag] = {}
        for child in children:
            # Special handling for <attribute> tag with an 'id' attribute
            if child.tag == 'attribute' and 'id' in child.attrib:
                attr_id = child.attrib['id']
                # Store all attributes (value, handle, version, etc.)
                result[element.tag][attr_id] = {
                    k: v for k, v in child.attrib.items() if k != 'id'
                }
            else:
                child_result = xml_to_dict(child)
                child_tag = child.tag

                # Handle multiple children with the same tag (make them a list)
                if child_tag not in result[element.tag]:
                    result[element.tag][child_tag] = child_result[child_tag]
                else:
                    if not isinstance(result[element.tag][child_tag], list):
                        result[element.tag][child_tag] = [result[element.tag][child_tag]]
                    result[element.tag][child_tag].append(child_result[child_tag])
    # If element has text, ensure we handle that safely
    elif element.text and element.text.strip():
        result[element.tag] = element.text.strip()

    return result


def dict_to_simplenamespace(data):
    """Recursively converts a dictionary to a SimpleNamespace for dot notation access"""
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_simplenamespace(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_simplenamespace(i) for i in data]
    else:
        return data


def iterate_nested_nodes(lsx):
    nodes_list = []
    # First, ensure the path exists and the structure is valid
    if hasattr(lsx, 'save') and hasattr(lsx.save, 'region'):
        regions = lsx.save.region
        if not isinstance(regions, list):
            regions = [regions]  # Ensure we have a list to iterate over (if there's just one <region>)

        for region in regions:
            # Check if <node> exists within <region>
            if hasattr(region, 'node'):
                nodes = region.node
                if not isinstance(nodes, list):
                    nodes = [nodes]  # Handle single <node> by converting to list

                for node in nodes:
                    # Check if <children><node> exists
                    if hasattr(node, 'children') and hasattr(node.children, 'node'):
                        children_nodes = node.children.node

                        # Ensure it's a list (if there are multiple <children><node> elements)
                        if not isinstance(children_nodes, list):
                            children_nodes = [children_nodes]

                        # Add each child <node> to the list
                        nodes_list.extend(children_nodes)
    return nodes_list


def lookup_body_type(value):
    if value == "0":
        return "Male"
    elif value == "1":
        return "Female"
    else:
        return "Unknown"


def lookup_body_shape(value):
    if value == "0":
        return "Standard"
    elif value == "1":
        return "Strong"
    else:
        return "Unknown"


def lookup_availability(value):
    if value == "1":
        return "Available"
    elif value == "0":
        return "Unavailable"
    else:
        return "Hidden"


def lookup_really_tag(nodes):
    if isinstance(nodes, list):
        for node in nodes:
            if node.id == 'ReallyTags':
                return node.Object.value
    elif nodes.id == 'ReallyTags':
        return nodes.Object.value
    else:
        return None


def lookup_appearance_tag(nodes):
    if isinstance(nodes, list):
        for node in nodes:
            if node.id == 'AppearanceTags':
                return node.Object.value
    elif nodes.id == 'AppearanceTags':
        return nodes.Object.value
    else:
        return None