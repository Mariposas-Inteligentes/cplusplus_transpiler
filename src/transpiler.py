from lexer import Lexer
from parser import Parser

class Transpiler():
    def __init__(self, file_name, debug=False):
        self.debug = debug
        self.file_name = file_name
        self.lexer = Lexer()
        self.lexer.build()
        # self.parser = Parser()

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

        if(self.debug and self.lexer.token_stream):
            for i in self.lexer.token_stream:
                print(i)

        # self.parser.set_lexer(self.lexer)

        
