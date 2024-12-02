from transpiler import Transpiler
import sys

def main():
    debug = False

    if (len(sys.argv) < 2):
        print('Please insert a .py file to transpile')
        return
    if (len(sys.argv) == 3):
        if (sys.argv[2] == "debug"):
            debug = True
    
    file_name = sys.argv[1]
    if (file_name[len(file_name) - 3:] != ".py"):
        print('Please insert a file with a .py extension')
        return

    transpiler = Transpiler(file_name=file_name, debug=debug)
    transpiler.input()

if __name__ == "__main__":
    main()