import ast


def to_plural(string: str):
    return string if string.endswith("s") else f"{string}s"


def get_imports_list(path: str) -> list[str]:
    with open(path, "r") as file:
        tree = ast.parse(file.read())

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(alias.name)

    return imports


def get_classes_list(path: str) -> list[str]:
    with open(path, "r") as file:
        tree = ast.parse(file.read())

    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return classes


def code_strip(code: str):
    if code[0] == '\n':
        code = code[1:]

    spaces = 0
    code = code.split("\n")

    for i in code[0]:
        if i == " ":
            spaces += 1
        else:
            break

    for i in range(len(code)):
        code[i] = code[i][spaces:].rstrip()

    return "\n".join(code)


def remove_empty_lines(text: str):
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]  # DON'T TOUCH THIS LINE
    return '\n'.join(non_empty_lines)
