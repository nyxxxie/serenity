import logging
from spade.template import parser
from spade.template import generator

def from_file(target_file_path: str, template_file: str):
    """Transforms a target + a .stf file into a workable template.

    :param stf_file: STF file.
    :param target_file: File to apply STF to.
    :return: A spade TRoot cooresponding with a fully-formed template tree.
    """
    # Parse template file
    ast_root = parser.TemplateParser.parse_file(multistruct1)
    if not ast_root:
        return None

    with open(target_file_path, "rb") as f:
        return generator.generate_template(f, ast_root)
