import os
from node import Node

class CodeGenerator:
    def __init__(self, output_file, ast):
        self.root = ast[0]
        self.variables = ""
        self.code = ""
        self.classes = ""
        self.functions = ""
        self.output_file = output_file

        self.int_vector = []
        self.float_vector = []
        self.string_vector = []
        self.existing_variables = {}
    
    def generate_code(self):
        # Get code ready
        self.generate_code_recv(self.root)
        self.code = self.variables + self.code

        # Always define true and false
        self.code = "Entity bool_true(INT, \"1\");\n" + self.code
        self.code = "Entity bool_false(INT, \"0\");\n" + self.code

        # Append necessary includes
        self.code = "int main() {\n" + self.code
        self.code = "#include \"entity.hpp\"\n" + self.code
        self.code = "#include <string>\n" + self.code
        self.code = "#include <iostream>\n" + self.code
        self.code += "return 0;\n}"

        # Write to file (make sure directory exists)
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(self.code)

    def generate_code_recv(self, node):
        if node.n_type in ['IfRule', 'ElifRule', 'ElseRule']:
            self.process_node(node)
        else:
            self.process_node(node)
            if node.children:
                for child in node.children:
                    self.generate_code_recv(child)

    def handle_literal(self, value, var_type, vector):
        if value in vector:
            index = vector.index(value)
        else:
            index = len(vector)
            vector.append(value)
            if var_type == "string" and len(value) > 1:  # Remove " and ' to avoid problems
                stripped_value = value[1:-1]
            else:
                stripped_value = value

            self.variables += f"Entity {var_type}_{index}({var_type.upper()}, \"{stripped_value}\");\n"
        return f"{var_type}_{index}"
    

    def process_variable_assignment(self, node):
        variable_name = node.children[0].value
        cpp_variable_name = f"py_{variable_name}"

        operator = node.children[1].value # operator
        right_node = node.children[2]  # asignee

        value = self.get_cpp_value(right_node)

        if cpp_variable_name not in self.existing_variables:
            # Define the variable for the first time

            # define variable at the beginning of document
            self.variables += f"Entity {cpp_variable_name} = Entity(INT, \"0\");\n"
            # use in the variable
            self.code +=  f"{cpp_variable_name} {operator} {value};\n"
            self.existing_variables[cpp_variable_name] = True
        else:
            # Update the variable if it already exists
            self.code += f"{cpp_variable_name} {operator} {value};\n"


    def process_math_expression(self, node):
        components = [] # to store each operand

        for child in node.children:
            if child.n_type == 'MathSymbol': # child is an operator
                components.append(child.value)
            elif child.n_type == 'Parenthesis': # child is an operator
                inner_expression = self.get_cpp_value(child.children[0]) 
                components.append(f"({inner_expression})")
            else: # Normal operand
                components.append(self.get_cpp_value(child))

        # Join everything
        return " ".join(components)
    
    def process_print(self, node):
        code_to_add = "std::cout"
        for child in node.children:
            if child.n_type == 'MathExpression':
                expression = self.process_math_expression(child)
                code_to_add += f" << {expression}"
            else: 
               code_to_add += f" << {self.get_cpp_value(child)}"
        code_to_add += " << std::endl;\n"
        self.code += code_to_add

    def process_if(self, node):
        condition = self.get_cpp_value(node.children[0])
        self.code += f"if (({condition}).is_true()) {{\n"
        ended = False # avoid extra curly brackets
        for child in node.children[1:]:
            if (child.n_type == "ElifRule" or child.n_type == "ElseRule") and not ended:
                self.code += "}\n"
                ended = True
            self.generate_code_recv(child)
        if not ended:
            self.code += "}\n"

    def process_elif(self, node):
        # the else has to be apart from the if in case we need
        # to define a variable for the condition
        condition = self.get_cpp_value(node.children[0])
        self.code += f"else if (({condition}).is_true())"
        self.code += "{\n"
        ended = False
        for child in node.children[1:]:
            if (child.n_type == "ElifRule" or child.n_type == "Else") and not ended:
                self.code += "}\n"
            self.generate_code_recv(child)
        if not ended:
            self.code += "}\n"

    def process_else(self, node):
        self.code += "else {\n"
        for child in node.children:
            self.generate_code_recv(child)
        self.code += "}\n"

    def process_function_call(self, node):
        function_name = node.children[0].value

        args = [self.get_cpp_value(arg) for arg in node.children[1:]]

        if function_name == 'sum':
            if len(args) == 1 and args[0].startswith("std::vector"):
                self.code += f"std::accumulate({args[0]}.begin(), {args[0]}.end(), 0);\n"
            else:
                return " + ".join(args)
        elif function_name in ['int', 'string', 'double', 'bool']:
            cpp_type = function_name.upper() if function_name != 'string' else 'std::string'
            return f"static_cast<{cpp_type}>({args[0]})"
        elif function_name == 'type':
            return f"{args[0]}.get_type()"
        else:
            return f"{function_name}({', '.join(args)})"

    def process_while_loop(self, node):
        condition = self.get_cpp_value(node.children[0])
        self.code += f"while (({condition}).is_true()) {{\n"
        for child in node.children[1:]:
            self.generate_code_recv(child)
        self.code += "}\n"

    def process_for_loop(self, node): # TODO(us): implement when we have call function
        pass



    def get_cpp_value(self, value_node):
        if value_node.n_type == 'IntegerLiteral':
            return self.handle_literal(value_node.value, 'int', self.int_vector)
        elif value_node.n_type == 'FloatLiteral':
            return self.handle_literal(value_node.value, 'double', self.float_vector)
        elif value_node.n_type == 'StringLiteral':
            return self.handle_literal(value_node.value, 'string', self.string_vector)
        elif value_node.n_type == 'VarName':
            return f"py_{value_node.value}"
        elif value_node.n_type == 'MathExpression':
            return self.process_math_expression(value_node)
        elif value_node.n_type == 'BooleanLiteral':
            return "bool_true" if value_node.value == True else "bool_false"
        else:
            raise ValueError(f"Unsupported value node type: {value_node.n_type}")


    # TODO(us): when we have something that should return true or false, we need to use the value
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

        elif node.n_type == 'WhileLoop':
            self.process_while_loop(node)

        elif node.n_type == 'ForLoop':
            self.process_for_loop(node)

        elif node.n_type == 'TryRule':
            # TODO(us): hacer
            pass

        elif node.n_type == 'ExceptRule':
            # TODO(us): hacer
            pass

        elif node.n_type == 'IfRule':
            self.process_if(node)

        elif node.n_type == 'ElifRule':
            self.process_elif(node)

        elif node.n_type == 'ElseRule':
            self.process_else(node)

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
            self.process_function_call(node)

        elif node.n_type == 'ParameterWithAssignment':
            # TODO(us): hacer
            pass

        elif node.n_type == 'BooleanLiteral':
            # TODO(us): think if it is needed (When I uncomment this code, it just trows boolean values in the code)
            # Test input: x = True + 8 - False
            # cpp_value = "bool_true" if node.value == True else "bool_false"
            # self.code += f"{cpp_value};\n"
            pass 

        elif node.n_type == 'AccessVariable':
            # TODO(us): hacer
            pass

        elif node.n_type == 'AccessVarList':
            # TODO(us): hacer
            pass

        elif node.n_type == 'MathExpression':
            self.process_math_expression(node)

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
            self.process_print(node)

        elif node.n_type == 'EmptyPrint':
            # TODO(us): hacer
            pass


        elif node.n_type == 'PrintDataStructs':
            self.code += "std::cout << std::endl;"

        elif node.n_type == 'VariableAssignment':
            self.process_variable_assignment(node)

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
