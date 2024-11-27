import ply.yacc as yacc
from lexer import Lexer
from node import Node

error_count = 0
debug_parser = False
ast = None

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'FLOOR_DIV', 'DIV',  'MODULO'),
    ('left', 'POWER'),
    ('left', 'PLUS_EQUALS', 'MINUS_EQUALS', 'MODULO_EQUALS', 'MUL_EQUALS', 'DIV_EQUALS'),
    ('left', 'FLOOR_DIV_EQUALS', 'POWER_EQUALS'),
    ('left', 'OPEN_PARENTHESIS', 'CLOSED_PARENTHESIS'),
    ('left', 'OPEN_BRACKET', 'CLOSED_BRACKET'),
    ('left', 'OPEN_CURLY_BRACKET', 'CLOSED_CURLY_BRACKET')
)

def level_statement(p):
    while len(p[0].children) == 1 and p[0].children[0].n_type == "Statement":
            p[0] = p[0].children[0]
    return p

def statement_creation(p):
    if len(p) == 2:
        if p[1] is not None:
            p[0] = Node(n_type='Statement', children= [p[1]])
        else:
            p[0] = Node(n_type='EmptyStatement')
    else:
        children = [c for c in [p[1], p[2]] if c is not None]
        if children[0].n_type == 'Statement' and len(children) == 2:
            children[0].children.append(children[1])
            p[0] = children[0]
        elif len(children) == 1:
            p[0] = children[0]

    p = level_statement(p)

    return p

def for_loop_statement(p):
    iterator = p[2]
    iterable = p[4]
    loop_body = p[8]
    if len(p) != 10: 
        iterator = p[3]
        iterable = p[5]
        loop_body = p[10]
    iterator =  Node(n_type="VarName", value=iterator)
    p[0] = Node("ForLoop", children=[iterator, iterable, loop_body])
    return p

def while_loop_statement(p):
    p[0] = Node("WhileLoop", children=[p[2], p[6]])
    return p

def try_statement(p): 
    try_block = p[5]  
    except_block = None
    if len(p) == 8:
        except_block = p[7]
    children = [c for c in [try_block, except_block] if c is not None]
    p[0] = Node("TryRule", children=children)
    return p

def catch_statement(p):
    exception_type = None
    except_block = p[5]
    if len(p) == 8:
        exception_type = p[2]
        except_block = p[6]
    p[0] = Node("ExceptRule", children=[except_block], value = exception_type)
    return p

def level_if_statement(p):
    if len(p.children) == 3:
        tempP = p.children[2]
        while len(tempP.children) == 3 and (tempP.children[2].n_type == "ElifRule" or tempP.children[2].n_type == "ElseRule"):
            tempChild = tempP.children[2]
            p.children.append(tempChild)
            tempP.children.remove(tempP.children[2])
            tempP = p.children[len(p.children)-1]
    return p

def if_statement_creation(p):
    if_node = Node(n_type="IfRule", children=[p[2], p[6]])
    if len(p) > 8:
        additional_clauses = p[8:]
        for clause in additional_clauses:
            if isinstance(clause, Node):
                if_node.children.append(clause)
    p[0] = if_node
    p[0] = level_if_statement(p[0])
    return p

def elif_statement_creation(p):
    elif_node = Node(n_type="ElifRule", children=[p[2], p[6]])
    if len(p) > 8:
        next_clause = p[8]
        if isinstance(next_clause, Node):
            elif_node.children.append(next_clause)
    
    p[0] = elif_node
    return p

def else_statement_creation(p):
    p[0] = Node(n_type="ElseRule", children=[p[5]])
    return p

def p_start(p):
    '''start : START_MARKER statement END_MARKER
            | START_MARKER statement statement_values_end END_MARKER
            | START_MARKER END_MARKER'''
    if len(p) == 4:
        if p[2] is not None:
            p[0] = Node(n_type= 'Start', children = [p[2]])
        else:
            p[0] = Node(n_type="Empty")
    elif len(p) == 5: 
        children = [p[2]]
        if p[3] is not None:
            children.append(p[3])
        p[0] = Node(n_type='Start', children=children)
    else:  # Empty
        p[0] = Node(n_type='Empty')

    if debug_parser:
        print("AST tree:")
        print(p[0])
        p[0].visualize()
    global ast
    ast = p
    
def p_statement(p):
    '''statement : statement_values
                 | statement statement_values'''
    p = statement_creation(p)

def p_statement_values(p):
    '''statement_values : def_function
                        | if_rule
                        | def_class
                        | STRING NEWLINE
                        | NONE NEWLINE
                        | variable_assign NEWLINE
                        | variable NEWLINE
                        | math_expression NEWLINE
                        | tuple NEWLINE
                        | list NEWLINE
                        | set NEWLINE
                        | dictionary NEWLINE
                        | call_function NEWLINE
                        | PASS NEWLINE
                        | printing NEWLINE
                        | while_rule
                        | for_rule
                        | try_rule
                        | NEWLINE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != '\n' and p[1] != 'pass':  # Ignore newlines and pass
        p[0] = p[1]
    else:
        p[0] = None

def p_statement_values_end(p):
    '''statement_values_end : STRING
                        | NONE
                        | variable_assign
                        | variable
                        | math_expression
                        | tuple
                        | list
                        | set
                        | dictionary
                        | call_function
                        | PASS
                        | printing'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != 'pass':  # Ignore pass
        p[0] = p[1]
    else:
        p[0] = None

