"""The toktab file was the assembly source for the token table.
This was to read it, parse it, and output python structures to
represent the data required from it.
This was a script used in the production of amosTokens.py.
"""
from __future__ import print_function
from re import match, search
from amosTokens import token_map


def capitalize_all(line):
    """Amos has a habit of capitalizing the first letter of all words in a statement."""
    words = line.split(" ")
    words = [word.capitalize() for word in words]
    return " ".join(words)


def process_similar(new_pairs):
    """Some entries were the same words, but with prefixes - so as to be different tokens.
    These often represent different uses of the same word, or variations on a
    function - overloading"""
    in_repeat = None
    for address, name, orig in new_pairs:
        if name.startswith('"!'):
            name = name.replace("!", "")
            in_repeat = name
        elif in_repeat and name.startswith("$80"):
            name = in_repeat
        else:
            in_repeat = None
        yield (address, name, orig)


def get_tokens(lines):

    lines = (line for line in lines if not line.startswith('*'))  # kill comments
    lines = (line.strip() for line in lines)  # kill rubbish around lines
    lines = [line for line in lines if line]  # kill blank lines
    lines = [line for line in lines if not match("[A-Za-z_][A-Za-z0-9_]*:", line)]  # kill labels
    #Pair up the lines
    il = iter(lines)
    line_pairs = zip(il, il)
    # Condition the address lines
    line_pairs = [(line_pair[0].replace("FFFFF", "F"), line_pair[1], line_pair) for line_pair in line_pairs]
    line_pairs = [(line_pair[0][:4].split('+')[0], line_pair[1], line_pair[2]) for line_pair in line_pairs]
    #line_pairs = [(int(address, 16), name) for address, name in line_pairs]
    # Filter out tokens without names
    non_tokens = [(address, name, orig) for address, name, orig in line_pairs if '"' not in name or "$80" not in name]
    new_pairs = [line_pair for line_pair in line_pairs if line_pair[:2] not in non_tokens]
    # Start to condition the names
    #   Clear stuff before the dc
    new_pairs = [(address, name.partition("dc.b")[2].strip(), orig) for address, name, orig in new_pairs]
    new_pairs = list(process_similar(new_pairs))
    new_pairs = [(address, name, orig) for address, name, orig in new_pairs if int(address, 16) not in token_map]
    #  split at the $80
    new_pairs = [( address, name.partition("$80")[0], orig) for address, name, orig in new_pairs]
    #  Drop the comma in the middle of names
    new_pairs = [( address, name.replace('","', ""), orig) for address, name, orig in new_pairs]
    #extract the name from the line
    new_pairs = [(address, search('".+"', name).group(0), orig) for address, name, orig in new_pairs]
    new_pairs = [(address, name.strip('"'), orig) for address, name, orig in new_pairs]
#    #Capitalize the name (as Amos does)
    new_pairs = [(address, capitalize_all(name), orig) for address, name, orig in new_pairs]
    return lines, new_pairs, non_tokens


def convert_to_dict(new_pairs):
    new_pairs = [(int(address, 16), name) for address, name, orig in new_pairs]
    token_map.update(new_pairs)
    pair_list = [(key, token_map[key]) for key in token_map]
    pair_list = sorted(pair_list, key=lambda item: item[0])
    for key, value in pair_list:
        if isinstance(value, tuple):
            value = (value[0], value[1].func_name)
            print("0x%04x: ('%s', %s)," % (key, value[0], value[1]))
        else:
            print("0x%04x: %s," % (key, repr(value)))


if __name__ == '__main__':
    with open("toktabparsed.txt") as fd:
        lines, new_pairs, non_tokens = get_tokens(fd.readlines())
    convert_to_dict(new_pairs)