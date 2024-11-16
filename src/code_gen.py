import os
from node import Node

class CodeGenerator:
    def __init__(self, output_file, ast):
        self.root = ast[0]
        self.code = ""
        self.output_file = output_file

        self.int_vector = []
        self.float_vector = []
        self.string_vector = []
    
    def generate_code(self):
        self.code += "#include <iostream>\n"
        self.code += "#include <string>\n"
        self.code += "#include \"entity.hpp\"\n"
        
        # get code ready
        self.generate_code_recv(self.root)

        # Write to file (make sure directory exists)
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(self.code)

    def generate_code_recv(self, node):
        if node.children:
            for c in node.children:
                self.generate_code_recv(c)
        else:  # Leaf node
            self.process_node(node)

    def handle_literal(self, value, var_type, vector):
        if value in vector:
            index = vector.index(value)
        else:
            index = len(vector)
            vector.append(value)
            self.code += f"Entity {var_type}_{index}({var_type.upper()}, \"{value}\");\n"
        self.code += f"{var_type}_{index};\n"

    def process_node(self, node):
        if node.n_type == 'Start':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Empty':
            # TODO(us): hacer
            pass
        elif node.n_type == 'EmptyStatement':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Statement':
            # TODO(us): hacer
            pass
        elif node.n_type == 'VarName':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ForLoop':
            # TODO(us): hacer
            pass
        elif node.n_type == 'WhileLoop':
            # TODO(us): hacer
            pass
        elif node.n_type == 'TryRule':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ExceptRule':
            # TODO(us): hacer
            pass
        elif node.n_type == 'IfRule':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ElifRule':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ElseRule':
            # TODO(us): hacer
            pass
        elif node.n_type == 'NoneLiteral':
            # TODO(us): hacer
            pass
        elif node.n_type == 'IntegerLiteral':
            self.handle_literal(node.value, 'int', self.int_vector)
        elif node.n_type == 'FloatLiteral':
            self.handle_literal(node.value, 'double', self.float_vector)
        elif node.n_type == 'StringLiteral':
            self.handle_literal(node.value, 'string', self.string_vector)
        elif node.n_type == 'DefFunction':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Parameter':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ParameterList':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ParameterWithDefault':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ReturnStatement':
            # TODO(us): hacer
            pass
        elif node.n_type == 'CallFunction':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ParameterWithAssignment':
            # TODO(us): hacer
            pass
        elif node.n_type == 'BooleanLiteral':
            # TODO(us): hacer
            pass
        elif node.n_type == 'AccessVariable':
            # TODO(us): hacer
            pass
        elif node.n_type == 'AccessVarList':
            # TODO(us): hacer
            pass
        elif node.n_type == 'MathExpression':
            # TODO(us): hacer
            pass
        elif node.n_type == 'MathSymbol':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Parenthesis':
            # TODO(us): hacer
            pass
        elif node.n_type == 'MathAssign':
            # TODO(us): hacer
            pass
        elif node.n_type == 'LogicSymbols':
            # TODO(us): hacer
            pass
        elif node.n_type == 'CmpSymbols':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Tuple':
            # TODO(us): hacer
            pass
        elif node.n_type == 'EmptyList':
            # TODO(us): hacer
            pass
        elif node.n_type == 'List':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ListTupleContent':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Set':
            # TODO(us): hacer
            pass
        elif node.n_type == 'SetContent':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Dictionary':
            # TODO(us): hacer
            pass
        elif node.n_type == 'EmptyDictionary':
            # TODO(us): hacer
            pass
        elif node.n_type == 'DictionaryContent':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Print':
            # TODO(us): hacer
            self.code += "std::cout << "
            pass
        elif node.n_type == 'EmptyPrint':
            # TODO(us): hacer
            pass
        elif node.n_type == 'PrintDataStructs':
            # TODO(us): hacer
            pass
        elif node.n_type == 'VariableAssignment':
            # TODO(us): hacer
            pass
        elif node.n_type == 'AttributeMethod':
            # TODO(us): hacer
            pass
        elif node.n_type == 'ClassDefinition':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Inheritance':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Continue':
            # TODO(us): hacer
            pass
        elif node.n_type == 'Break':
            # TODO(us): hacer
            pass

# def angie():
#   return 20

# pepito = 5 + angie()


# Entity angie(){
#   return Entity(int, 20)
# }
# Entity a5 = Entity(int, 5)
# Entity pepito = a5 + angie()