def p_def_function(p):
    '''def_function : DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT
                    | DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter_assign CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT
                    | DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter COMMA def_parameter_assign CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT
                    | DEF VAR_FUNC_NAME OPEN_PARENTHESIS CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT'''
    if len(p) == 11: # Rule 1 and 2
        p[0] = Node(n_type= 'DefFunction', children=[p[4], p[9]], value=p[2])

    elif len(p) == 13: # Rule 3
        p[6].children = [p[4]] + p[6].children
        p[0] = Node(n_type= 'DefFunction', children=[p[6], p[11]], value=p[2])

    elif len(p) == 10: # Rule 4
        p[0] = Node(n_type='DefFunction', children = [p[8]], value=p[2])

def p_def_parameter(p):
    '''def_parameter : VAR_FUNC_NAME
                     | def_parameter COMMA VAR_FUNC_NAME'''
    if len(p) == 2:
        p[0] = Node(n_type="Parameter", value=p[1])
    else:
        if isinstance(p[1], Node):
            children = [c for c in ([Node(n_type="Parameter", value=p[1].value)] + p[1].children + [Node(n_type="Parameter", value=p[3])]) if c.value is not None]
            p[0] = Node(n_type="ParameterList", children=children)
        else:
            p[0] = Node(n_type="ParameterList", children=[p[1], Node(n_type="Parameter", value=p[3])])

def p_def_parameter_assign(p):
    '''def_parameter_assign : def_parameter_assign COMMA VAR_FUNC_NAME ASSIGN values
                            | VAR_FUNC_NAME ASSIGN values'''
    if len(p) == 4:
        # Single parameter with a default value
        param_node = Node(n_type="ParameterWithDefault", children=[p[3]], value=p[1])
        p[0] = Node(n_type="ParameterList", children=[param_node])
    else:
        # Multiple parameters with default values
        param_node = Node(n_type="ParameterWithDefault", children=[p[5]], value=p[3])
        p[0] = Node(n_type="ParameterList", children=p[1].children + [param_node])


def p_func_statement(p):
    '''func_statement : func_statement_values_end
                      | func_statement_recv
                      | func_statement_recv func_statement_values_end'''
    p = statement_creation(p)

def p_func_statement_recv(p):
    '''func_statement_recv : func_statement_values
                           | func_statement_recv func_statement_values'''
    p = statement_creation(p)

def p_func_statement_values(p):
    '''func_statement_values : if_rule_func
                               | STRING NEWLINE
                               | NONE NEWLINE
                               | variable_assign NEWLINE
                               | variable NEWLINE
                               | tuple NEWLINE
                               | list NEWLINE
                               | set NEWLINE
                               | dictionary NEWLINE
                               | PASS NEWLINE
                               | math_expression NEWLINE
                               | call_function NEWLINE
                               | printing NEWLINE
                               | while_rule_func 
                               | for_rule_func 
                               | return_statement NEWLINE
                               | try_rule_func 
                               | NEWLINE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != '\n' and p[1] != 'pass':  # Ignore newlines and pass
        p[0] = p[1]
    else:
        p[0] = None

def p_func_statement_values_end(p):
    '''func_statement_values_end : STRING 
                               | NONE 
                               | variable_assign 
                               | variable 
                               | tuple 
                               | list 
                               | set 
                               | dictionary 
                               | PASS 
                               | math_expression 
                               | call_function 
                               | printing  
                               | return_statement '''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != 'pass':  # Ignore pass
        p[0] = p[1]
    else:
        p[0] = None

def p_return_statement(p):
    '''return_statement : RETURN
                        | RETURN call_function
                        | RETURN variable
                        | RETURN values
                        | RETURN list
                        | RETURN dictionary
                        | RETURN set
                        | RETURN tuple'''
    if len(p) == 2:
        p[0] = Node(n_type="ReturnStatement")
    else:
        p[0] = Node(n_type="ReturnStatement", children=[p[2]])

def p_call_function(p):
    '''call_function : VAR_FUNC_NAME OPEN_PARENTHESIS call_parameter CLOSED_PARENTHESIS
                     | VAR_FUNC_NAME OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
    if len(p) == 5: 
        p[0] = Node(n_type="CallFunction", value=p[1], children=[p[3]])
    else:
        p[0] = Node(n_type="CallFunction", value=p[1])

def p_call_parameter(p):
    '''call_parameter : call_function_parameter'''
    p[0] = p[1]

