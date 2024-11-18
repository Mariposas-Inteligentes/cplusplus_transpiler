def add_tabs(count):
    tabs = "\t"
    tabs *= count
    return tabs

def indent_code(code):
    indent_count = 0
    new_code = ""
    for line in code.splitlines():
        if "{\n" in line:
            new_code += add_tabs(indent_count) + line
            indent_count += 1
            break
        if "{\n" in line:
            indent_count -= 1
        new_code += add_tabs(indent_count) + line
    return new_code