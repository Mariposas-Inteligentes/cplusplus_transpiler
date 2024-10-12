# **C++ Transpiler**

Transpiler from a Python subset of instructions to C++ implemented using the PLY library.

## **Dependencies**

To use the project certain packages are required.

To install them you can run the following command in your terminal:

``` bash
pip install -r requirements.txt
```

## **Use manual**

To use the transpiler itself, you can execute the following command from the `src` directory:

``` bash
python main.py <file_name>
```

Where `<file_name>` corresponds to a file with the following characteristics:

1. The file must have a `.py` extension.
2. The file must exist.

For now, this will output the tokens read from the file and any error detected. In the case of errors it will report any incorrect tokens detected or indentation. 

## **Unit tests**

To run the all of the unit tests (except for the parsing one), you can execute the following command from the `src/tests` directory:

``` bash
python -m pytest
```

In case of wanting to run a specific test, you can execute the following command:

``` bash
python -m pytest <file_name>
```

In the case of parsing test, in order to run it, you need to be in the src folder and run the command:

``` bash
python .\tests\test_parsing.py
```


## Credits
+ Luis David Solano Santamaría
+ Angie Solís Manzano
+ Emilia Víquez Mora