def p_call_function_parameter(p):
    '''call_function_parameter : call_function_parameter COMMA VAR_FUNC_NAME ASSIGN values
                                | call_function_parameter COMMA VAR_FUNC_NAME ASSIGN call_function
                                | call_function_parameter COMMA VAR_FUNC_NAME ASSIGN variable
                                | call_function_parameter COMMA values
                                | call_function_parameter COMMA variable
                                | call_function_parameter COMMA call_function
                                | VAR_FUNC_NAME ASSIGN call_function
                                | VAR_FUNC_NAME ASSIGN values
                                | VAR_FUNC_NAME ASSIGN variable
                                | call_function
                                | variable
                                | values'''
    if len(p) == 2:
        # Single parameter
        p[0] = Node(n_type="ParameterList", children=[p[1]])
    elif len(p) == 4 and p[2] == '=':
        # Parameter with assignment
        param_node = Node(n_type="ParameterWithAssignment", value=p[1], children=[p[3]])
        p[0] = Node(n_type="ParameterList", children=[param_node])
    else:
        # Multiple parameters 
        if isinstance(p[1], Node) and p[1].n_type == "ParameterList":
            new_param = Node(n_type="ParameterWithAssignment", value=p[3], children=[p[5]]) if len(p) == 6 else p[3]
            p[1].children.append(new_param)
            p[0] = p[1]
        else:
            # Create a ParameterList with two children
            p[0] = Node(n_type="ParameterList", children=[p[1], p[3]])

def p_values(p):
    '''values : math_expression
                | STRING
                | NONE'''
    if isinstance(p[1], Node):
        p[0] = p[1]
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    else: # None
        p[0] = Node(n_type="NoneLiteral", value=p[1])
        

def p_math_values(p):
    '''math_values : INT
                    | FLOAT
                    | bool_values '''
    if isinstance(p[1], int):
        p[0] = Node(n_type="IntegerLiteral", value=p[1])
    elif isinstance(p[1], float):
        p[0] = Node(n_type="FloatLiteral", value=p[1])
    else: # Bool values
        p[0] = p[1]

def p_bool_values(p):
    '''bool_values : TRUE
                    | FALSE'''
    p[0] = Node(n_type="BooleanLiteral", value= (p[1] == 'True'))

def p_access_content(p):
    '''access_content : values
                      | variable
                      | tuple'''
    p[0] = p[1]

def p_variable_assign(p):
    '''variable_assign : variable_assign_var
                       | variable_assign_expr'''
    p[0] = p[1]

def p_variable_assign_expr(p):
    '''variable_assign_expr : variable math_assign math_expression
                            | variable math_assign STRING
                            | variable_assign_var math_assign math_expression
                            | variable_assign_var math_assign STRING
                            | variable math_assign call_function
                            | variable_assign_var math_assign call_function
                            | variable math_assign data_structures
                            | variable_assign_var math_assign data_structures'''
    
    if isinstance(p[3], str) and (p[3][0] == "\'" or p[3][0] == "\""):
        p[3] = Node(n_type="StringLiteral", value=p[3])
    
    if p[1].n_type == "VariableAssignment":
        p[1].children.append(p[2])
        p[1].children.append(p[3])
        p[0] = p[1]
    else:
        p[0] = Node(n_type="VariableAssignment", children=[p[1], p[2], p[3]], value =  p[2].value) 

def p_data_structures(p):
    '''data_structures : list
                        | set
                        | tuple
                        | dictionary'''
    p[0] = p[1]

def p_variable_assign_var(p):
    '''variable_assign_var : variable math_assign variable
                           | variable_assign_var math_assign variable'''
    
    if isinstance(p[1], Node) and p[1].n_type == "VariableAssignment":
        p[1].children.append(Node(n_type="VariableAssignment", value=p[2].value))
        p[1].children.append(p[3])
        p[0] = p[1]
    else:
        p[0] = Node(n_type="VariableAssignment", children=[p[1], p[2], p[3]])

def p_period_operator(p):
    '''period_operator : PERIOD VAR_FUNC_NAME
                       | PERIOD call_function'''
    if isinstance(p[2], Node):
        p[0] = p[2]
    else: # VAR_FUNC_NAME
        p[0] = Node(n_type="VarName", value=p[2])

def p_variable(p):
    '''variable : VAR_FUNC_NAME
                | variable period_operator
                | variable OPEN_BRACKET access_content CLOSED_BRACKET 
                | variable OPEN_BRACKET access_content COLON access_content CLOSED_BRACKET
                | variable OPEN_BRACKET COLON access_content CLOSED_BRACKET
                | variable OPEN_BRACKET access_content COLON CLOSED_BRACKET
                | STRING OPEN_BRACKET access_content CLOSED_BRACKET 
                | STRING OPEN_BRACKET access_content COLON access_content CLOSED_BRACKET
                | STRING OPEN_BRACKET COLON access_content CLOSED_BRACKET
                | STRING OPEN_BRACKET access_content COLON CLOSED_BRACKET'''
    if len(p) > 3:
        if isinstance(p[1], str) and (p[1][0] == "\"" or p[1][0] == "\'"):
            p[1] =  Node(n_type = "StringLiteral", value = p[1])
    
    if len(p) == 2:
        p[0] = Node(n_type="VarName", value=p[1])
    elif len(p) == 3:
        p[0] = Node(n_type="AttributeMethod", children=[p[1], p[2]])
    elif len(p) == 5:
        p[0] = Node(n_type="AccessVariable", children=[p[1], p[3]])
    elif len(p) == 6:
        if p[3] == ':':
            p[0] = Node(n_type="AfterVarSlice", children=[p[1], p[4]])
        else:
            p[0] = Node(n_type="BeforeVarSlice", children=[p[1], p[3]])
    elif len(p) == 7:
        p[0] = Node(n_type="AccessVarSlice", children=[p[1], p[3], p[5]])
    

