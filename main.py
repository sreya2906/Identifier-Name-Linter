import sys
import os
import enchant
import re
from github import Github, Repository, ContentFile
from tree_sitter import Language, Parser, Node

from git.repo.base import Repo

if not os.path.exists("./Language-Implementations/tree-sitter-python"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-python", "./Language-Implementations/tree-sitter-python")
if not os.path.exists("./Language-Implementations/tree-sitter-javascript"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-javascript", "./Language-Implementations/tree-sitter-javascript")
if not os.path.exists("./Language-Implementations/tree-sitter-ruby"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-ruby", "./Language-Implementations/tree-sitter-ruby")
if not os.path.exists("./Language-Implementations/tree-sitter-go"):
    Repo.clone_from("https://github.com/tree-sitter/tree-sitter-go", "./Language-Implementations/tree-sitter-go")

Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  [
    'Language-Implementations/tree-sitter-javascript',
    'Language-Implementations/tree-sitter-python',
    'Language-Implementations/tree-sitter-go',
    'Language-Implementations/tree-sitter-ruby'
  ]
)

JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
PY_LANGUAGE = Language('build/my-languages.so', 'python')
GO_LANGUAGE = Language('build/my-languages.so', 'go')
RB_LANGUAGE = Language('build/my-languages.so', 'ruby')

identifier_list = ''
identifiers_with_violation_list = ''
dictionary = enchant.Dict("en_US")
allowed_short_identifiers = ["c", "d", "e", "g", "i", "in", "inOut", "j", "k", "m", "n", "o", "out", "t", "x", "y", "z"]
valid_number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
                      "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
                      "thirty", "fourty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand",
                      "million", "billion", "trillion"]


def read_git_file(content_file: ContentFile, file_extension: str):
    if content_file.name.endswith(file_extension):
        parse_file(content_file)


def read_git_folder(repo: Repository, path: str, file_extension: str):
    for contentFile in repo.get_contents(path):
        if contentFile.type == "dir":
            read_git_folder(repo, contentFile.path, file_extension)
        else:
            read_git_file(contentFile, file_extension)


def read_git_repo(repo_name: str):
    if len(repo_name.split('github.com/')) > 1:
        repo_name = repo_name.split('github.com/')[1]
    g = Github("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")
    try:
        repo = g.get_repo(repo_name)
    except:
        print("GIT Repo not found")
        sys.exit()
    read_git_folder(repo, "", sys.argv[2])



def write_to_file(path: str, file_name: str, file_content: str):
    filepath = os.path.join(path, file_name)
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(filepath):
        os.remove(filepath)
    with open(filepath, 'x') as f:
        f.write(file_content)


def create_parser(file_extension: str, lang: str) -> Parser:
    new_parser = Parser()
    if lang.lower() == "python" and file_extension.lower() == ".py":
        new_parser.set_language(PY_LANGUAGE)
    elif lang.lower() == "javascript" and file_extension.lower() == ".js":
        new_parser.set_language(JS_LANGUAGE)
    elif lang.lower() == "go" and file_extension.lower() == ".go":
        new_parser.set_language(GO_LANGUAGE)
    elif lang.lower() == "ruby" and file_extension.lower() == ".rb":
        new_parser.set_language(RB_LANGUAGE)
    else:
        print("Language or File Extension Combination Not Supported")
        sys.exit()
    return new_parser


def get_tuple_string(point: tuple) -> str:
    return "(" + str(point[0]) + ":" + str(point[1]) + ")"


def get_identifier_data(file_content_string: str, node: Node, path: str) -> str:
    return "Identifier_String=" + "'" + file_content_string[node.start_byte: node.end_byte] + "'"\
           + ",\tFile_Path And_Name=" + "'" + path + "'"\
           + ", \tStart_Point=" + "'" + get_tuple_string(node.start_point) + "'"\
           + ", \tEnd_Point=" + "'" + get_tuple_string(node.end_point) + "'" + "\n\n"


def get_violation_data_for_identifier(identifier_string: str) -> str:
    violation_data = ''
    identifier_string_split_by_underscore = identifier_string.split('_')
    identifier_string_split_by_underscore = [parsed_string for parsed_string in identifier_string_split_by_underscore if
                                             len(parsed_string) > 0]
    identifier_string_split_by_casing = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', identifier_string)
    identifier_string_split_by_casing = [parsed_string for parsed_string in identifier_string_split_by_casing if
                                             len(parsed_string) > 0]

    # Check Dictionary Violation
    if not dictionary.check(identifier_string):
        violation_data = violation_data + "\tDictionary_Words_Violation"

    # Check Consecutive Underscores Violation
    if identifier_string.find('__') != -1:
        violation_data = violation_data + "\tConsecutive_Underscores_Violation"

    # Check External Underscores Violation
    if identifier_string.startswith('_') or identifier_string.endswith('_'):
        violation_data = violation_data + "\tExternal_Underscores_Violation"

    # Check Naming Convention Anomaly Exception
    if len(identifier_string_split_by_underscore) > 1 \
            and not (all((len(parsed_string) == 0 or parsed_string.islower())
                         for parsed_string in identifier_string_split_by_underscore)
                     or all((len(parsed_string) == 0 or parsed_string.isupper())
                            for parsed_string in identifier_string_split_by_underscore)):
        violation_data = violation_data + "\tNaming_Convention_Anomaly_Violation"

    # Check Excessive Words Violation (Camel/Pascal case words and Words with underscores)
    if len(identifier_string_split_by_underscore) > 4 or len(identifier_string_split_by_casing) > 4:
        violation_data = violation_data + "\tExcessive_Words_Violation"

    # Number Of Words Violation (Camel/Pascal case words and Words with underscores)
    if (len(identifier_string_split_by_underscore) == 1 or len(identifier_string_split_by_underscore) > 4)\
            or (len(identifier_string_split_by_casing) == 1 or len(identifier_string_split_by_casing) > 4):
        violation_data = violation_data + "\tNumber_Of_Words_Violation"

    # Check Long Identifier Name Violation
    if len(identifier_string) > 20:
        violation_data = violation_data + "\tLong_Identifier_Name_Violation"

    # Check Short Identifier Name Violation
    if len(identifier_string) < 8 and identifier_string not in allowed_short_identifiers:
        violation_data = violation_data + "\tShort_Identifier_Name_Violation"

    # Check Numeric Identifier Name Violation
    if identifier_string.isnumeric() \
            or (len(identifier_string_split_by_underscore)
                and all(parsed_string.lower() in valid_number_words
                        for parsed_string in identifier_string_split_by_underscore)) \
            or (len(identifier_string_split_by_casing)
                and all(parsed_string.lower() in valid_number_words
                        for parsed_string in identifier_string_split_by_casing)):
        violation_data = violation_data + "\tNumeric_Identifier_Name_Violation"

    return violation_data


def get_identifier_violation_data(file_content_string: str, node: Node, path: str) -> str:
    identifier_string = file_content_string[node.start_byte: node.end_byte]
    if not len(identifier_string) > 0:
        return ''
    violation_data = get_violation_data_for_identifier(identifier_string)
    if len(violation_data) > 0:
        return "Identifier_String=" + "'" + identifier_string + "'"\
               + ",\tFile_Path And_Name=" + "'" + path + "'"\
               + ", \tStart_Point=" + "'" + get_tuple_string(node.start_point) + "'" \
               + ", \tEnd_Point=" + "'" + get_tuple_string(node.end_point) + "'" \
               + ", \tRules_Violated=" + "'" + violation_data + "'" + "\n\n"
    else:
        return ''


def get_all_identifiers_from_file(node: Node, file_content_string: str, path: str):
    global identifier_list
    global identifiers_with_violation_list
    if node.child_count > 0:
        for child_node in node.children:
            get_all_identifiers_from_file(child_node, file_content_string, path)
    else:
        if node.type == "identifier":
            identifier_list = identifier_list + get_identifier_data(file_content_string, node, path)
            identifiers_with_violation_list = \
                identifiers_with_violation_list + get_identifier_violation_data(file_content_string, node, path)


def parse_file(file_content: ContentFile):
    tree = parser.parse(file_content.decoded_content)
    get_all_identifiers_from_file(tree.root_node, file_content.decoded_content.decode(), file_content.path)


# total arguments
n = len(sys.argv)

# Name of python script itself is counted as one argument
if n != 6:
    print("Please pass following 5 arguments: Name of GIT Repo, File Extension, Programming Language, File Output "
          "Path 1, File Output Path 2")
    sys.exit()

parser = create_parser(sys.argv[2], sys.argv[3])
read_git_repo(sys.argv[1])
write_to_file(sys.argv[4], "output1.txt", identifier_list)
write_to_file(sys.argv[5], "output2.txt", identifiers_with_violation_list)
