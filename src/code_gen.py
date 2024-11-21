import os
from node import Node

class CodeGenerator:
    def __init__(self, ast):
        self.root = ast[0]
        self.variables = ""
        self.code = ""

        self. in_class = False
        self.classes = "" # store all classes
        self.class_single = ""  # store a class
        self.class_attributes = "" # store atributes for a class

        self.in_function = False
        self.func_variables = ""
        self.func_code = ""
        self.functions = ""

        self.globals = ""

        self.global_vector = []
        self.main_existing_variables = {}
        self.func_existing_variables = {}
        self.class_existing_attributes = {}
        self.main_existing_iterators = {}
        self.func_existing_iterators = {}
        self.class_existing_attributes_iterators = {}
    
    def generate_code(self):
        # Get code ready
        self.generate_code_recv(self.root)
        self.code = self.variables + self.code

        # function for all normal code
        self.code = "int python_root() {\n" + self.code

        # Always define true and false
        self.globals += "Entity bool_true(INT, \"1\");\n"
        self.globals += "Entity bool_false(INT, \"0\");\n"
        self.globals += "Entity none(NONE, \"NULL\");\n"

        # Append necessary includes
        self.code = "#include \"functions.hpp\"\n" + self.code
        self.code = "#include \"classes.hpp\"\n" + self.code
        self.code = "#include \"entity.hpp\"\n" + self.code
        self.code = "#include <string>\n" + self.code
        self.code = "#include <iostream>\n" + self.code
        self.code = "#include <stdexcept>\n" + self.code
        self.code += "return 0;\n}\n"
        self.code += "int main() {\npython_root();\n}"
        self.globals = "#include \"entity.hpp\"\n\n" + self.globals
        self.functions = "#include \"globals.hpp\"\n\n" + self.functions
        
        self.classes = "#include \"entity.hpp\"\n\n" + self.classes
        self.classes = "#include \"globals.hpp\"\n" + self.classes
        self.classes = "#include <string>\n" + self.classes
        self.classes = "#include <iostream>\n" + self.classes
        self.classes = "#include <stdexcept>\n" + self.classes


        self.code = self.indent_code(self.code)
        self.functions = self.indent_code(self.functions)
        self.classes = self.indent_code(self.classes)

        self.write_file("../output/main.cpp", self.code)
        self.write_file("../output/functions.hpp", self.functions)
        self.write_file("../output/globals.hpp", self.globals)
        self.write_file("../output/classes.hpp", self.classes)


    def write_file(self, path, content):
        # Write to file (make sure directory exists)
        output_dir = os.path.dirname(path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def generate_code_recv(self, node):
        if node.n_type in ['IfRule', 'ElifRule', 'ElseRule', 'DefFunction', 'WhileLoop', 'ForLoop', 'TryRule', 'ExceptRule', 'ClassDefinition']:
            self.process_node(node)
        else:
            self.process_node(node)
            if node.children:
                for child in node.children:
                    self.generate_code_recv(child)

    def append_text(self, t_type, to_append, begin = False):
        # c => code
        # v => variable
        # g => global
        # ca => class attribute
        # cs => single class

        if not begin:
            if t_type == "c":
                if not self.in_function:
                    self.code += to_append
                else:
                    self.func_code += to_append
            elif t_type == "v":
                if not self.in_function:
                    self.variables += to_append
                else:
                    self.func_variables += to_append
            elif t_type == "g":
                self.globals += to_append
            elif t_type == "ca":
                self.class_attributes += to_append
            elif t_type == "cs":
                self.class_single += to_append
        else:
            if t_type == "c":
                if not self.in_function:
                    self.code = to_append + self.code
                else:
                    self.func_code = to_append + self.func_code
            elif t_type == "v":
                if not self.in_function:
                    self.variables = to_append + self.variables
                else:
                    self.func_variables = to_append + self.func_variables
            elif t_type == "g":
                self.globals = to_append + self.globals
            elif t_type == "ca":
                self.class_attributes = to_append + self.class_attributes
            elif t_type == "cs":
                self.class_single = to_append + self.class_single

    def handle_literal(self, value, var_type):
        vector = self.global_vector
        if value in vector:
            index = vector.index(value)
        else:
            index = len(vector)
            vector.append(value)
            if var_type == "string" and len(value) > 1:  # Remove " and ' to avoid problems
                stripped_value = value[1:-1]
            else:
                stripped_value = value

            self.append_text("g", f"Entity {var_type}_{index}({var_type.upper()}, \"{stripped_value}\", true);\n")
        return f"{var_type}_{index}"
    
    def process_variable_assignment(self, node):
        variable_name = node.children[0].value
        cpp_variable_name = f"py_{variable_name}"

        operator = node.children[1].value # operator
        right_node = node.children[2]  # asignee

        value = self.get_cpp_value(right_node)

        if not self.in_function:
            existing_variables = self.main_existing_variables
        else:
            existing_variables = self.func_existing_variables

        if cpp_variable_name not in existing_variables:
            # Define the variable for the first time
            # define variable at the beginning of document
            self.append_text("v", f"Entity {cpp_variable_name} = Entity(INT, \"0\");\n")
            # use in the variable
            self.append_text("c", f"{cpp_variable_name} {operator} {value};\n")
            existing_variables[cpp_variable_name] = True
        else:
            # Update the variable if it already exists
            self.append_text("c", f"{cpp_variable_name} {operator} {value};\n")
            self.append_text("c", f"{cpp_variable_name}.set_active(true);\n")

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
        self.append_text("c", code_to_add)

    # TODO(us): extract active and set it back at the end of the conditions, loops and try catches
    def process_if(self, node):
        condition = self.get_cpp_value(node.children[0])
        self.append_text("c", f"if (({condition}).is_true()) {{\n")
        ended = False # avoid extra curly brackets
        for child in node.children[1:]:
            if (child.n_type == "ElifRule" or child.n_type == "ElseRule") and not ended:
                self.append_text("c", "}\n")
                ended = True
            self.generate_code_recv(child)
        if not ended:
            self.append_text("c", "}\n")

    def process_elif(self, node):
        # the else has to be apart from the if in case we need
        # to define a variable for the condition
        condition = self.get_cpp_value(node.children[0])
        self.append_text("c", f"else if (({condition}).is_true())")
        self.append_text("c", "{\n")
        ended = False
        for child in node.children[1:]:
            if (child.n_type == "ElifRule" or child.n_type == "Else") and not ended:
                self.append_text("c", "}\n")
            self.generate_code_recv(child)
        if not ended:
            self.append_text("c","}\n")

    def process_else(self, node):
        self.append_text("c", "else {\n")
        for child in node.children:
            self.generate_code_recv(child)
        self.append_text("c", "}\n")
    
    def process_except(self, node):
        exception_type = "std::exception"
        exception_var = "e"  

        if node.children and node.children[0].n_type == 'VarName':
            exception_var = node.children[0].value

        self.append_text("c", f"catch ({exception_type}& {exception_var}) {{\n")

        for child in node.children[1:]:  
            self.generate_code_recv(child)
        self.append_text("c", "}\n")  

    def process_try(self, node):
        self.append_text("c", "try {\n")
        for child in node.children:
            if child.n_type == 'ExceptRule':
                self.append_text("c", "}\n")  
                self.process_except(child)
            else:
                self.generate_code_recv(child)
        if not any(child.n_type == 'ExceptRule' for child in node.children):
            self.append_text("c", "}\n") # TODO(us): revisar si quitamos try sin catch

    def process_while_loop(self, node):
        condition = self.get_cpp_value(node.children[0])
        self.append_text("c", f"while (({condition}).is_true()) {{\n")
        for child in node.children[1:]:
            self.generate_code_recv(child)
        self.append_text("c", "}\n")

    def process_for_loop(self, node):
        iterator_index = 0
        iterable_index = 1
        loop_body_index = -1

        iterator = node.children[iterator_index].value
        cpp_iterator = f"py_{iterator}"

        if cpp_iterator not in self.func_existing_variables:
            self.func_existing_variables[cpp_iterator] = True
            self.append_text("v", f"Entity {cpp_iterator};\n")

        iterable_node = node.children[iterable_index]
        iterable = self.get_cpp_value(iterable_node)

        # TODO(us): check if this works in c++ for our iterator 
        self.append_text("c", f"for (auto& {cpp_iterator} : {iterable}.iter()) {{\n")
        
        loop_body = node.children[loop_body_index]
        self.generate_code_recv(loop_body)
        self.append_text("c", "}\n")

    def find_parameters(self, node):
        # TODO(us): pensar si hay referencias
        parameters = ""
        if node.children[0].n_type == "Parameter":
            parameters = f"Entity py_{node.children[0].value}"
            self.func_existing_variables[f"py_{node.children[0].value}"] = True
        elif node.children[0].n_type == "ParameterList":
            # if we have several parameters with no asigned values
            if node.children[0].children[0].n_type == "ParameterList":
                for child in node.children[0].children[0].children:
                    parameters += f"Entity py_{child.value}, "
                    self.func_existing_variables[f"py_{child.value}"] = True

            # now check if there are any other params, search for children with default value
            for child in node.children[0].children:
                if child.n_type == "Parameter":
                    parameters += f"Entity py_{child.value}, "
                    self.func_existing_variables[f"py_{child.value}"] = True
                elif child.n_type == "ParameterWithDefault":
                    value = self.get_cpp_value(child.children[0])
                    parameters += f"Entity py_{child.value} = {value}, "
                    self.func_existing_variables[f"py_{child.value}"] = True

        return parameters[:-2]

    # TODO(us): handle __init__ in classes
    # TODO(us): handle __main__ 
    def handle_def_function(self, node):
        self.in_function = True
        self.func_code = ""
        self.func_variables = ""
        self.func_existing_variables = {}

        func_name = f"py_{node.value}"
        parameters = self.find_parameters(node)
        
        self.generate_code_recv(node.children[-1])
        self.append_text("c", self.func_variables, True)
        self.append_text("c", f"Entity {func_name}({parameters}){{\n", True)
        self.append_text("c", "return none;\n}\n")
        if not self.in_class:
            self.functions += self.func_code
        else:
            self.class_single += self.func_code
        self.in_function = False

    def handle_return(self, node):
        if len(node.children) == 0:
            self.append_text("c", "return none;\n")
        else:
            value = self.get_cpp_value(node.children[0])
            self.append_text("c", f"return {value};\n")

    # TODO(us): revisar lo de si está true no (para poder agregarle a tupla)
    def handle_data_structure(self, elements, var_type):
        vector = self.global_vector

        if var_type == "list" or var_type == "tuple":
            serialized_value = [self.get_cpp_value(el) for el in elements]
        elif var_type == "set":
            serialized_value = {self.get_cpp_value(el) for el in elements}
        elif var_type == "dict":
            serialized_value = {self.get_cpp_value(k): self.get_cpp_value(v) for k, v in elements.items()}
        else:
            raise ValueError(f"Unsupported data structure type: {var_type}")

        if serialized_value in vector:
            index = vector.index(serialized_value)
        else:
            index = len(vector)
            vector.append(serialized_value)

            self.append_text("g", f"Entity {var_type}_{index}({var_type.upper()}, \"\");\n")
            if var_type in ["list", "tuple", "set"]:
                for el in elements:
                    cpp_element = self.get_cpp_value(el)
                    self.append_text("c", f"{var_type}_{index}.append({cpp_element});\n")
            elif var_type == "dict":
                for key, value in elements.items():
                    cpp_key = self.get_cpp_value(key)
                    cpp_value = self.get_cpp_value(value)
                    self.append_text("c", f"{var_type}_{index}[{cpp_key}] = {cpp_value};\n")

        return f"{var_type}_{index}"

    # TODO(us): Cada vez que vemos un self. eso tiene que ser un atributo
    def handle_class_definition(self, node):
        self.in_class = True
        self.class_attributes = ""
        self.class_single = ""
        self.class_existing_attributes = {}

        class_name = f"py_{node.value}"
        if node.children[0].n_type == "Inheritance":
            inheritance = f"py_{node.children[0].value}"
        else:
            inheritance = None
        
        # generate children
        self.generate_code_recv(node.children[-1])

        # TODO(us): append attributes
        # TODO(us): ifndef?
        if inheritance is not None:
            self.append_text("cs", f"class {class_name} : public {inheritance}{{\npublic: \n", True)
        else: 
            self.append_text("cs", f"class {class_name}{{\npublic:\n", True)

        self.append_text("cs", "};\n")
        self.classes += self.class_single
        self.in_class = False

    def process_function_call(self, node):
        function_name = node.value
        parameters = []
        if len(node.children) > 0:
            for param in node.children[0].children:
                if param.n_type == "ParameterWithAssignment":
                    # In c++ there is no parameter asignation in c++
                    # param_name = param.value
                    param_value = self.get_cpp_value(param.children[0])
                    parameters.append(f"{param_value}")
                else:
                    parameters.append(self.get_cpp_value(param))

        if function_name == "type":
            if len(parameters) != 1:
                raise ValueError("type() expects exactly one argument.")
            return f"{parameters[0]}.type()"
        elif function_name == "sum":
            if len(parameters) == 1:
                return f"{parameters[0]}.sum()"
            elif len(parameters) == 2:
                return f"{parameters[0]}.sum({parameters[1]})"
            else:
                raise ValueError("sum() expects at most two arguments: iterable and optional start value.")
        elif function_name == "range":
            if len(parameters) == 1:
                return f"{parameters[0]}.range()"
            elif len(parameters) == 2:
                return f"{parameters[0]}.range({parameters[1]})"
            elif len(parameters) == 3:
                return f"{parameters[0]}.range({parameters[1]}, {parameters[2]})"
            else:
                raise ValueError("range() expects 1 to 3 arguments.")
        elif function_name == "iter": # TODO(us): define the variable iterator as a Iterator Instance
            if len(parameters) != 1:
                raise ValueError("iter() expects exactly one argument.")
            return f"{parameters[0]}.iter()"
        elif function_name == "next":
            if len(parameters) != 1:
                raise ValueError("next() expects exactly one argument.")
            return f"{parameters[0]}.next()"
        elif function_name in ["int", "float", "str", "bool"]:
            if len(parameters) != 1:
                raise ValueError(f"{function_name}() expects exactly one argument.")
            target_type = {
                "int": "INT",
                "float": "DOUBLE",
                "str": "STRING",
                "bool": "BOOL"
            }[function_name]
            return f"{parameters[0]}.cast({target_type})"
        else:
            cpp_function_name = f"py_{function_name}"
            param_list = ", ".join(parameters)
            return f"{cpp_function_name}({param_list})"



    def get_cpp_value(self, value_node):
        if value_node.n_type == 'IntegerLiteral':
            return self.handle_literal(value_node.value, 'int')
        elif value_node.n_type == 'FloatLiteral':
            return self.handle_literal(value_node.value, 'double')
        elif value_node.n_type == 'StringLiteral':
            return self.handle_literal(value_node.value, 'string')
        elif value_node.n_type == 'VarName':
            return f"py_{value_node.value}"
        elif value_node.n_type == 'MathExpression':
            return self.process_math_expression(value_node)
        elif value_node.n_type == 'Parenthesis': 
            return self.get_cpp_value(value_node.children[0])
        elif value_node.n_type == 'BooleanLiteral':
            return "bool_true" if value_node.value == True else "bool_false"
        elif value_node.n_type == 'NoneLiteral':
            return "none" 
        elif value_node.n_type == 'List':
            list_elements = value_node.children
            return self.handle_data_structure(list_elements, 'list')
        elif value_node.n_type == 'Tuple':
            tuple_elements = value_node.children
            return self.handle_data_structure(tuple_elements, 'tuple')
        elif value_node.n_type == 'Set':
            set_elements = value_node.children
            return self.handle_data_structure(set_elements, 'set')
        elif value_node.n_type == 'Dictionary':
            dict_elements = {}
            for i in range(0, len(value_node.children), 2):
                key = value_node.children[i]
                value = value_node.children[i + 1]
                dict_elements[key] = value
            return self.handle_data_structure(dict_elements, 'dict')

        elif value_node.n_type == 'EmptyList':
            return self.handle_data_structure([], 'list')
        elif value_node.n_type == 'EmptyDictionary':
            return self.handle_data_structure({}, 'dict')
        elif value_node.n_type == 'CallFunction':
            return self.process_function_call(value_node)
        else:
            raise ValueError(f"Unsupported value node type: {value_node.n_type}")
    

    def process_node(self, node):
        if node.n_type == 'Start':
            pass # Just used as a start point

        elif node.n_type == 'Empty':
            pass # it is already empty

        elif node.n_type == 'EmptyStatement':
            pass # just pass the statement

        elif node.n_type == 'Statement':
            pass # just pass the statement

        elif node.n_type == 'VarName':
            # TODO(us): hacer
            pass

        elif node.n_type == 'WhileLoop':
            self.process_while_loop(node)

        elif node.n_type == 'ForLoop':
            self.process_for_loop(node)

        elif node.n_type == 'TryRule':
            self.process_try(node)

        elif node.n_type == 'ExceptRule':
            pass # handled in try rule

        elif node.n_type == 'IfRule':
            self.process_if(node)

        elif node.n_type == 'ElifRule':
            self.process_elif(node)

        elif node.n_type == 'ElseRule':
            self.process_else(node)

        elif node.n_type == 'NoneLiteral':
            pass # global value

        elif node.n_type == 'IntegerLiteral':
            if not self.in_function:
                self.handle_literal(node.value, 'int')
            else:
                self.handle_literal(node.value, 'int')

        elif node.n_type == 'FloatLiteral':
            if not self.in_function:
                self.handle_literal(node.value, 'double')
            else:
                self.handle_literal(node.value, 'double')

        elif node.n_type == 'StringLiteral':
            if not self.in_function:
                self.handle_literal(node.value, 'string')
            else:
                self.handle_literal(node.value, 'string')

        elif node.n_type == 'DefFunction':
            self.handle_def_function(node)

        elif node.n_type == 'Parameter':
            pass # handled in function

        elif node.n_type == 'ParameterList':
            pass # handled in function

        elif node.n_type == 'ParameterWithDefault':
            pass # handled in function

        elif node.n_type == 'ReturnStatement':
            self.handle_return(node)

        elif node.n_type == 'CallFunction':
            cpp_code = self.process_function_call(node)
            self.append_text("c", cpp_code + ";\n")

        elif node.n_type == 'ParameterWithAssignment':
            pass # handled in call function

        elif node.n_type == 'BooleanLiteral':
            pass # Global values

        elif node.n_type == 'AccessVariable':
            # TODO(us): hacer
            # Self -> needs to be function attribute
            pass

        elif node.n_type == 'AccessVarList':
            # TODO(us): hacer
            # Self -> needs to be function attribute
            pass

        elif node.n_type == 'MathExpression':
            self.process_math_expression(node)

        elif node.n_type == 'MathSymbol':
            pass # handled by math expression

        elif node.n_type == 'Parenthesis':
            pass # handled by math expression

        elif node.n_type == 'MathAssign':
            pass # handled by math expression

        elif node.n_type == 'LogicSymbols':
            pass # handled by math expression

        elif node.n_type == 'CmpSymbols':
            pass # handled by math expression

        if node.n_type == 'List':
            list_elements = node.children
            self.handle_data_structure(list_elements, "list")

        elif node.n_type == 'Tuple':
            tuple_elements = node.children
            self.handle_data_structure(tuple_elements, "tuple")

        elif node.n_type == 'Set':
            set_elements = node.children
            self.handle_data_structure(set_elements, "set")

        elif node.n_type == 'Dictionary':
            dict_elements = {}
            for i in range(0, len(node.children), 2):
                key = node.children[i]
                value = node.children[i + 1]
                dict_elements[key] = value
            self.handle_data_structure(dict_elements, "dict")

        elif node.n_type in ['EmptyList', 'EmptyDictionary']:
            empty_type = 'list' if node.n_type == 'EmptyList' else 'dict'
            self.handle_data_structure([], empty_type)

        elif node.n_type == 'Print':
            self.process_print(node)

        elif node.n_type == 'EmptyPrint':
            self.append_text("c", "std::cout << std::endl;")

        elif node.n_type == 'PrintDataStructs':
            self.process_print(node) # TODO(us): revisar

        elif node.n_type == 'VariableAssignment':
            self.process_variable_assignment(node)

        elif node.n_type == 'AttributeMethod':
            # TODO(us): hacer
            pass

        elif node.n_type == 'ClassDefinition':
            self.handle_class_definition(node)
            pass

        elif node.n_type == 'Inheritance':
            pass # handled by class

        elif node.n_type == 'Continue':
            self.append_text("c", "continue; \n")
            pass

        elif node.n_type == 'Break':
            self.append_text("c", "break; \n")
            pass
    
    # TODO(us): propperly indent classes
    def indent_code(self, code):
        indent_count = 0
        new_code = ""
        
        for line in code.splitlines():
            stripped_line = line.strip()
            
            if stripped_line.endswith("}"):
                indent_count -= 1
            
            new_code += "\n" + "\t" * indent_count + line
            
            if stripped_line.endswith("{"):
                indent_count += 1

        return new_code.lstrip("\n")
