from transpiler import Transpiler
import sys


def main():
    if (len(sys.argv) < 2):
        print('Please insert a .py file to transpile')
        return
    
    file_name = sys.argv[1]
    transpiler = Transpiler(file_name=file_name, debug=True)
    transpiler.input()

if __name__ == "__main__":
    main()