from lexer import Lexer
from parser import Parser
from code_gen import CodeGenerator

class Transpiler():
    def __init__(self, file_name, debug=False):
        self.debug = debug
        self.file_name = file_name
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = Parser(debug=self.debug)

    def input(self):
        if self.file_name is None:
            print("Please provide a file name")
            return
        
        try:
            file = open(self.file_name, 'r', encoding='utf-8')      
        except IOError:
            print("ERROR: File does not appear to exist.")
            return

        data = file.read()
        self.lexer.input(data)
        print(f'Error count for lexer: {self.lexer.error_count}')

        if(self.debug and self.lexer.token_stream):
            for i in self.lexer.token_stream:
                print(i)
        if (self.lexer.error_count == 0):
            self.parser.set_lexer(self.lexer)
            ast = self.parser.parse(data)
            print(f"Error count for parsing: {self.parser.error_count}")
            if (self.parser.error_count == 0 and ast is not None ):
                print("AST succesfully created")
                code = CodeGenerator("../output/main.cpp", ast)
                code.generate_code()
                print("Code was generated succesfully")
            

        
