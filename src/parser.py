import ply.yacc as yacc
from lexer import Lexer

def p_start(p):
    '''start : START_MARKER statement END_MARKER'''
    pass

def p_statement(p):
    '''statement : statement_values
                    | statement NEWLINE statement_values
                    | statement NEWLINE statement_values NEWLINE'''
    pass

def p_statement_values(p):
    '''statement_values : def_function
                        | if_rule
                        | def_class
                        | call_function
                        | values
                        | variable
                        | def_variable
                        | tuple
                        | list
                        | set
                        | dictionary
                        | PASS
                        | bool_expression
                        | printing
                        | while_rule
                        | for_rule
                        | try_rule'''
    pass

def p_def_function(p):
    '''def_function : DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT'''
    pass

def p_func_statement(p):
    '''func_statement : func_statement_values
                        | func_statement NEWLINE func_statement_values
                        | func_statement NEWLINE func_statement_values NEWLINE'''
    pass

def p_func_statement_values(p):
    '''func_statement_values : if_rule_func
                                | call_function
                                | values
                                | variable
                                | def_variable
                                | tuple
                                | list
                                | set
                                | dictionary
                                | bool_expression
                                | PASS
                                | printing
                                | while_rule_func
                                | for_rule_func
                                | return_statement
                                | try_rule_func'''
    pass

def p_return_statement(p):
    '''return_statement : RETURN return_values'''
    pass

def p_return_values(p):
    '''return_values : values_and_call_function
                        | bool_expression'''
    pass

def p_call_function(p):
    '''call_function : VAR_FUNC_NAME OPEN_PARENTHESIS call_parameter CLOSED_PARENTHESIS
                        | VAR_FUNC_NAME PERIOD OPEN_PARENTHESIS call_parameter CLOSED_PARENTHESIS'''
    pass

def p_def_parameter(p):
    '''def_parameter : 
                        | def_function_parameter'''
    pass

def p_def_function_parameter(p):
    '''def_function_parameter : VAR_FUNC_NAME
                                | def_function_parameter COMMA VAR_FUNC_NAME
                                | def_function_parameter COMMA VAR_FUNC_NAME ASSIGN values
                                | VAR_FUNC_NAME ASSIGN values'''
    pass

def p_call_parameter(p):
    '''call_parameter : 
                        | call_function_parameter'''
    pass

def p_call_function_parameter(p):
    '''call_function_parameter : call_function_parameter COMMA VAR_FUNC_NAME ASSIGN values_and_call_function
                                | VAR_FUNC_NAME ASSIGN values_and_call_function
                                | values_and_call_function
                                | call_function_parameter COMMA values_and_call_function'''
    pass

def p_values_and_call_function(p):
    '''values_and_call_function : values
                                | call_function
                                | VAR_FUNC_NAME'''
    pass

def p_values(p):
    '''values : math_values
                | STRING
                | NONE'''
    pass

def p_math_values(p):
    '''math_values : INT
                    | FLOAT
                    | bool_values
                    | MINUS INT
                    | PLUS INT
                    | MINUS FLOAT
                    | PLUS FLOAT'''
    pass

def p_bool_values(p):
    '''bool_values : TRUE
                    | FALSE'''
    pass

def p_variable(p):
    '''variable : VAR_FUNC_NAME
                | def_variable 
                | def_variable_str 
                | call_function 
                | VAR_FUNC_NAME PERIOD VAR_FUNC_NAME
                | VAR_FUNC_NAME PERIOD call_function'''
    pass

def p_def_variable(p):
    '''def_variable : VAR_FUNC_NAME math_assign def_variable_values
                    | VAR_FUNC_NAME PERIOD math_assign def_variable_values'''
    pass

def p_def_variable_values(p):
    '''def_variable_values : variable
                            | math_expression
                            | str_expression
                            | def_variable_str'''
    pass

def p_def_variable_str(p):
    '''def_variable_str : STRING
                        | call_function
                        | def_variable_str PLUS STRING'''
    pass

