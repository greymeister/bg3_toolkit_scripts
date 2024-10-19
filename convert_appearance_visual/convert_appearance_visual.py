import os
import sys

from jinja2 import Template, Environment, FileSystemLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import *


def generate_tbl_file(lsx):
    cca_nodes = iterate_nested_nodes(lsx)
    env = Environment(loader=FileSystemLoader('.'))
    env.filters['lookup_body_type'] = lookup_body_type
    env.filters['lookup_body_shape'] = lookup_body_shape
    template = env.get_template('CharacterCreationAppearanceVisuals.tbl.j2')
    return template.render(cca_nodes=cca_nodes)


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print("""
    Usage: python convert_appearance_visual.py <input lsx file>
    Example: python convert_appearance_visual.py CharacterCreationAppearanceVisuals.lsx > CharacterCreationAppearanceVisuals.tbl
    """)
        sys.exit(2)

    input_lsx = sys.argv[1]
    lsx = parse_xml_to_obj(input_lsx)
    tbl = generate_tbl_file(lsx)
    print(tbl)
