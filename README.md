# Identifier-Name-Linter

### Pre-Requisites:
* C-compiler is installed on the machine
* Python 3.x is installed on the machine and added to Environment Path variable


### Project Set-Up:
* Clone this GITHub project from this [link](https://github.com/sreya2906/Identifier-Name-Linter)
* Open the project in PyCharm and set up appropriate Virtual Environment by following this [link](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env).
* If PyCharm or any other IDE is not used, then set up the Virtual Environment by using steps from this [link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) 

### Program Set-Up:
* PyCharm automatically downloads all required Python Library dependencies once Virtual Environment is set up. If libraries are installed, then we can skip the below steps of Program Set-Up Section
* If the libraries are not installed, then please follow below steps:
* Once project set up is done, run the `setup.py` file with `develop` as parameter. Refer below for sample code:
    ```
    python setup.py develop
            or
    ${path-to-python.exe} ${path-to-main.py} develop
            or
    Right click setup.py in PyCharm -> Modify Run Configurations -> Add 'develop' in parameters -> Save Configurations -> Run setup.py
    ```
* After successful completion of the above step, all the Python Library dependencies will be resolved.

### Executing / Testing the program:

The program expects following parameters as command-line arguments (in the same sequence):
* GITHub repo URL (Eg: tree-sitter/tree-sitter-ruby or https://github.com/tree-sitter/tree-sitter-ruby)
* File Extension (Supported Values: .py, .js, .rb, .go)
* Programming Language Name (Supported Values: python, javascript, ruby, go)
* Path for output1.txt (Eg: output/identifiers)
* Path for output2.txt (Eg: output/identifiers-with-violations)

Use the following command as a reference:
```
python main.py tree-sitter/tree-sitter-ruby .rb ruby output/identifiers output/identifiers-with-errors
            or
${path-to-python.exe} ${path-to-main.py} ${path-to-git-repo} ${file-extension} ${programming-language-name} ${path-for-output1} ${path-for-output-2}
            or
Right click main.py in PyCharm -> Modify Run Configurations -> Add all required parameters -> Save Configurations -> Run main.py
```

> The first run takes few extra seconds to complete as it clones all the required tree_sitter language parsers. This step is not repeated in consecutive runs. 


### Verifying the Output files:
* `output1.txt` and `output2.txt` file will be generated at the respective paths specified while running main.py
* `output1.txt` will contain following information of all identifiers in the GIT repo: *Identifier string, File Location, Start Point(Line-Number: Character-Number) and End Point(Line-Number: Character-Number)*
* `output2.txt` will contain following information of all identifiers with naming convention violation in the GIT repo: *Identifier string, File Location, Start Point(Line-Number: Character-Number), End Point(Line-Number: Character-Number) and List of Violations*
* Sample outputs have been uploaded in this Repo in the folder with name 'output'
