import ply.yacc as yacc
from lexer import Lexer

error_count = 0

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'FLOOR_DIV', 'DIV',  'MODULO'),
    ('left', 'POWER'),
    ('left', 'PLUS_EQUALS', 'MINUS_EQUALS', 'MODULO_EQUALS', 'MUL_EQUALS', 'DIV_EQUALS'),
    ('left', 'FLOOR_DIV_EQUALS', 'POWER_EQUALS'),
)

def p_start(p):
    '''start : START_MARKER statement END_MARKER
            | START_MARKER END_MARKER'''

def p_statement(p):
    '''statement : statement_values
                    | statement NEWLINE statement_values
                    | statement statement_values
                    | statement NEWLINE statement_values NEWLINE'''

def p_statement_values(p):
    '''statement_values : def_function
                        | if_rule
                        | def_class
                        | STRING
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
                        | printing
                        | while_rule
                        | for_rule
                        | try_rule
                        | NEWLINE'''

def p_def_function(p):
    '''def_function : DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT
                    | DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter_assign CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT
                    | DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter COMMA def_parameter_assign CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT
                    | DEF VAR_FUNC_NAME OPEN_PARENTHESIS CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT'''

def p_def_parameter(p):
    '''def_parameter : VAR_FUNC_NAME
                     | def_parameter COMMA VAR_FUNC_NAME'''

def p_def_parameter_assign(p):
    '''def_parameter_assign : def_parameter_assign COMMA VAR_FUNC_NAME ASSIGN values
                            | VAR_FUNC_NAME ASSIGN values'''

def p_func_statement(p):
    '''func_statement : func_statement_values
                        | func_statement NEWLINE func_statement_values
                        | func_statement func_statement_values
                        | func_statement NEWLINE func_statement_values NEWLINE'''

def p_func_statement_values(p):
    '''func_statement_values : if_rule_func
                               | STRING 
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
                               | while_rule_func
                               | for_rule_func
                               | return_statement
                               | try_rule_func
                               | NEWLINE'''

def p_return_statement(p):
    '''return_statement : RETURN
                        | RETURN call_function
                        | RETURN variable
                        | RETURN values
                        | RETURN list
                        | RETURN dictionary
                        | RETURN set
                        | RETURN tuple'''

def p_call_function(p):
    '''call_function : VAR_FUNC_NAME OPEN_PARENTHESIS call_parameter CLOSED_PARENTHESIS
                        | VAR_FUNC_NAME OPEN_PARENTHESIS CLOSED_PARENTHESIS'''

def p_call_parameter(p):
    '''call_parameter : call_function_parameter'''

def p_call_function_parameter(p):
    '''call_function_parameter : call_function_parameter COMMA VAR_FUNC_NAME ASSIGN values
                                | VAR_FUNC_NAME ASSIGN values
                                | values
                                | call_function_parameter COMMA values
                                | call_function_parameter COMMA VAR_FUNC_NAME ASSIGN call_function
                                | VAR_FUNC_NAME ASSIGN call_function
                                | call_function
                                | call_function_parameter COMMA call_function
                                | call_function_parameter COMMA VAR_FUNC_NAME ASSIGN variable
                                | VAR_FUNC_NAME ASSIGN variable
                                | variable
                                | call_function_parameter COMMA variable'''

def p_values(p):
    '''values : math_expression
                | STRING
                | NONE'''

def p_math_values(p):
    '''math_values : INT
                    | FLOAT
                    | bool_values
                    | MINUS INT
                    | PLUS INT
                    | MINUS FLOAT
                    | PLUS FLOAT'''

def p_bool_values(p):
    '''bool_values : TRUE
                    | FALSE'''

def p_period_operator(p):
    '''period_operator : period_operator PERIOD VAR_FUNC_NAME
                       | period_operator PERIOD call_function
                       | PERIOD VAR_FUNC_NAME
                       | PERIOD call_function'''


def p_access_content(p):
    '''access_content : values
                      | variable
                      | tuple'''

def p_variable_assign(p):
    '''variable_assign : variable_assign_var
                       | variable_assign_expr'''

