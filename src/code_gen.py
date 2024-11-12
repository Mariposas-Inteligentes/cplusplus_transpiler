from node import Node

class CodeGenerator:
    def __init__(self, output_file, ast):
        self.root = ast[0]
        self.code = ""
        self.output_file = output_file
    
    def generate_code(self):
        # TODO: generate code string
        code += "#include <iostream>\n"
        code += "#include <string>\n"
        code += "#include \"entity.hpp\"\n"
        self.generate_code_recv(self.root)
    
        # TODO: place code in ouput file

    def generate_code_recv(self, node):
        if node.children != None:
            for c in node.children:
                self.generate_code_recv(c)
        else:  # Leaf
            self.process_node(node)

    def process_node(self, node):
        if node.type == 'Start':
            # TODO(us): hacer
            pass
        elif node.type == 'Empty':
          # TODO(us): hacer
            pass
        elif node.type == 'EmptyStatement':
            # TODO(us): hacer
            pass
        elif node.type == 'Statement':
            # TODO(us): hacer
            pass
        elif node.type == 'VarName':
            # TODO(us): hacer
            pass
        elif node.type == 'ForLoop':
          # TODO(us): hacer
            pass
        elif node.type == 'WhileLoop':
          # TODO(us): hacer
            pass
        elif node.type == 'TryRule':
          # TODO(us): hacer
            pass
        elif node.type == 'ExceptRule':
          # TODO(us): hacer
            pass
        elif node.type == 'IfRule':
          # TODO(us): hacer
            pass
        elif node.type == 'ElifRule':
          # TODO(us): hacer
            pass
        elif node.type == 'ElseRule':
          # TODO(us): hacer
            pass
        elif node.type == 'NoneLiteral':
          # TODO(us): hacer
            pass
        elif node.type == 'StringLiteral':
          # TODO(us): hacer
            pass
        elif node.type == 'DefFunction':
          # TODO(us): hacer
            pass
        elif node.type == 'Parameter':
          # TODO(us): hacer
            pass
        elif node.type == 'ParameterList':
          # TODO(us): hacer
            pass
        elif node.type == 'ParameterWithDefault':
          # TODO(us): hacer
            pass
        elif node.type == 'ReturnStatement':
          # TODO(us): hacer
            pass
        elif node.type == 'CallFunction':
          # TODO(us): hacer
            pass
        elif node.type == 'ParameterWithAssignment':
          # TODO(us): hacer
            pass
        elif node.type == 'IntegerLiteral':
          # TODO(us): hacer
            pass
        elif node.type == 'FloatLiteral':
          # TODO(us): hacer
            pass
        elif node.type == 'BooleanLiteral':
          # TODO(us): hacer
            pass
        elif node.type == 'AccessVariable':
          # TODO(us): hacer
            pass
        elif node.type == 'AccessVarList':
          # TODO(us): hacer
            pass
        elif node.type == 'MathExpression':
          # TODO(us): hacer
            pass
        elif node.type == 'MathSymbol':
          # TODO(us): hacer
            pass
        elif node.type == 'Parenthesis':
          # TODO(us): hacer
            pass
        elif node.type == 'MathAssign':
          # TODO(us): hacer
            pass
        elif node.type == 'LogicSymbols':
          # TODO(us): hacer
            pass
        elif node.type == 'CmpSymbols':
          # TODO(us): hacer
            pass
        elif node.type == 'Tuple':
          # TODO(us): hacer
            pass
        elif node.type == 'EmptyList':
          # TODO(us): hacer
            pass
        elif node.type == 'List':
          # TODO(us): hacer
            pass
        elif node.type == 'ListTupleContent':
          # TODO(us): hacer
            pass
        elif node.type == 'Set':
          # TODO(us): hacer
            pass
        elif node.type == 'SetContent':
          # TODO(us): hacer
            pass
        elif node.type == 'Dictionary':
          # TODO(us): hacer
            pass
        elif node.type == 'EmptyDictionary':
          # TODO(us): hacer
            pass
        elif node.type == 'DictionaryContent':
          # TODO(us): hacer
            pass
        elif node.type == 'Print':
          # TODO(us): hacer
            pass
        elif node.type == 'EmptyPrint':
          # TODO(us): hacer
            pass
        elif node.type == 'PrintDataStructs':
          # TODO(us): hacer
            pass
        elif node.type == 'VariableAssignment':
          # TODO(us): hacer
            pass
        elif node.type == 'AttributeMethod':
          # TODO(us): hacer
            pass
        elif node.type == 'ClassDefinition':
          # TODO(us): hacer
            pass
        elif node.type == 'Inheritance':
          # TODO(us): hacer
            pass
        elif node.type == 'Continue':
          # TODO(us): hacer
            pass
        elif node.type == 'Break':
          # TODO(us): hacer
            pass
