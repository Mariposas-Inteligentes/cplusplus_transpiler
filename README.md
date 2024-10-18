# **C++ Transpiler**

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
python main.py <file_name> <debug>
```

Where `<file_name>` corresponds to an obligatory parameter and a file with the following characteristics:

1. The file must have a `.py` extension.
2. The file must exist.

And `<debug>` corresponds to an optional parameter, if set to the string `"debug"` it will print out PLY's debbuging mecanisms.

### **Execution example**

An execution example can be done with the file [test_valid_case.py](src/tests/parser_test_files/test_valid_case.py)

``` bash
python main.py tests/parser_test_files/test_valid_case.py
```

To run it in debug mode you can do so the following way:

``` bash
python main.py tests/parser_test_files/test_valid_case.py debug
```

## **Unit tests**

### **Lexer**

To run the unit tests for the lexer, the pytest module is utilized.

To execute all tests once, you must be in the `src/tests/lexer_test_files` directory and run the following command:

``` bash
python -m pytest
```

In case of wanting to run a specific test, you can execute the following command:

``` bash
python -m pytest <file_name>
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


## Credits
+ Luis David Solano Santamaría
+ Angie Solís Manzano
+ Emilia Víquez Mora