import re
from pathlib import Path
from collections import deque
from io import StringIO

# Matches keys and values, with or without quotes, separated by any whitespace
KEY_PAIR_PATTERN = re.compile(r'(?:"([^"]*)"|([^"\s]+))\s+(?:"([^"]*)"|([^"\s]+))')

# Matches a table name, with or without quotes
TABLE_NAME_PATTERN = re.compile(r'(?:"([^"]*)"|([^"\s]+))')

class ImproperTableFormatException:

    def __init__(self, message):
        super().__init__(message)

class ValveTableParser:

    def __init__(self, filepath: Path, mode = "r"):
        self.__filepath = filepath.resolve()
        self.__mode = mode
        self.__file = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    def __enter__(self):
        if 'w' in self.__mode:
            self.__filepath.parent.mkdir(parents=True, exist_ok=True)
        self.__file = open(self.__filepath, self.__mode, encoding="utf-8")
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.__file:
            self.__file.close()
            self.__file = None
    
    def load(self) -> tuple[str, dict]:
        '''
        Load a Valve Table file, returning the name and dictionary.

        :raises RuntimeError: RuntimeError raised if file is unopened.
        :raises ImproperTableFormatException: ImproperTableFormatException raised if table is of improper format.
        :return: _description_
        :rtype: tuple[str, dict]
        '''
        if self.__file is None:
            raise RuntimeError("Cannot read an unopened Valve Table File")
        if not self.__file.readable():
            raise RuntimeError("Opened Valve Table File is not readable.")
        name = None
        root_table = {}
        current_table = None
        next_table_name = None
        table_stack = deque()
        for line in self.__file:
            line = line.split("//")[0].strip()
            if not line:
                continue

            if not line or line.startswith("//"):
                continue

            if line == "{":
                if next_table_name is None:
                    raise ImproperTableFormatException("Encountered '{' without a preceding table name.")
                # If we haven't encountered a table yet, we need to setup root table
                if current_table is None:
                    name = next_table_name
                    current_table = root_table
                else:
                    current_table[next_table_name] = {}
                    table_stack.append(current_table)
                    current_table = current_table[next_table_name]
                next_table_name = None
            elif line == "}":
                if current_table is None:
                    raise ImproperTableFormatException("Encountered '}' without a preceding '{'.")
                if not table_stack:
                    current_table = None
                else:
                    current_table = table_stack.pop()
            else:
                key_pair_match = KEY_PAIR_PATTERN.fullmatch(line)
                if key_pair_match:
                    # Grab the first non-None group for key, and the first non-None for value
                    groups = key_pair_match.groups()
                    entry_key = groups[0] or groups[1]
                    entry_value = groups[2] or groups[3]
                    current_table[entry_key] = entry_value
                else:
                    table_name_match = TABLE_NAME_PATTERN.fullmatch(line)
                    if table_name_match:
                        groups = table_name_match.groups()
                        next_table_name = groups[0] or groups[1]
        return (name, root_table)
    
    def loads(self):
        name, data = self.load()
        return ValveTableParser.parse(name, data)

    def dump(self, name: str, data: dict):
        if self.__file is None:
            raise RuntimeError("Cannot write to an unopened Valve Table File.")
        if not self.__file.writable():
            raise RuntimeError("Opened Valve Table File is not writeable.")
        file_contents = ValveTableParser.parse(name, data)
        self.__file.write(file_contents)
    
    @staticmethod
    def parse(name: str, data: dict):
        stringstream = StringIO("")
        ValveTableParser.__parse_node(stringstream, name, data, depth=0)
        return stringstream.getvalue()
    
    @staticmethod
    def __parse_node(sstream: StringIO, name: str, data: dict, depth: int):

        indent = '\t' * depth

        sstream.write(f'{indent}"{str(name)}"\n')
        sstream.write(f'{indent}{{\n')

        for key, value in data.items():
            if isinstance(value, dict):
                ValveTableParser.__parse_node(sstream, key, value, depth+1)
            else:
                sstream.write(f'{indent}\t"{str(key)}"\t\t"{str(value)}"\n')

        sstream.write(f'{indent}}}\n')