def p_math_expression(p):
    '''math_expression : math_expression_1
                       | NOT math_expression_1
                       | PLUS variable
                       | MINUS variable
                       | NOT variable
                       | PLUS call_function
                       | MINUS call_function
                       | NOT call_function'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] == "not":
            p[1] = "!"
        p[1] = Node(n_type="MathSymbol", value=p[1])
        if isinstance(p[2], Node) and p[2].n_type == 'MathExpression':
            p[2].children = [p[1]] + p[2].children
            p[0] = p[2]
        else:
            p[0] = Node(n_type='MathExpression', children=[p[1], p[2]])
            
def p_math_expression_1(p):
    '''math_expression_1 : math_values
                       | MINUS math_expression_1
                       | PLUS math_expression_1
                       | OPEN_PARENTHESIS math_expression_1 CLOSED_PARENTHESIS
                       | OPEN_PARENTHESIS STRING CLOSED_PARENTHESIS
                       | OPEN_PARENTHESIS variable CLOSED_PARENTHESIS
                       | OPEN_PARENTHESIS call_function CLOSED_PARENTHESIS
                       | math_expression_1 math_symbols expr_math_values_recv
                       | variable math_symbols expr_math_values_recv
                       | call_function math_symbols expr_math_values_recv
                       | STRING math_symbols expr_math_values_recv'''
    
    if len(p) == 2:
        # Direct value or variable
        p[0] = Node(n_type="MathExpression", children=[p[1]])
    elif p[1] in ('-', '+'):
        p[1] = Node(n_type="MathSymbol", value=p[1])
        p[2].children = [p[1]]+ p[2].children 
        p[0] = p[2]
    elif p[1] == '(':
        # Wrap the expression in a Parenthesis node
        if isinstance(p[2], str) and (p[2][0] == '\"' or p[2][0] == '\''):
            p[2] = Node(n_type='StringLiteral', value = p[2])
        p[0] = Node(n_type="Parenthesis", children=[p[2]])
    else:
        # Check if String
        if isinstance(p[1], str) and (p[1][0] == '\"' or p[1][0] == '\''):
            p[1] = Node(n_type='StringLiteral', value = p[1])
            
        # Create a MathExpression node
        left_operand = p[1]
        operator_node = p[2]
        right_operand = p[3]

        if isinstance(left_operand, Node) and left_operand.n_type == "MathExpression":
            left_operand.children.append(operator_node)
            left_operand.children.append(right_operand)
            p[0] = left_operand
        else:
            p[0] = Node(n_type="MathExpression", children=[left_operand, operator_node, right_operand])


def p_expr_math_values_recv(p):
    '''expr_math_values_recv : math_values
                            | STRING
                            | variable
                            | call_function
                            | OPEN_PARENTHESIS math_expression CLOSED_PARENTHESIS
                            | OPEN_PARENTHESIS variable CLOSED_PARENTHESIS
                            | OPEN_PARENTHESIS call_function CLOSED_PARENTHESIS
                            | PLUS expr_math_values_recv
                            | MINUS expr_math_values_recv'''
    if len(p) == 2:
        if isinstance(p[1], str) and (p[1][0] == '\"' or p[1][0] == '\''):
            p[1] = Node(n_type='StringLiteral', value = p[1])
        p[0] = p[1]
    elif p[1] in ('-', '+'):
        p[1] = Node(n_type="MathSymbol", value=p[1])
        p[0] = Node(n_type='MathExpression', children= [p[1] , p[2]])
    else:
        if (p[1] == '('):
            p[0] = Node(n_type="Parenthesis", children=[p[2]])
        else:
            p[0] = Node(n_type='MathExpression', children=[p[1], p[2]])
   
def p_math_symbols(p):
    '''math_symbols : PLUS
                    | MINUS
                    | MUL
                    | DIV
                    | FLOOR_DIV
                    | MODULO
                    | POWER
                    | logic_symbols
                    | cmp_symbols'''
    if (isinstance(p[1], Node)):
        p[0] = Node(n_type="MathSymbol", value=p[1].value)
    else:
        p[0] = Node(n_type="MathSymbol", value=p[1])


def p_math_assign(p):
    '''math_assign  : ASSIGN
                    | PLUS_EQUALS
                    | MINUS_EQUALS
                    | MUL_EQUALS
                    | DIV_EQUALS
                    | MODULO_EQUALS
                    | FLOOR_DIV_EQUALS
                    | POWER_EQUALS'''
    
    p[0] = Node(n_type="MathAssign", value=p[1])


def p_logic_symbols(p):
    '''logic_symbols : OR
                    | AND
                    | IN'''
    
    if p[1] == "or":
        p[1] = "||"
    elif p[1] == 'and':
        p[1] = "and"
    # TODO(us): figure in out

    p[0] = Node(n_type="LogicSymbols", value=p[1])

def p_cmp_symbols(p):
    '''cmp_symbols : EQUALS
                    | DIFFERENT
                    | LESS
                    | MORE
                    | LESS_EQUALS
                    | MORE_EQUALS'''
    
    p[0] = Node(n_type="CmpSymbols", value=p[1])

def p_tuple(p):
    '''tuple : OPEN_PARENTHESIS list_tuple_recursion COMMA list_tuple_values CLOSED_PARENTHESIS'''
    p[0] = Node(n_type='Tuple', children= p[2].children + [p[4]])

def p_list(p):
    '''list : OPEN_BRACKET list_tuple_recursion CLOSED_BRACKET
            | OPEN_BRACKET CLOSED_BRACKET'''
    if len(p) == 3:
        p[0] = Node(n_type='EmptyList')
    else:
        p[0] = Node(n_type='List', children=p[2].children)

def p_list_tuple_recursion(p):
    '''list_tuple_recursion : list_tuple_recursion COMMA list_tuple_values
                            | list_tuple_values'''
    if len(p) == 2:
        p[0] = Node(n_type='ListTupleContent', children=[p[1]])
    else:
        p[0] = Node(n_type='ListTupleContent', children = p[1].children + [p[3]])

def p_list_tuple_values(p):
    '''list_tuple_values : tuple
                         | list
                         | set
                         | dictionary
                         | values
                         | variable
                         | call_function'''
    p[0] = p[1]

def p_set(p):
    '''set : OPEN_CURLY_BRACKET set_recursion CLOSED_CURLY_BRACKET'''
    p[0] = Node(n_type ='Set', children = p[2].children)


def p_set_recursion(p):
    '''set_recursion : set_recursion COMMA set_values
                     | set_values'''
    if len(p) == 2:
        p[0] = Node(n_type='SetContent', children=[p[1]])
    else:
        p[0] = Node(n_type='SetContent', children = p[1].children + [p[3]] )


def p_set_values(p):
    '''set_values : tuple
                  | values'''
    p[0] = p[1]

def p_dictionary(p):
    '''dictionary : OPEN_CURLY_BRACKET dictionary_content CLOSED_CURLY_BRACKET
                   | OPEN_CURLY_BRACKET CLOSED_CURLY_BRACKET'''
    if len(p) == 3:
        p[0] = Node(n_type='EmptyDictionary')
    else:
        p[0] = Node(n_type='Dictionary', children=p[2].children)

def p_dictionary_content(p):
    '''dictionary_content : dictionary_content COMMA list_tuple_values COLON list_tuple_values
                          | list_tuple_values COLON list_tuple_values '''
    # Even positions have keys and odd positions have values
    if len(p) == 4:
        p[0] = Node(n_type='DictionaryContent', children=[p[1], p[3]])
    else:
        p[0] = Node(n_type='DictionaryContent', children = p[1].children + [p[3], p[5]] )



def p_printing(p):
    '''printing : PRINT OPEN_PARENTHESIS math_expression CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS STRING CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS call_function CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS variable CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS print_content_recv CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS NONE CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
    if len(p) == 4:
        p[0] = Node(n_type = "EmptyPrint")
    else:
        if p[3] == 'None':
            p[3] = Node(n_type="NoneLiteral", value= p[3])
        elif isinstance(p[3], str) and (p[3][0] == "\'" or p[3][0] == "\""):
            p[3] = Node(n_type="StringLiteral", value=p[3])
        p[0] = Node(n_type="Print", children = [p[3]] )
        
        