def p_math_expression(p):
    '''math_expression : math_expression math_symbols expr_math_values
                        | OPEN_PARENTHESIS math_expression CLOSED_PARENTHESIS
                        | expr_math_values
                        | NOT expr_math_values'''
    pass

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
    pass

def p_math_assign(p):
    '''math_assign  : ASSIGN
                    | PLUS_EQUALS
                    | MINUS_EQUALS
                    | MUL_EQUALS
                    | DIV_EQUALS
                    | MODULO_EQUALS
                    | FLOOR_DIV_EQUALS
                    | POWER_EQUALS'''
    pass

def p_bool_expression(p):
    '''bool_expression : math_expression 
                        | str_expression'''
    pass

def p_logic_symbols(p):
    '''logic_symbols : OR
                        | AND'''
    pass

def p_cmp_symbols(p):
    '''cmp_symbols : EQUALS
                    | DIFFERENT
                    | LESS
                    | MORE
                    | LESS_EQUALS
                    | MORE_EQUALS'''
    pass

def p_expr_math_values(p):
    '''expr_math_values : math_values
                        | VAR_FUNC_NAME
                        | call_function'''
    pass

def p_str_expression(p):
    '''str_expression : str_expression str_expression_symbols STRING
                        | OPEN_PARENTHESIS str_expression CLOSED_PARENTHESIS
                        | str_expression str_expression_symbols STRING MUL INT
                        | str_expression str_expression_symbols INT MUL STRING
                        | STRING MUL INT
                        | INT MUL STRING
                        | STRING MUL bool_values
                        | bool_values MUL STRING'''
    pass

def p_str_expression_symbols(p):
    '''str_expression_symbols : cmp_symbols
                                | logic_symbols
                                | PLUS'''
    pass

def p_tuple(p):
    '''tuple : OPEN_PARENTHESIS list_tuple_recursion CLOSED_PARENTHESIS
                | OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
    pass

def p_list(p):
    '''list : OPEN_BRACKET list_tuple_recursion CLOSED_BRACKET
            | OPEN_BRACKET CLOSED_BRACKET'''
    pass

def p_list_tuple_recursion(p):
    '''list_tuple_recursion : list_tuple_recursion COMMA list_tuple_values
                            | list_tuple_values'''
    pass

def p_list_tuple_values(p):
    '''list_tuple_values : tuple
                            | values
                            | list
                            | set
                            | dictionary'''
    pass

def p_set(p):
    '''set : OPEN_CURLY_BRACKET set_recursion CLOSED_CURLY_BRACKET'''
    pass

def p_set_recursion(p):
    '''set_recursion : set_recursion COMMA set_values
                        | set_values'''
    pass

def p_set_values(p):
    '''set_values : tuple
                    | values'''
    pass

def p_dictionary(p):
    '''dictionary : OPEN_CURLY_BRACKET dictionary_content CLOSED_CURLY_BRACKET
                    | OPEN_CURLY_BRACKET CLOSED_CURLY_BRACKET'''
    pass

def p_dictionary_content(p):
    '''dictionary_content : dictionary_content COMMA dictionary_values COLON list_tuple_recursion
                            | dictionary_values COLON list_tuple_recursion'''
    pass

def p_dictionary_values(p):
    '''dictionary_values : dictionary_tuple
                            | values'''
    pass

def p_dictionary_tuple(p):
    '''dictionary_tuple : OPEN_PARENTHESIS dictionary_tuple_recursion CLOSED_PARENTHESIS
                        | OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
    pass

def p_dictionary_tuple_recursion(p):
    '''dictionary_tuple_recursion : dictionary_tuple_recursion COMMA values
                                    | values'''
    pass

