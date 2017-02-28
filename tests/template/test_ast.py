from spade.template.parser import TemplateParser

def validate_header(struct):
    assert struct is not None

def validate_blob(struct):
    assert struct is not None

def validate_file(struct):
    assert struct is not None

def test_parser_validtemplate1():
    # Parse template
    parser = TemplateParser()
    assert parser is not None
    ast = parser.parse_file("tests/template/validtemplate1.stf")
    assert ast is not None

    # Do we have all our structs?
    assert ast.structs is not None
    assert len(ast.structs) == 3

    # Make sure all expected structs exist and are good in ast
    expected_structs = ["header_t", "blob_t", "FILE"]
    for struct in ast.structs:
        for s in expected_structs:
            if struct.name == s:
                expected_structs.remove(s)
    assert len(expected_structs) == 0

    # Validate structs
    validate_header(ast.struct("header_t"))
    validate_blob(ast.struct("blob_t"))
    validate_file(ast.struct("FILE"))