def p_variable_assign_expr(p):
    '''variable_assign_expr : variable math_assign math_expression
                            | variable math_assign STRING
                            | variable_assign_var math_assign math_expression
                            | variable_assign_var math_assign STRING
                            | variable math_assign call_function
                            | variable_assign_var math_assign call_function
                            | variable ASSIGN data_structures
                            | variable_assign_var ASSIGN data_structures'''

def p_data_structures(p):
    '''data_structures : list
                        | set
                        | tuple
                        | dictionary'''

def p_variable_assign_var(p):
    '''variable_assign_var : variable math_assign variable
                           | variable_assign_var math_assign variable'''

def p_variable(p):
    '''variable : VAR_FUNC_NAME
                | variable period_operator
                | variable OPEN_BRACKET access_content CLOSED_BRACKET
                | variable OPEN_BRACKET access_content COLON access_content CLOSED_BRACKET
                | variable OPEN_BRACKET access_content COLON CLOSED_BRACKET'''

def p_math_expression(p):
    '''math_expression : math_values
                       | OPEN_PARENTHESIS math_expression CLOSED_PARENTHESIS
                       | OPEN_PARENTHESIS STRING CLOSED_PARENTHESIS
                       | OPEN_PARENTHESIS variable CLOSED_PARENTHESIS
                       | OPEN_PARENTHESIS call_function CLOSED_PARENTHESIS
                       | NOT math_expression
                       | MINUS OPEN_PARENTHESIS math_expression CLOSED_PARENTHESIS
                       | math_expression math_symbols expr_math_values_recv
                       | STRING math_symbols expr_math_values_recv
                       | variable math_symbols expr_math_values_recv
                       | call_function math_symbols expr_math_values_recv
                       | math_expression math_symbols variable math_symbols expr_math_values_recv
                       | math_expression math_symbols call_function math_symbols expr_math_values_recv
                       | STRING math_symbols variable math_symbols expr_math_values_recv
                       | STRING math_symbols call_function math_symbols expr_math_values_recv'''

def p_expr_math_values_recv(p):
    '''expr_math_values_recv : math_values
                            | STRING
                            | variable
                            | call_function
                            | OPEN_PARENTHESIS math_expression CLOSED_PARENTHESIS
                            | OPEN_PARENTHESIS variable CLOSED_PARENTHESIS
                            | OPEN_PARENTHESIS call_function CLOSED_PARENTHESIS'''
    
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

def p_math_assign(p):
    '''math_assign  : ASSIGN
                    | PLUS_EQUALS
                    | MINUS_EQUALS
                    | MUL_EQUALS
                    | DIV_EQUALS
                    | MODULO_EQUALS
                    | FLOOR_DIV_EQUALS
                    | POWER_EQUALS'''


def p_logic_symbols(p):
    '''logic_symbols : OR
                    | AND
                    | IN'''

def p_cmp_symbols(p):
    '''cmp_symbols : EQUALS
                    | DIFFERENT
                    | LESS
                    | MORE
                    | LESS_EQUALS
                    | MORE_EQUALS'''

def p_tuple(p):
    '''tuple : OPEN_PARENTHESIS list_tuple_recursion COMMA list_tuple_values CLOSED_PARENTHESIS'''

def p_list(p):
    '''list : OPEN_BRACKET list_tuple_recursion CLOSED_BRACKET
            | OPEN_BRACKET CLOSED_BRACKET'''

def p_list_tuple_recursion(p):
    '''list_tuple_recursion : list_tuple_recursion COMMA list_tuple_values
                            | list_tuple_values'''

def p_list_tuple_values(p):
    '''list_tuple_values :   tuple
                            | list
                            | set
                            | dictionary
                            | values
                            | variable
                            | call_function'''

def p_set(p):
    '''set : OPEN_CURLY_BRACKET set_recursion CLOSED_CURLY_BRACKET'''

def p_set_recursion(p):
    '''set_recursion : set_recursion COMMA set_values
                        | set_values'''

def p_set_values(p):
    '''set_values : tuple
                    | values'''

def p_dictionary(p):
    '''dictionary : OPEN_CURLY_BRACKET dictionary_content CLOSED_CURLY_BRACKET
                   | OPEN_CURLY_BRACKET CLOSED_CURLY_BRACKET'''

