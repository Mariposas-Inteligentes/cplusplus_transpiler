# **Python to C++ Transpiler**

Transpiler from a Python subset of instructions to C++ implemented using the PLY library.

## **Dependencies**

To use the project certain packages are required.

To install them you can run the following command in your terminal:

``` bash
pip install -r requirements.txt
```

## **Use manual**

### **Execution commands**

To use the transpiler itself, you can execute the following command from the `src` directory:

``` bash
python main.py (file_name) [debug]
```

Where `(file_name)` corresponds to an obligatory parameter and a file with the following characteristics:

1. The file must have a `.py` extension.
2. The file must exist.

And `[debug]` corresponds to an optional parameter, if set to the string `"debug"` it will print out PLY's debugging mecanisms and the generated AST (Abstract Syntax Tree).

The generated code will be in `output/main.cpp`.

To compile the generated code, run the following command in the `output` directory:

    g++ -o transpiled_code main.cpp

Then, to execute it, run the following command in the `output` directory:

    ./transpiled_code

### **Execution example**

An execution example can be done with the file [test_principal_cases.py](src/tests/transpiler_test_files/test_principal_cases.py)

``` bash
python main.py tests/transpiler_test_files/test_principal_cases.py
```

To run it in debug mode you can do so the following way:

``` bash
python main.py tests/transpiler_test_files/test_principal_cases.py debug
```

## **Tests**

### **Lexer**

To run the unit tests for the lexer, the pytest module is utilized.

To execute all tests once, you must be in the `src/tests/lexer_test_files` directory and run the following command:

``` bash
python -m pytest
```

In case of wanting to run a specific test, you can execute the following command:

``` bash
python -m pytest [file_name]
```

The current options for <file_name> are:

1. `test_indentation.py`
2. `test_tokens.py`

### **Parser**

To execute the unit tests for the parser, pytest is not required.

Therefore, inside the `src` directory the following command must be executed.

``` bash
python ./tests/test_parsing.py
```

This will run all the parsing tests at once, and tell you the total amount of tests passed and failed.


### **Transpiler**

The transpiler tests are in the directory `src/test/transpiler_test_files`.

To execute the tests, there are a few steps to follow:
1. Select a test to run from the directory.
1. Transpile the Python code following the [Use Manual](##use-manual) for the selected test.
1. Compile and execute the transpiled code following the [Use Manual](##use-manual).
1. Execute the desired test in Python with the following command, where `(path_to_test)` corresponds to the path of the desired test:

    python (path_to_test)

1. Finally, compare both outputs.

*Note*: the sets and dictionaries in C++ are stored in a different order than Python. Hence, differences in the output regarding this order are not alarming.


## Credits
+ Luis David Solano Santamaría
+ Angie Solís Manzano
+ Emilia Víquez Mora