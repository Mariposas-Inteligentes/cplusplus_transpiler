import ply.yacc as yacc

class Parser:
    tokens = Lexer.tokens  

    def __init__(self, lexer):
        self.lexer = lexer
        self.parser = yacc.yacc(module=self)

    # Grammar rules
    def p_start(self, p):
        '''start : START_MARKER statement END_MARKER'''
        pass

    def p_statement(self, p):
        '''statement : statement_values
                     | statement NEWLINE statement_values
                     | statement NEWLINE statement_values NEWLINE'''
        pass

    def p_statement_values(self, p):
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

    def p_def_function(self, p):
        '''def_function : DEF VAR_FUNC_NAME OPEN_PARENTHESIS def_parameter CLOSED_PARENTHESIS COLON NEWLINE INDENT func_statement DEDENT'''
        pass

    def p_func_statement(self, p):
        '''func_statement : func_statement_values
                          | func_statement NEWLINE func_statement_values
                          | func_statement NEWLINE func_statement_values NEWLINE'''
        pass

    def p_func_statement_values(self, p):
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

    def p_return_statement(self, p):
        '''return_statement : RETURN return_values'''
        pass

    def p_return_values(self, p):
        '''return_values : values_and_call_function
                         | bool_expression'''
        pass

    def p_call_function(self, p):
        '''call_function : VAR_FUNC_NAME OPEN_PARENTHESIS call_parameter CLOSED_PARENTHESIS
                         | VAR_FUNC_NAME PERIOD OPEN_PARENTHESIS call_parameter CLOSED_PARENTHESIS'''
        pass

    def p_def_parameter(self, p):
        '''def_parameter : 
                         | def_function_parameter'''
        pass

    def p_def_function_parameter(self, p):
        '''def_function_parameter : VAR_FUNC_NAME
                                  | def_function_parameter COMMA VAR_FUNC_NAME
                                  | def_function_parameter COMMA VAR_FUNC_NAME ASSIGN values
                                  | VAR_FUNC_NAME ASSIGN values'''
        pass

    def p_call_parameter(self, p):
        '''call_parameter : 
                          | call_function_parameter'''
        pass

    def p_call_function_parameter(self, p):
        '''call_function_parameter : call_function_parameter COMMA VAR_FUNC_NAME ASSIGN values_and_call_function
                                   | VAR_FUNC_NAME ASSIGN values_and_call_function
                                   | values_and_call_function
                                   | call_function_parameter COMMA values_and_call_function'''
        pass

    def p_values_and_call_function(self, p):
        '''values_and_call_function : values
                                    | call_function
                                    | VAR_FUNC_NAME'''
        pass

    def p_values(self, p):
        '''values : math_values
                  | STRING
                  | NONE'''
        pass

    def p_math_values(self, p):
        '''math_values : INT
                       | FLOAT
                       | bool_values
                       | MINUS INT
                       | PLUS INT
                       | MINUS FLOAT
                       | PLUS FLOAT'''
        pass

    def p_bool_values(self, p):
        '''bool_values : TRUE
                       | FALSE'''
        pass

    def p_variable(self, p):
        '''variable : VAR_FUNC_NAME
                    | def_variable 
                    | def_variable_str 
                    | call_function 
                    | VAR_FUNC_NAME PERIOD VAR_FUNC_NAME
                    | VAR_FUNC_NAME PERIOD call_function'''
        pass

    def p_def_variable(self, p):
        '''def_variable : VAR_FUNC_NAME math_assign def_variable_values
                        | VAR_FUNC_NAME PERIOD math_assign def_variable_values'''
        pass

    def p_def_variable_values(self, p):
        '''def_variable_values : variable
                               | math_expression
                               | str_expression
                               | def_variable_str'''
        pass

    def p_def_variable_str(self, p):
        '''def_variable_str : STRING
                            | call_function
                            | def_variable_str PLUS STRING'''
        pass

    def p_math_expression(self, p):
        '''math_expression : math_expression math_symbols expr_math_values
                           | OPEN_PARENTHESIS math_expression CLOSED_PARENTHESIS
                           | expr_math_values
                           | NOT expr_math_values'''
        pass

    def p_math_symbols(self, p):
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

    def p_math_assign(self, p):
        '''math_assign  : ASSIGN
                        | PLUS_EQUALS
                        | MINUS_EQUALS
                        | MUL_EQUALS
                        | DIV_EQUALS
                        | MODULO_EQUALS
                        | FLOOR_DIV_EQUALS
                        | POWER_EQUALS'''
        pass

    def p_bool_expression(self, p):
        '''bool_expression : math_expression 
                            | str_expression'''
        pass

    def p_logic_symbols(self, p):
        '''logic_symbols : OR
                         | AND'''
        pass

    def p_cmp_symbols(self, p):
        '''cmp_symbols : EQUALS
                       | DIFFERENT
                       | LESS
                       | MORE
                       | LESS_EQUALS
                       | MORE_EQUALS'''
        pass

    def p_expr_math_values(self, p):
        '''expr_math_values : math_values
                            | VAR_FUNC_NAME
                            | call_function'''
        pass

    def p_str_expression(self, p):
        '''str_expression : str_expression str_expression_symbols STRING
                          | OPEN_PARENTHESIS str_expression CLOSED_PARENTHESIS
                          | str_expression str_expression_symbols STRING MUL INT
                          | str_expression str_expression_symbols INT MUL STRING
                          | STRING MUL INT
                          | INT MUL STRING
                          | STRING MUL bool_values
                          | bool_values MUL STRING'''
        pass

    def p_str_expression_symbols(self, p):
        '''str_expression_symbols : cmp_symbols
                                  | logic_symbols
                                  | PLUS'''
        pass

    def p_tuple(self, p):
        '''tuple : OPEN_PARENTHESIS list_tuple_recursion CLOSED_PARENTHESIS
                 | OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
        pass

    def p_list(self, p):
        '''list : OPEN_BRACKET list_tuple_recursion CLOSED_BRACKET
                | OPEN_BRACKET CLOSED_BRACKET'''
        pass

    def p_list_tuple_recursion(self, p):
        '''list_tuple_recursion : list_tuple_recursion COMMA list_tuple_values
                                | list_tuple_values'''
        pass

    def p_list_tuple_values(self, p):
        '''list_tuple_values : tuple
                             | values
                             | list
                             | set
                             | dictionary'''
        pass

    def p_set(self, p):
        '''set : OPEN_CURLY_BRACKET set_recursion CLOSED_CURLY_BRACKET'''
        pass

    def p_set_recursion(self, p):
        '''set_recursion : set_recursion COMMA set_values
                         | set_values'''
        pass

    def p_set_values(self, p):
        '''set_values : tuple
                      | values'''
        pass

    def p_dictionary(self, p):
        '''dictionary : OPEN_CURLY_BRACKET dictionary_content CLOSED_CURLY_BRACKET
                      | OPEN_CURLY_BRACKET CLOSED_CURLY_BRACKET'''
        pass

    def p_dictionary_content(self, p):
        '''dictionary_content : dictionary_content COMMA dictionary_values COLON list_tuple_recursion
                              | dictionary_values COLON list_tuple_recursion'''
        pass

    def p_dictionary_values(self, p):
        '''dictionary_values : dictionary_tuple
                             | values'''
        pass

    def p_dictionary_tuple(self, p):
        '''dictionary_tuple : OPEN_PARENTHESIS dictionary_tuple_recursion CLOSED_PARENTHESIS
                            | OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
        pass

    def p_dictionary_tuple_recursion(self, p):
        '''dictionary_tuple_recursion : dictionary_tuple_recursion COMMA values
                                      | values'''
        pass

    def p_printing(self, p):
        '''printing : PRINT OPEN_PARENTHESIS print_content CLOSED_PARENTHESIS
                    | PRINT OPEN_PARENTHESIS NONE CLOSED_PARENTHESIS
                    | PRINT OPEN_PARENTHESIS CLOSED_PARENTHESIS'''
        pass

    def p_print_content(self, p):
        '''print_content : print_content PLUS print_content_value
                         | print_content_value'''
        pass

    def p_print_content_value(self, p):
        '''print_content_value : math_values
                               | STRING
                               | call_function
                               | list
                               | tuple
                               | set
                               | dictionary'''
        pass

    def p_limited_statement(self, p):
        '''limited_statement : limited_statement_values
                             | limited_statement NEWLINE limited_statement_values
                             | limited_statement NEWLINE limited_statement_values NEWLINE'''
        pass

    def p_limited_statement_values(self, p):
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

    def p_if_rule(self, p):
        '''if_rule : IF bool_expression COLON NEWLINE INDENT limited_statement DEDENT
                   | IF bool_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                   | IF bool_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule'''
        pass

    def p_elif_rule(self, p):
        '''elif_rule : ELIF bool_expression COLON NEWLINE INDENT limited_statement DEDENT
                     | ELIF bool_expression COLON NEWLINE INDENT limited_statement DEDENT elif_rule
                     | ELIF bool_expression COLON NEWLINE INDENT limited_statement DEDENT else_rule'''
        pass

    def p_else_rule(self, p):
        '''else_rule : ELSE COLON NEWLINE INDENT limited_statement DEDENT'''
        pass

    def p_loop_statement(self, p):
        '''loop_statement : loop_statement_values
                          | loop_statement NEWLINE loop_statement_values
                          | loop_statement NEWLINE loop_statement_values NEWLINE'''
        pass

    def p_loop_statement_values(self, p):
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

    def p_while_rule(self, p):
        '''while_rule : WHILE bool_expression COLON NEWLINE INDENT loop_statement DEDENT
                      | WHILE VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT loop_statement DEDENT
                      | WHILE OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT loop_statement DEDENT'''
        pass

    def p_for_rule(self, p):
        '''for_rule : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT loop_statement DEDENT
                    | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT loop_statement DEDENT'''
        pass

    def p_for_rule_content(self, p):
        '''for_rule_content : call_function
                            | VAR_FUNC_NAME
                            | list
                            | tuple
                            | dictionary
                            | set'''
        pass

    def p_try_rule(self, p):
        '''try_rule : TRY COLON NEWLINE INDENT limited_statement DEDENT
                    | TRY COLON NEWLINE INDENT limited_statement DEDENT except_rule'''
        pass

    def p_except_rule(self, p):
        '''except_rule : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement DEDENT
                       | EXCEPT COLON NEWLINE INDENT limited_statement DEDENT'''
        pass

    def p_limited_statement_loop(self, p):
        '''limited_statement_loop : limited_statement_values_loop
                                  | limited_statement_loop NEWLINE limited_statement_values_loop
                                  | limited_statement_loop NEWLINE limited_statement_values_loop NEWLINE'''
        pass

    def p_limited_statement_values_loop(self, p):
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

    def p_if_rule_loop(self, p):
        '''if_rule_loop : IF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                        | IF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                        | IF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''
        pass

    def p_elif_rule_loop(self, p):
        '''elif_rule_loop : ELIF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT
                          | ELIF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT elif_rule_loop
                          | ELIF bool_expression COLON NEWLINE INDENT limited_statement_loop DEDENT else_rule_loop'''
        pass

    def p_else_rule_loop(self, p):
        '''else_rule_loop : ELSE COLON NEWLINE INDENT limited_statement_loop DEDENT'''
        pass

    def p_try_rule_loop(self, p):
        '''try_rule_loop : TRY COLON NEWLINE INDENT limited_statement_loop DEDENT
                         | TRY COLON NEWLINE INDENT limited_statement_loop DEDENT except_rule_loop'''
        pass

    def p_except_rule_loop(self, p):
        '''except_rule_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_loop DEDENT
                            | EXCEPT COLON NEWLINE INDENT limited_statement_loop DEDENT'''
        pass

    def p_limited_statement_func(self, p):
        '''limited_statement_func : limited_statement_values_func
                                  | limited_statement_func NEWLINE limited_statement_values_func
                                  | limited_statement_func NEWLINE limited_statement_values_func NEWLINE'''
        pass

    def p_limited_statement_values_func(self, p):
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

    def p_if_rule_func(self, p):
        '''if_rule_func : IF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                        | IF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                        | IF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''
        pass

    def p_elif_rule_func(self, p):
        '''elif_rule_func : ELIF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT
                          | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT elif_rule_func
                          | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func DEDENT else_rule_func'''
        pass

    def p_else_rule_func(self, p):
        '''else_rule_func : ELSE COLON NEWLINE INDENT limited_statement_func DEDENT'''
        pass

    def p_try_rule_func(self, p):
        '''try_rule_func : TRY COLON NEWLINE INDENT limited_statement_func DEDENT
                         | TRY COLON NEWLINE INDENT limited_statement_func DEDENT except_rule_func'''
        pass

    def p_except_rule_func(self, p):
        '''except_rule_func : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func DEDENT
                            | EXCEPT COLON NEWLINE INDENT limited_statement_func DEDENT'''
        pass

    def p_limited_statement_func_loop(self, p):
        '''limited_statement_func_loop : limited_statement_values_func_loop
                                       | limited_statement_func_loop NEWLINE limited_statement_values_func_loop
                                       | limited_statement_func_loop NEWLINE limited_statement_values_func_loop NEWLINE'''
        pass

    def p_limited_statement_values_func_loop(self, p):
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

    def p_while_rule_func(self, p):
        '''while_rule_func : WHILE bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                           | WHILE VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                           | WHILE OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
        pass

    def p_for_rule_func(self, p):
        '''for_rule_func : FOR VAR_FUNC_NAME IN for_rule_content COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                         | FOR OPEN_PARENTHESIS VAR_FUNC_NAME IN for_rule_content CLOSED_PARENTHESIS COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
        pass

    def p_if_rule_func_loop(self, p):
      '''if_rule_func_loop : IF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                            | IF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                            | IF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''
    pass

    def p_elif_rule_func_loop(self, p):
        '''elif_rule_func_loop : ELIF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                              | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT elif_rule_func_loop
                              | ELIF bool_expression COLON NEWLINE INDENT limited_statement_func_loop DEDENT else_rule_func_loop'''
        pass

    def p_else_rule_func_loop(self, p):
        '''else_rule_func_loop : ELSE COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
        pass

    def p_try_rule_func_loop(self, p):
        '''try_rule_func_loop : TRY COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                              | TRY COLON NEWLINE INDENT limited_statement_func_loop DEDENT except_rule_func_loop'''
        pass

    def p_except_rule_func_loop(self, p):
        '''except_rule_func_loop : EXCEPT VAR_FUNC_NAME COLON NEWLINE INDENT limited_statement_func_loop DEDENT
                                | EXCEPT COLON NEWLINE INDENT limited_statement_func_loop DEDENT'''
        pass

    def p_def_class(self, p):
        '''def_class : CLASS VAR_FUNC_NAME COLON NEWLINE INDENT statement DEDENT
                     | CLASS VAR_FUNC_NAME OPEN_PARENTHESIS VAR_FUNC_NAME CLOSED_PARENTHESIS COLON NEWLINE INDENT statement DEDENT'''
        pass

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    # Parse input
    def parse(self, input_text):
        return self.parser.parse(input_text, lexer=self.lexer.lexer)