def p_printing(p):
    '''printing : PRINT OPEN_PARENTHESIS print_content CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS NONE CLOSED_PARENTHESIS
                | PRINT OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
    pass

def p_print_content(p):
    '''print_content : print_content PLUS print_content_value
                        | print_content_value'''
    pass

def p_print_content_value(p):
    '''print_content_value : math_values
                            | STRING
                            | call_function
                            | list
                            | tuple
                            | set
                            | dictionary'''
    pass

def p_limited_statement(p):
    '''limited_statement : limited_statement_values
                            | limited_statement NEWLINE limited_statement_values
                            | limited_statement NEWLINE limited_statement_values NEWLINE'''
    pass

def p_limited_statement_values(p):
    '''limited_statement_values : if_rule
                                | call_function
                                | values
                                | variable
                                | def_variable
                                | tuple
                                | list
                                | set
                                | dictionary
                                | PASS
                                | bool_expression
                                | printing
                                | while_rule
                                | for_rule
                                | try_rule'''
    pass

def p_if_rule(p):
    '''if_rule : IF bool_expression COLON NEWLINE INDENT limited_statement DEDENT
                | IF bool_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                | IF bool_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule'''
    pass

def p_elif_rule(p):
    '''elif_rule : ELIF bool_expression COLON NEWLINE INDENT limited_statement DEDENT
                    | ELIF bool_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                    | ELIF bool_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule'''
    pass

def p_else_rule(p):
    '''else_rule : ELSE COLON NEWLINE INDENT limited_statement DEDENT'''
    pass

def p_loop_statement(p):
    '''loop_statement : loop_statement_values
                        | loop_statement NEWLINE loop_statement_values
                        | loop_statement NEWLINE loop_statement_values NEWLINE'''
    pass

def p_loop_statement_values(p):
    '''loop_statement_values : if_rule_loop
                                | call_function
                                | values
                                | variable
                                | def_variable
                                | tuple
                                | list
                                | set
                                | dictionary
                                | PASS
                                | bool_expression
                                | printing
                                | while_rule
                                | for_rule
                                | try_rule_loop
                                | CONTINUE
                                | BREAK'''
    pass

def p_while_rule(p):
    '''while_rule : WHILE bool_expression COLON NEWLINE INDENT loop_statement DEDENT
                    | WHILE VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT loop_statement DEDENT
                    | WHILE OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT loop_statement DEDENT'''
    pass

def p_for_rule(p):
    '''for_rule : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT loop_statement DEDENT
                | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT loop_statement DEDENT'''
    pass

def p_for_rule_content(p):
    '''for_rule_content : call_function
                        | VAR_FUNC_NAME
                        | list
                        | tuple
                        | dictionary
                        | set'''
    pass

def p_try_rule(p):
    '''try_rule : TRY COLON NEWLINE INDENT limited_statement DEDENT
                | TRY COLON NEWLINE INDENT limited_statement DEDENT except_rule'''
    pass

def p_except_rule(p):
    '''except_rule : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement DEDENT
                    | EXCEPT COLON NEWLINE INDENT limited_statement DEDENT'''
    pass

def p_limited_statement_loop(p):
    '''limited_statement_loop : limited_statement_values_loop
                                | limited_statement_loop NEWLINE limited_statement_values_loop
                                | limited_statement_loop NEWLINE limited_statement_values_loop NEWLINE'''
    pass

def p_limited_statement_values_loop(p):
    '''limited_statement_values_loop : if_rule_loop
                                        | call_function
                                        | values
                                        | variable
                                        | def_variable
                                        | tuple
                                        | list
                                        | set
                                        | dictionary
                                        | PASS
                                        | bool_expression
                                        | printing
                                        | while_rule
                                        | for_rule
                                        | try_rule_loop
                                        | BREAK
                                        | CONTINUE'''
    pass

def p_if_rule_loop(p):
    '''if_rule_loop : IF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                    | IF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                    | IF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''
    pass

