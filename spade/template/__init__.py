import logging
from spade.template import parser
from spade.template import generator

def from_file(template_file_path: str, target_file_path: str):
    """Transforms a .stf and target file into a workable template.

    :param template_file_path: Spade template file to apply to the target file.
    :param target_file_path: File to apply the the template to.
    :return: A spade TRoot cooresponding with a fully-formed template tree.
    """
    # Parse template file
    ast_root = parser.TemplateParser.parse_file(template_file_path)
    if not ast_root:
        return None

    with open(target_file_path, "rb") as f:
        return generator.generate_template(f, ast_root)
