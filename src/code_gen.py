from node import Node

class CodeGenerator:
  def __init__(self, output_file, ast):
    self.root = ast[0]
    self.code = ""
    self.output_file = output_file
  
  def generate_code(self):
    # TODO: generate code string
    
    # TODO: place code in ouput file
