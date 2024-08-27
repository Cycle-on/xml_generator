import ast


def get_variable_names(file_path):
    with open(file_path, 'r') as file:
        node = ast.parse(file.read(), filename=file_path)

    variable_names = set()

    class VariableVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                variable_names.add(node.id)
            self.generic_visit(node)

    VariableVisitor().visit(node)
    return variable_names


# Пример использования
file_path = 'constants.py'  # Замените на путь к вашему файлу
variables = get_variable_names(file_path)
print(variables)
