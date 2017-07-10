import logging
from spade.template import parser
from spade.template import generator

def from_file(target_file: str, template_file: str):
    """Transforms a target + a .stf file into a workable template.

    :param stf_file: STF file.
    :param target_file: File to apply STF to.
    :return: A spade TRoot cooresponding with a fully-formed template tree.
    """
    # Parse template file
    ast = parser.TemplateParser.parse_file(template_file)
    if not ast:
        return None

    # Find Ast root

    # Generate template tree
    return generator.generate_template(target_file, ast)