def p_dictionary_content(p):
    '''dictionary_content : dictionary_content COMMA list_tuple_values COLON list_tuple_values
                          | dictionary_content COMMA values COLON list_tuple_values
                          | list_tuple_values COLON list_tuple_values
                          | values COLON list_tuple_values'''

def p_printing(p):
    '''printing : PRINT OPEN_PARENTHESIS print_content CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS NONE CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS CLOSED_PARENTHESIS'''

def p_print_content(p):
    '''print_content : print_content PLUS print_content_value
                    | print_content_value'''

def p_print_content_value(p):
    '''print_content_value : math_values
                            | STRING
                            | call_function
                            | variable
                            | list
                            | tuple
                            | set
                            | dictionary'''

def p_limited_statement(p):
    '''limited_statement : limited_statement_values
                            | limited_statement NEWLINE limited_statement_values
                            | limited_statement limited_statement_values'''

def p_limited_statement_values(p):
    '''limited_statement_values : if_rule
                                | STRING
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
                                | while_rule
                                | for_rule
                                | try_rule
                                | NEWLINE'''

def p_if_rule(p):
    '''if_rule : IF math_expression COLON NEWLINE INDENT limited_statement DEDENT
                | IF math_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                | IF math_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule
                | IF variable COLON NEWLINE INDENT limited_statement DEDENT
                | IF variable COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                | IF variable COLON NEWLINE INDENT limited_statement DEDENT else_rule'''

def p_elif_rule(p):
    '''elif_rule : ELIF math_expression COLON NEWLINE INDENT limited_statement DEDENT
                    | ELIF math_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                    | ELIF math_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule
                    | ELIF variable COLON NEWLINE INDENT limited_statement DEDENT
                    | ELIF variable COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                    | ELIF variable COLON NEWLINE INDENT limited_statement DEDENT else_rule'''

def p_else_rule(p):
    '''else_rule : ELSE COLON NEWLINE INDENT limited_statement DEDENT'''

def p_loop_statement(p):
    '''loop_statement : loop_statement_values
                        | loop_statement NEWLINE loop_statement_values
                        | loop_statement loop_statement_values'''

def p_loop_statement_values(p):
    '''loop_statement_values : if_rule_loop
                                | STRING
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
                                | while_rule
                                | for_rule
                                | try_rule_loop
                                | call_function
                                | CONTINUE
                                | BREAK
                                | NEWLINE'''

def p_while_rule(p):
    '''while_rule : WHILE math_expression COLON NEWLINE INDENT loop_statement DEDENT
                    | WHILE variable COLON NEWLINE INDENT loop_statement DEDENT
                    | WHILE VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT loop_statement DEDENT
                    | WHILE OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT loop_statement DEDENT'''

def p_for_rule(p):
    '''for_rule : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT loop_statement DEDENT
                | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT loop_statement DEDENT'''

def p_for_rule_content(p):
    '''for_rule_content : call_function
                        | VAR_FUNC_NAME
                        | list
                        | tuple
                        | dictionary
                        | set'''

def p_try_rule(p):
    '''try_rule : TRY COLON NEWLINE INDENT limited_statement DEDENT
                | TRY COLON NEWLINE INDENT limited_statement DEDENT except_rule'''

def p_except_rule(p):
    '''except_rule : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement DEDENT
                    | EXCEPT COLON NEWLINE INDENT limited_statement DEDENT'''

def p_limited_statement_loop(p):
    '''limited_statement_loop : limited_statement_values_loop
                                | limited_statement_loop NEWLINE limited_statement_values_loop
                                | limited_statement_loop limited_statement_values_loop'''

def p_limited_statement_values_loop(p):
    '''limited_statement_values_loop : if_rule_loop
                                        | STRING
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
                                        | while_rule
                                        | for_rule
                                        | try_rule_loop
                                        | BREAK
                                        | CONTINUE
                                        | NEWLINE'''

def p_if_rule_loop(p):
    '''if_rule_loop : IF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                    | IF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                    | IF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop
                    | IF variable COLON NEWLINE INDENT limited_statement_loop DEDENT
                    | IF variable COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                    | IF variable COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''

def p_elif_rule_loop(p):
    '''elif_rule_loop : ELIF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                      | ELIF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                      | ELIF math_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop
                      | ELIF variable COLON NEWLINE INDENT limited_statement_loop DEDENT
                      | ELIF variable COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                      | ELIF variable COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''