def p_elif_rule_loop(p):
    '''elif_rule_loop : ELIF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                        | ELIF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                        | ELIF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''
    pass

def p_else_rule_loop(p):
    '''else_rule_loop : ELSE COLON NEWLINE INDENT limited_statement_loop DEDENT'''
    pass

def p_try_rule_loop(p):
    '''try_rule_loop : TRY COLON NEWLINE INDENT limited_statement_loop DEDENT
                        | TRY COLON NEWLINE INDENT limited_statement_loop DEDENT except_rule_loop'''
    pass

def p_except_rule_loop(p):
    '''except_rule_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_loop DEDENT
                        | EXCEPT COLON NEWLINE INDENT limited_statement_loop DEDENT'''
    pass

def p_limited_statement_func(p):
    '''limited_statement_func : limited_statement_values_func
                                | limited_statement_func NEWLINE limited_statement_values_func
                                | limited_statement_func NEWLINE limited_statement_values_func NEWLINE'''
    pass

def p_limited_statement_values_func(p):
    '''limited_statement_values_func : if_rule_func
                                        | call_function
                                        | values
                                        | variable
                                        | def_variable
                                        | tuple
                                        | list
                                        | set
                                        | dictionary
                                        | PASS
                                        | bool_expression
                                        | printing
                                        | while_rule_func
                                        | for_rule_func
                                        | try_rule_func
                                        | return_statement'''
    pass

def p_if_rule_func(p):
    '''if_rule_func : IF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                    | IF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                    | IF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''
    pass

def p_elif_rule_func(p):
    '''elif_rule_func : ELIF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                        | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                        | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''
    pass

def p_else_rule_func(p):
    '''else_rule_func : ELSE COLON NEWLINE INDENT limited_statement_func DEDENT'''
    pass

def p_try_rule_func(p):
    '''try_rule_func : TRY COLON NEWLINE INDENT limited_statement_func DEDENT
                        | TRY COLON NEWLINE INDENT limited_statement_func DEDENT except_rule_func'''
    pass

def p_except_rule_func(p):
    '''except_rule_func : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func DEDENT
                        | EXCEPT COLON NEWLINE INDENT limited_statement_func DEDENT'''
    pass

def p_limited_statement_func_loop(p):
    '''limited_statement_func_loop : limited_statement_values_func_loop
                                    | limited_statement_func_loop NEWLINE limited_statement_values_func_loop
                                    | limited_statement_func_loop NEWLINE limited_statement_values_func_loop NEWLINE'''
    pass

def p_limited_statement_values_func_loop(p):
    '''limited_statement_values_func_loop : if_rule_func_loop
                                            | call_function
                                            | values
                                            | variable
                                            | def_variable
                                            | tuple
                                            | list
                                            | set
                                            | dictionary
                                            | PASS
                                            | bool_expression
                                            | printing
                                            | while_rule_func
                                            | for_rule_func
                                            | try_rule_func_loop
                                            | return_statement
                                            | BREAK
                                            | CONTINUE'''
    pass

def p_while_rule_func(p):
    '''while_rule_func : WHILE bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | WHILE VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | WHILE OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
    pass

def p_for_rule_func(p):
    '''for_rule_func : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
    pass

def p_if_rule_func_loop(p):
    '''if_rule_func_loop : IF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                        | IF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                        | IF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''
pass

def p_elif_rule_func_loop(p):
    '''elif_rule_func_loop : ELIF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                            | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''
    pass

def p_else_rule_func_loop(p):
    '''else_rule_func_loop : ELSE COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
    pass

def p_try_rule_func_loop(p):
    '''try_rule_func_loop : TRY COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | TRY COLON NEWLINE INDENT limited_statement_func_loop DEDENT except_rule_func_loop'''
    pass

def p_except_rule_func_loop(p):
    '''except_rule_func_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | EXCEPT COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
    pass

def p_def_class(p):
    '''def_class : CLASS VAR_FUNC_NAME COLON NEWLINE INDENT statement DEDENT
                    | CLASS VAR_FUNC_NAME OPEN_PARENTHESIS VAR_FUNC_NAME CLOSED_PARENTHESIS COLON NEWLINE INDENT statement DEDENT'''
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

tokens = Lexer.tokens

class Parser:
    def __init__(self, lexer=None):
        self.lexer = lexer
        self.parser = yacc.yacc(module=self)

    def set_lexer(self, lexer):
        self.lexer = lexer

    def parse(self, input_text):
        return self.parser.parse(input_text, lexer=self.lexer)