def p_print_content_recv(p):
    '''print_content_recv : print_content_recv PLUS data_structures
                          | data_structures '''
    if len(p) == 2:
        p[0] = Node(n_type = "PrintDataStructs", children = [p[1]])
    else:
        p[0] = Node(n_type = "PrintDataStructs", children = p[1].children + [p[3]])

def p_limited_statement(p):
    '''limited_statement : limited_statement_recv
                         | limited_statement_values_end
                         | limited_statement_recv limited_statement_values_end'''
    p = statement_creation(p)
    
def p_limited_statement_recv(p):
    '''limited_statement_recv : limited_statement_values
                              | limited_statement_recv limited_statement_values'''
    p = statement_creation(p)

def p_limited_statement_values(p):
    '''limited_statement_values : if_rule
                                | STRING NEWLINE
                                | NONE NEWLINE
                                | variable NEWLINE
                                | variable_assign NEWLINE
                                | tuple NEWLINE
                                | list NEWLINE
                                | set NEWLINE
                                | dictionary NEWLINE
                                | PASS NEWLINE
                                | math_expression NEWLINE
                                | call_function NEWLINE
                                | printing NEWLINE
                                | while_rule
                                | for_rule
                                | try_rule
                                | NEWLINE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != '\n' and p[1] != 'pass':  # Ignore newlines and pass
        p[0] = p[1]
    else:
        p[0] = None

def p_limited_statement_values_end(p):
    '''limited_statement_values_end : STRING
                                | NONE
                                | variable
                                | variable_assign
                                | tuple
                                | list
                                | set
                                | dictionary
                                | PASS
                                | math_expression
                                | call_function
                                | printing '''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != 'pass':  # Ignore pass
        p[0] = p[1]
    else:
        p[0] = None

def p_if_rule(p):
    '''if_rule : IF math_expression COLON NEWLINE INDENT limited_statement DEDENT
                | IF math_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                | IF math_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule
                | IF variable COLON NEWLINE INDENT limited_statement DEDENT
                | IF variable COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                | IF variable COLON NEWLINE INDENT limited_statement DEDENT else_rule
                | IF call_function COLON NEWLINE INDENT limited_statement DEDENT
                | IF call_function COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                | IF call_function COLON NEWLINE INDENT limited_statement DEDENT else_rule'''
    p = if_statement_creation(p)

def p_elif_rule(p):
    '''elif_rule : ELIF math_expression COLON NEWLINE INDENT limited_statement DEDENT
                    | ELIF math_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                    | ELIF math_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule
                    | ELIF variable COLON NEWLINE INDENT limited_statement DEDENT
                    | ELIF variable COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                    | ELIF variable COLON NEWLINE INDENT limited_statement DEDENT else_rule
                    | ELIF call_function COLON NEWLINE INDENT limited_statement DEDENT
                    | ELIF call_function COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                    | ELIF call_function COLON NEWLINE INDENT limited_statement DEDENT else_rule'''
    p = elif_statement_creation(p)

def p_else_rule(p):
    '''else_rule : ELSE COLON NEWLINE INDENT limited_statement DEDENT'''
    p = else_statement_creation(p)

def p_loop_statement(p):
    '''loop_statement : loop_statement_recv
                      | loop_statement_values_end
                      | loop_statement_recv loop_statement_values_end'''
    p = statement_creation(p)

def p_loop_statement_recv(p):
    '''loop_statement_recv : loop_statement_values
                           | loop_statement_recv loop_statement_values'''
    p = statement_creation(p)

def p_loop_statement_values(p):
    '''loop_statement_values : if_rule_loop
                                | STRING NEWLINE
                                | NONE NEWLINE
                                | variable NEWLINE
                                | variable_assign NEWLINE
                                | tuple NEWLINE
                                | list NEWLINE
                                | set NEWLINE
                                | dictionary NEWLINE
                                | PASS NEWLINE
                                | math_expression NEWLINE
                                | printing NEWLINE
                                | while_rule 
                                | for_rule
                                | try_rule_loop
                                | call_function NEWLINE
                                | CONTINUE NEWLINE
                                | BREAK NEWLINE
                                | NEWLINE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif p[1] == 'continue':
        p[0] = Node(n_type="Continue", value=p[1])
    elif p[1] == 'break':
        p[0] = Node(n_type="Break", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != '\n' and p[1] != 'pass':  # Ignore newlines and pass
        p[0] = p[1]
    else:
        p[0] = None
    

def p_loop_statement_values_end(p):
    '''loop_statement_values_end : STRING
                                | NONE
                                | variable
                                | variable_assign
                                | tuple
                                | list
                                | set
                                | dictionary
                                | PASS
                                | math_expression
                                | printing
                                | call_function
                                | CONTINUE
                                | BREAK '''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif p[1] == 'continue':
        p[0] = Node(n_type="Continue", value=p[1])
    elif p[1] == 'break':
        p[0] = Node(n_type="Break", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != 'pass':  # Ignore pass
        p[0] = p[1]
    else:
        p[0] = None

def p_while_rule(p):
    '''while_rule : WHILE math_expression COLON NEWLINE INDENT loop_statement DEDENT
                    | WHILE variable COLON NEWLINE INDENT loop_statement DEDENT'''
    p = while_loop_statement(p)

def p_for_rule(p):
    '''for_rule : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT loop_statement DEDENT
                | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT loop_statement DEDENT'''
    p = for_loop_statement(p)

def p_for_rule_content(p):
    '''for_rule_content : call_function
                        | variable
                        | list
                        | tuple
                        | dictionary
                        | set'''
    if isinstance(p[1], Node):
        p[0] = p[1]
    else:
        p[0] = Node(n_type="VarName", value=p[1])

def p_try_rule(p):
    '''try_rule : TRY COLON NEWLINE INDENT limited_statement DEDENT except_rule'''
    p = try_statement(p)

def p_except_rule(p):
    '''except_rule : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement DEDENT
                    | EXCEPT COLON NEWLINE INDENT limited_statement DEDENT'''
    p = catch_statement(p)

def p_limited_statement_loop(p):
    '''limited_statement_loop : limited_statement_values_loop_end
                              | limited_statement_loop_recv
                              | limited_statement_loop_recv limited_statement_values_loop_end'''
    p= statement_creation(p)
    
def p_limited_statement_loop_recv(p):
    '''limited_statement_loop_recv : limited_statement_values_loop
                                   | limited_statement_loop_recv limited_statement_values_loop'''
    p = statement_creation(p)

def p_limited_statement_values_loop(p):
    '''limited_statement_values_loop : if_rule_loop
                                        | STRING NEWLINE
                                        | NONE NEWLINE
                                        | variable NEWLINE
                                        | variable_assign NEWLINE
                                        | tuple NEWLINE
                                        | list NEWLINE
                                        | set NEWLINE
                                        | dictionary NEWLINE
                                        | PASS NEWLINE
                                        | math_expression NEWLINE
                                        | call_function NEWLINE
                                        | printing NEWLINE
                                        | while_rule
                                        | for_rule
                                        | try_rule_loop
                                        | BREAK NEWLINE
                                        | CONTINUE NEWLINE
                                        | NEWLINE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif p[1] == 'continue':
        p[0] = Node(n_type="Continue", value=p[1])
    elif p[1] == 'break':
        p[0] = Node(n_type="Break", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != '\n' and p[1] != 'pass':  # Ignore newlines and pass
        p[0] = p[1]
    else:
        p[0] = None

def p_limited_statement_values_loop_end(p):
    '''limited_statement_values_loop_end : STRING
                                        | NONE
                                        | variable
                                        | variable_assign
                                        | tuple
                                        | list
                                        | set
                                        | dictionary
                                        | PASS
                                        | math_expression
                                        | call_function
                                        | printing
                                        | BREAK
                                        | CONTINUE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif p[1] == 'continue':
        p[0] = Node(n_type="Continue", value=p[1])
    elif p[1] == 'break':
        p[0] = Node(n_type="Break", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != 'pass':  # Ignore pass
        p[0] = p[1]
    else:
        p[0] = None

def p_if_rule_loop(p):
    '''if_rule_loop : IF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                    | IF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                    | IF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop
                    | IF variable COLON NEWLINE INDENT limited_statement_loop DEDENT
                    | IF variable COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                    | IF variable COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop
                    | IF call_function COLON NEWLINE INDENT limited_statement_loop DEDENT
                    | IF call_function COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                    | IF call_function COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''
    p = if_statement_creation(p)

def p_elif_rule_loop(p):
    '''elif_rule_loop : ELIF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                      | ELIF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                      | ELIF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop
                      | ELIF variable COLON NEWLINE INDENT limited_statement_loop DEDENT
                      | ELIF variable COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                      | ELIF variable COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop
                      | ELIF call_function COLON NEWLINE INDENT limited_statement_loop DEDENT
                      | ELIF call_function COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                      | ELIF call_function COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''
    p = elif_statement_creation(p)

def p_else_rule_loop(p):
    '''else_rule_loop : ELSE COLON NEWLINE INDENT limited_statement_loop DEDENT'''
    p = else_statement_creation(p)


def p_try_rule_loop(p):
    '''try_rule_loop : TRY COLON NEWLINE INDENT limited_statement_loop DEDENT except_rule_loop'''
    p = try_statement(p)

def p_except_rule_loop(p):
    '''except_rule_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_loop DEDENT
                        | EXCEPT COLON NEWLINE INDENT limited_statement_loop DEDENT'''
    p = catch_statement(p)

def p_limited_statement_func(p):
    '''limited_statement_func : limited_statement_func_recv
                              | limited_statement_values_func_end
                              | limited_statement_func_recv limited_statement_values_func_end'''
    p = statement_creation(p)

def p_limited_statement_func_recv(p):
    '''limited_statement_func_recv : limited_statement_values_func
                                   | limited_statement_func_recv limited_statement_values_func'''
    p = statement_creation(p)

def p_limited_statement_values_func(p):
    '''limited_statement_values_func : if_rule_func
                                        | STRING NEWLINE
                                        | NONE NEWLINE
                                        | variable_assign NEWLINE
                                        | variable NEWLINE
                                        | tuple NEWLINE
                                        | list NEWLINE
                                        | set NEWLINE
                                        | dictionary NEWLINE
                                        | PASS NEWLINE
                                        | math_expression NEWLINE
                                        | printing NEWLINE
                                        | call_function NEWLINE
                                        | while_rule_func
                                        | for_rule_func
                                        | try_rule_func
                                        | return_statement NEWLINE
                                        | NEWLINE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != '\n' and p[1] != 'pass':  # Ignore newlines and pass
        p[0] = p[1]
    else:
        p[0] = None

def p_limited_statement_values_func_end(p):
    '''limited_statement_values_func_end : STRING
                                        | NONE
                                        | variable_assign
                                        | variable
                                        | tuple
                                        | list
                                        | set
                                        | dictionary
                                        | PASS
                                        | math_expression
                                        | printing
                                        | call_function
                                        | return_statement'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != 'pass':  # Ignore pass
        p[0] = p[1]
    else:
        p[0] = None

def p_if_rule_func(p):
    '''if_rule_func : IF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                    | IF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                    | IF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func
                    | IF variable COLON NEWLINE INDENT limited_statement_func DEDENT
                    | IF variable COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                    | IF variable COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func
                    | IF call_function COLON NEWLINE INDENT limited_statement_func DEDENT
                    | IF call_function COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                    | IF call_function COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''
    p = if_statement_creation(p)

def p_elif_rule_func(p):
    '''elif_rule_func : ELIF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                        | ELIF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                        | ELIF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func
                        | ELIF variable COLON NEWLINE INDENT limited_statement_func DEDENT
                        | ELIF variable COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                        | ELIF variable COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func
                        | ELIF call_function COLON NEWLINE INDENT limited_statement_func DEDENT
                        | ELIF call_function COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                        | ELIF call_function COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''
    p = elif_statement_creation(p)

def p_else_rule_func(p):
    '''else_rule_func : ELSE COLON NEWLINE INDENT limited_statement_func DEDENT'''
    p = else_statement_creation(p)

def p_try_rule_func(p):
    '''try_rule_func : TRY COLON NEWLINE INDENT limited_statement_func DEDENT except_rule_func'''
    p = try_statement(p)

def p_except_rule_func(p):
    '''except_rule_func : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func DEDENT
                        | EXCEPT COLON NEWLINE INDENT limited_statement_func DEDENT'''
    p = catch_statement(p)

def p_limited_statement_func_loop(p):
    '''limited_statement_func_loop : limited_statement_func_loop_recv
                                   | limited_statement_values_func_loop_end
                                   | limited_statement_func_loop_recv limited_statement_values_func_loop_end'''
    p = statement_creation(p)

def p_limited_statement_func_loop_recv(p):
    '''limited_statement_func_loop_recv : limited_statement_values_func_loop
                                        | limited_statement_func_loop_recv limited_statement_values_func_loop'''
    p = statement_creation(p)

def p_limited_statement_values_func_loop(p):
    '''limited_statement_values_func_loop : if_rule_func_loop
                                            | STRING NEWLINE
                                            | NONE NEWLINE
                                            | variable NEWLINE
                                            | variable_assign NEWLINE
                                            | tuple NEWLINE
                                            | list NEWLINE
                                            | set NEWLINE
                                            | dictionary NEWLINE
                                            | PASS NEWLINE
                                            | math_expression NEWLINE
                                            | printing NEWLINE
                                            | while_rule_func 
                                            | for_rule_func 
                                            | try_rule_func_loop 
                                            | call_function NEWLINE
                                            | return_statement NEWLINE
                                            | BREAK NEWLINE
                                            | CONTINUE NEWLINE
                                            | NEWLINE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif p[1] == 'continue':
        p[0] = Node(n_type="Continue", value=p[1])
    elif p[1] == 'break':
        p[0] = Node(n_type="Break", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != '\n' and p[1] != 'pass':  # Ignore newlines and pass
        p[0] = p[1]
    else:
        p[0] = None
    
def p_limited_statement_values_func_loop_end(p):
    '''limited_statement_values_func_loop_end : STRING
                                            | NONE
                                            | variable
                                            | variable_assign
                                            | tuple
                                            | list
                                            | set
                                            | dictionary
                                            | PASS
                                            | math_expression
                                            | printing
                                            | call_function
                                            | return_statement
                                            | BREAK
                                            | CONTINUE'''
    if p[1] == 'None': 
        p[0] = Node(n_type="NoneLiteral", value=p[1])
    elif p[1] == 'continue':
        p[0] = Node(n_type="Continue", value=p[1])
    elif p[1] == 'break':
        p[0] = Node(n_type="Break", value=p[1])
    elif isinstance(p[1], str) and (p[1][0] == "\'" or p[1][0] == "\""):
        p[0] = Node(n_type="StringLiteral", value=p[1])
    elif p[1] != 'pass':  # Ignore pass
        p[0] = p[1]
    else:
        p[0] = None

def p_while_rule_func(p):
    '''while_rule_func : WHILE math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | WHILE variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT '''
    p = while_loop_statement(p)

def p_for_rule_func(p):
    '''for_rule_func : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                     | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
    p = for_loop_statement(p)

def p_if_rule_func_loop(p):
    '''if_rule_func_loop : IF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | IF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                        | IF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop
                        | IF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | IF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                        | IF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop
                        | IF call_function COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | IF call_function COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                        | IF call_function COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''
    p = if_statement_creation(p)

def p_elif_rule_func_loop(p):
    '''elif_rule_func_loop : ELIF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | ELIF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                            | ELIF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop
                            | ELIF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | ELIF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                            | ELIF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop
                            | ELIF call_function COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | ELIF call_function COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                            | ELIF call_function COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''
    p = elif_statement_creation(p)

def p_else_rule_func_loop(p):
    '''else_rule_func_loop : ELSE COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
    p = else_statement_creation(p)

def p_try_rule_func_loop(p):
    '''try_rule_func_loop : TRY COLON NEWLINE INDENT limited_statement_func_loop DEDENT except_rule_func_loop'''
    p = try_statement(p)

def p_except_rule_func_loop(p):
    '''except_rule_func_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | EXCEPT COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
    p = catch_statement(p)

def p_def_class(p):
    '''def_class : CLASS VAR_FUNC_NAME COLON NEWLINE INDENT statement DEDENT
                 | CLASS VAR_FUNC_NAME OPEN_PARENTHESIS VAR_FUNC_NAME CLOSED_PARENTHESIS COLON NEWLINE INDENT statement DEDENT'''
    if len(p) == 8:  # Without inheritance
        p[0] = Node(n_type="ClassDefinition", value=p[2], children=[p[6]])
    else:  # With 1 level of inheritance
        p[0] = Node(n_type="ClassDefinition", value=p[2], children=[Node(n_type="Inheritance", value=p[4]), p[9]])
    
def p_error(p):
    global error_count
    if p:
        print(f"Syntax error at token '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at EOF (unexpected end of input)")
    error_count += 1

tokens = Lexer.tokens

class Parser:
    def __init__(self, lexer=None, debug=False):
        self.lexer = lexer
        self.parser = yacc.yacc(debug = debug)
        self.debug = debug
        self.error_count = 0

    def set_lexer(self, lexer):
        self.lexer = lexer

    def parse(self, input_text):
        global error_count
        global debug_parser
        global ast
        debug_parser = self.debug
        self.parser.parse(input_text, lexer=self.lexer, debug=self.debug)
        self.error_count = error_count
        return ast
