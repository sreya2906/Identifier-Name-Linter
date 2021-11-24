# Identifier-Name-Linter

### Pre-requisities:
* C-compiler is installed on the machine
* Python 3.x is installed on the machine and added to Environment Path variable


### Project Set-Up:
* Clone this GIThub project from this [link](https://github.com/sreya2906/Identifier-Name-Linter)
* Open the project in PyCharm and set up appropriate Virtual Environment.
* If PyCharm or any other IDE is not used, then set up the Virtual Environment by using steps from this [link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) 

### Program Set-Up:
* Once project set up is done, run the `setup.py` file with `develop` as parameter. Refer below for sample code:
    `python setup.py develop`
            or
    *'path-to-python.exe' 'path-to-main.py' develop*
* After successful completion of the above step, all the GIT Repo dependencies and Python Library dependencies will be resolved.

### Executing / Testing the program:
Use the following command as a reference:

`python main.py tree-sitter/tree-sitter-ruby .rb ruby output\identifiers output\identifiers-with-errors`
or
*'path-to-python.exe' 'path-to-main.py' 'path-to-git-repo' 'file-extension' 'programming-language-name' 'path-for-output1' 'path-for-output-2'*

### Verifying the Output files:
* `output1.txt` and `output2.txt` file will be generated at the respective paths specified while running main.py
* `output1.txt` will contain following information of all identifiers in the GIT repo: *Identifier string, File Location, Start Point(Line-Number: Character-Number) and End Point(Line-Number: Character-Number)*
* `output2.txt` will contain following information of all identifiers with naming convention violation in the GIT repo: *Identifier string, File Location, Start Point(Line-Number: Character-Number), End Point(Line-Number: Character-Number) and List of Violations*