def p_else_rule_loop(p):
    '''else_rule_loop : ELSE COLON NEWLINE INDENT limited_statement_loop DEDENT'''

def p_try_rule_loop(p):
    '''try_rule_loop : TRY COLON NEWLINE INDENT limited_statement_loop DEDENT
                        | TRY COLON NEWLINE INDENT limited_statement_loop DEDENT except_rule_loop'''

def p_except_rule_loop(p):
    '''except_rule_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_loop DEDENT
                        | EXCEPT COLON NEWLINE INDENT limited_statement_loop DEDENT'''

def p_limited_statement_func(p):
    '''limited_statement_func : limited_statement_values_func
                                | limited_statement_func NEWLINE limited_statement_values_func
                                | limited_statement_func limited_statement_values_func'''

def p_limited_statement_values_func(p):
    '''limited_statement_values_func : if_rule_func
                                        | STRING
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
                                        | while_rule_func
                                        | for_rule_func
                                        | try_rule_func
                                        | return_statement
                                        | NEWLINE'''

def p_if_rule_func(p):
    '''if_rule_func : IF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                    | IF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                    | IF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func
                    | IF variable COLON NEWLINE INDENT limited_statement_func DEDENT
                    | IF variable COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                    | IF variable COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''

def p_elif_rule_func(p):
    '''elif_rule_func : ELIF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                        | ELIF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                        | ELIF math_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func
                        | ELIF variable COLON NEWLINE INDENT limited_statement_func DEDENT
                        | ELIF variable COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                        | ELIF variable COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''

def p_else_rule_func(p):
    '''else_rule_func : ELSE COLON NEWLINE INDENT limited_statement_func DEDENT'''

def p_try_rule_func(p):
    '''try_rule_func : TRY COLON NEWLINE INDENT limited_statement_func DEDENT
                        | TRY COLON NEWLINE INDENT limited_statement_func DEDENT except_rule_func'''

def p_except_rule_func(p):
    '''except_rule_func : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func DEDENT
                        | EXCEPT COLON NEWLINE INDENT limited_statement_func DEDENT'''

def p_limited_statement_func_loop(p):
    '''limited_statement_func_loop : limited_statement_values_func_loop
                                    | limited_statement_func_loop NEWLINE limited_statement_values_func_loop
                                    | limited_statement_func_loop limited_statement_values_func_loop'''

def p_limited_statement_values_func_loop(p):
    '''limited_statement_values_func_loop : if_rule_func_loop
                                            | STRING
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
                                            | while_rule_func
                                            | for_rule_func
                                            | try_rule_func_loop
                                            | call_function
                                            | return_statement
                                            | BREAK
                                            | CONTINUE
                                            | NEWLINE'''

def p_while_rule_func(p):
    '''while_rule_func : WHILE math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | WHILE variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | WHILE VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | WHILE OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''

def p_for_rule_func(p):
    '''for_rule_func : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''

def p_if_rule_func_loop(p):
    '''if_rule_func_loop : IF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | IF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                        | IF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop
                        | IF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | IF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                        | IF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''

def p_elif_rule_func_loop(p):
    '''elif_rule_func_loop : ELIF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | ELIF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                            | ELIF math_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop
                            | ELIF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | ELIF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                            | ELIF variable COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''

def p_else_rule_func_loop(p):
    '''else_rule_func_loop : ELSE COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''

def p_try_rule_func_loop(p):
    '''try_rule_func_loop : TRY COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | TRY COLON NEWLINE INDENT limited_statement_func_loop DEDENT except_rule_func_loop'''

def p_except_rule_func_loop(p):
    '''except_rule_func_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | EXCEPT COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''

def p_def_class(p):
    '''def_class : CLASS VAR_FUNC_NAME COLON NEWLINE INDENT statement DEDENT
                    | CLASS VAR_FUNC_NAME OPEN_PARENTHESIS VAR_FUNC_NAME CLOSED_PARENTHESIS COLON NEWLINE INDENT statement DEDENT'''

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
        self.parser.parse(input_text, lexer=self.lexer, debug=self.debug)
        global error_count
        self.error_count = error_count
