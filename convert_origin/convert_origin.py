import os
import sys

from jinja2 import Template, Environment, FileSystemLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import *


def generate_tbl_file(lsx):
    origin_nodes = iterate_nested_nodes(lsx)
    env = Environment(loader=FileSystemLoader('.'))
    env.filters['lookup_body_type'] = lookup_body_type
    env.filters['lookup_body_shape'] = lookup_body_shape
    env.filters['lookup_availability'] = lookup_availability
    env.filters['lookup_really_tag'] = lookup_really_tag
    env.filters['lookup_appearance_tag'] = lookup_appearance_tag
    template = env.get_template('Origins.tbl.j2')
    return template.render(origin_nodes=origin_nodes)


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print("""
    Usage: python convert_origin.py <input lsx file>
    Example: python convert_origin.py Origins.lsx > Origins.tbl
    """)
        sys.exit(2)

    input_lsx = sys.argv[1]
    lsx = parse_xml_to_obj(input_lsx)
    tbl = generate_tbl_file(lsx)
    print(tbl)
