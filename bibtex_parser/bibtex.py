import re


# Unicode combining symbols
combining_symbols = {
    "\\`": u"\u0300",  # Grave accent (`)
    "\\'": u"\u0301",  # Acute accent (´)
    "\\^": u"\u0302",  # Circumflex (ˆ)
    "\\~": u"\u0303",  # Tilde (~)
    "\\=": u"\u0304",  # Macron (ˉ)
    "\\u": u"\u0306",  # Breve (˘)
    "\\.": u"\u0307",  # Dot above (˙)
    '\\"': u"\u0308",  # Diaeresis (¨)
    "\\H": u"\u030b",  # Double acute accent (´´)
    "\\r": u"\u030a",  # Ring above (˚)
    "\\v": u"\u030c",  # Caron (ˇ)
    "\\d": u"\u0323",  # Dot below (.)
    "\\c": u"\u0327",  # Cedilla (¸)
    "\\b": u"\u0331",  # Macron below (_)
    "\\t": u"\u0361",  # Double inverted breve (two args required) (⌒)
}

inverted_combining_symbols = {
    v.encode("utf-8").decode("utf-8"): k for k, v in combining_symbols.items()
}

# Special symbols in LaTeX
special_latex_symbols = {
    "\\\\": "\n",
    "\\ ": " ",
    "\\,": " ",
    "\\;": " ",
    "\\:": " ",
    "\\!": "",
    "~": " ",
    "\\quad": "    ",
    "\\qquad": "        ",
    "\\$": "$",
    "\\&": "&",
    "\\%": "%",
    "\\#": "#",
    "\\_": "_",
    "\\textasciitilde": u"\u02dc",  # Raised tilde
    "\\textasciicircum": "^",
    # "\\textbackslash": "\\",
    "\\textless": "<",
    "\\textgreater": ">",
    "\\oe": u"\u0153",  # Ligature oe
    "\\ae": u"\xe6",  # Ligature ae
    "\\aa": u"a\u030a",  # a followed by a combining symbols \u030a
    "\\AA": u"A\u030a",  # A followed by a combining symbols \u030a
    "\\AE": u"\xc6",  # Ligature AE
    "\\OE": u"\u0152",  # Ligature OE
    "\\o": u"\xf8",  # o with stroke
    "\\O": u"\xd8",  # O with stroke
    "\\l": u"\u0142",  # l with stroke
    "\\ss": u"\xdf",  # Sharp s
    "\\SS": "SS",  # Sharp S
    "\\i": u"\u0131",  # Latin small letter dotless i
    "\\j": u"\u0237",  # Latin small letter dotless j
    "\\ij": "ij",
    "\\IJ": "IJ",
    '\\"{\\i}': u"\xef",
    "?`": u"\xbf",  # Inverted question mark
    "!`": u"\xa1",  # Inverted exclamation mark
}

# Unicode symbols representing combining characters
unicode_symbol_to_combining_code = {
    u"`": "\\`",  # Grave accent (`)
    u"\xb4": "\\'",  # Acute accent (´)
    u"\u02c6": "\\^",  # Circumflex (ˆ)
    u"\u02dc": "\\~",  # Tilde (~)
    u"\xaf": "\\=",  # Macron (ˉ)
    u"\u02d8": "\\u",  # Breve (˘)
    u"\u02d9": "\\.",  # Dot above (˙)
    u"\xa8": '\\"',  # Diaeresis (¨)
    u"\u02dd": "\\H",  # Double acute accent (´´)
    u"\u02da": "\\r",  # Ring above (˚)
    u"\u02c7": "\\v",  # Caron (ˇ)
    u"\xb8": "\\c",  # Cedilla (¸)
}

# Unicode character encoding patterns to LaTeX code
char_encoding_to_code = {
    r"_": r"\_",
    r"\\xe6": r"{\\ae}",  # Ligature ae
    r"\\u0153": r"{\\oe}",  # Ligature oe
    r"\\xc6": r"{\\AE}",  # Ligature AE
    r"\\u0152": r"{\\OE}",  # Ligature OE
    r"\\xf8": r"{\\o}",  # o with stroke
    r"\\xd8": r"{\\O}",  # O with stroke
    r"\\u0142": r"{\\l}",  # l with stroke
    r"\\xdf": r"{\\ss}",  # Sharp s
    r"\\u0131": r"{\\i}",  # Latin small letter dotless i
    r"\\u0237": r"{\\j}",  # Latin small letter dotless j
    r"(\w)\\u0300": "\\`\\1",  # Grave accent
    r"(\w)\\u0301": "\\'\\1",  # Acute accent
    r"(\w)\\u0302": "\\^\\1",  # Circumflex
    r"(\w)\\u0303": "\\~\\1",  # Tilde
    r"(\w)\\u0304": "\\=\\1",  # Macron
    r"(\w)\\u0306": "\\u{\\1}",  # Breve
    r"(\w)\\u0307": "\\.\\1",  # Dot above
    r"(\w)\\u0308": '\\"\\1',  # Diaeresis
    r"(\w)\\u030b": "\\H{\\1}",  # Double acute accent
    r"(\w)\\u030a": "\\r{\\1}",  # Ring above
    r"(\w)\\u030c": "\\v{\\1}",  # Caron
    r"(\w)\\u0323": "\\d{\\1}",  # Dot below
    r"(\w)\\u0327": "\\c{\\1}",  # Cedilla
    r"(\w)\\u0331": "\\b{\\1}",  # Macron below
    r"(\w)\\u0361": "\\t{\\1}",  # Double inverted breve (two args required)
    r"\\xe0": "\\`a",  # Latin small letter a with grave `
    r"\\xe1": "\\'a",  # Latin small letter a with acute ´
    r"\\xe2": "\\^a",  # Latin small letter a with circumflex ^
    r"\\xe3": "\\~a",  # Latin small letter a with tilde ~
    r"\\xe4": '\\"a',  # Latin small letter a with diaeresis ¨
    r"\\xe5": r"\\r{a}",  # Latin small letter a with ring above
    r"\\xe8": "\\`e",  # Latin small letter e with grave `
    r"\\xe9": "\\'e",  # Latin small letter e with acute ´
    r"\\xea": "\\^e",  # Latin small letter e with circumflex ^
    r"\\xeb": '\\"e',  # latin small letter e with diaeresis ¨
    r"\\xec": "\\`i",  # Latin small letter i with grave `
    r"\\xed": "\\'i",  # Latin small letter i with acute ´
    r"\\xee": "\\^i",  # Latin small letter i with circumflex ^
    r"\\xef": r'\\"{\\i}',  # Latin small letter i with diaeresis ¨
    r"\\xf1": "\\~n",  # Latin small letter n with tilde ~
    r"\\xf2": "\\`o",  # Latin small letter o with grave `
    r"\\xf3": "\\'o",  # Latin small letter o with acute ´
    r"\\xf4": "\\^o",  # Latin small letter o with circumflex ^
    r"\\xf5": "\\~o",  # Latin small letter o with tilde ~
    r"\\xf6": '\\"o',  # Latin small letter o with diaeresis ¨
    r"\\xf9": "\\`u",  # Latin small letter u with grave `
    r"\\xfa": "\\'u",  # Latin small letter u with acute ´
    r"\\xfb": "\\^u",  # Latin small letter u with circumflex ^
    r"\\xfc": '\\"u',  # Latin small letter u with diaeresis ¨
    r"\\xfd": "\\'y",  # Latin small letter y with acute ´
    r"\\xff": '\\"y',  # Latin small letter y with diaeresis ¨
    r"\\xc0": "\\`A",  # Latin capital letter A with grave `
    r"\\xc1": "\\'A",  # Latin capital letter A with acute ´
    r"\\xc3": "\\~A",  # Latin capital letter A with tilde ~
    r"\\xc4": '\\"A',  # Latin capital letter A with diaeresis ¨
    r"\\xc5": r"\\r{A}",  # Latin capital letter A with ring above
    r"\\xc2": "\\^A",  # Latin capital letter A with circumflex ^
    r"\\xc8": "\\`E",  # Latin capital letter E with grave `
    r"\\xc9": "\\'E",  # Latin capital letter E with acute ´
    r"\\xca": "\\^E",  # Latin capital letter E with circumflex ^
    r"\\xcb": '\\"E',  # Latin capital letter E with diaeresis ¨
    r"\\xcc": "\\`I",  # Latin capital letter I with grave `
    r"\\xcd": "\\'I",  # Latin capital letter I with acute ´
    r"\\xce": "\\^I",  # Latin capital letter I with circumflex ^
    r"\\xcf": '\\"I',  # Latin capital letter I with diaeresis ¨
    r"\\xd1": "\\~N",  # Latin capital letter N with tilde ~
    r"\\xd2": "\\`O",  # Latin capital letter O with grave `
    r"\\xd3": "\\'O",  # Latin capital letter O with acute ´
    r"\\xd4": "\\^O",  # Latin capital letter O with circumflex ^
    r"\\xd5": "\\~O",  # Latin capital letter O with tilde ~
    r"\\xd6": '\\"O',  # Latin capital letter O with diaeresis ¨
    r"\\xd9": "\\`U",  # Latin capital letter U with grave `
    r"\\xda": "\\'U",  # Latin capital letter U with acute ´
    r"\\xdb": "\\^U",  # Latin capital letter U with circumflex ^
    r"\\xdc": '\\"U',  # Latin capital letter U with diaeresis ¨
    r"\\xdd": "\\'Y",  # Latin capital letter Y with acute ´
}

punctuation_encoding_to_code = {
    r"\\xbf": "?`",  # Inverted question mark
    r"\\xa1": "!`",  # Inverted exclamation mark
    "&": "\\&",
    "%": "\\%",
    "#": "\\#",
    "$": "\\$",
    "^": "\\textasciicircum{}",
    "<": "\\textless{}",
    ">": "\\textgreater{}",
}

predefined_string = {
    "icassp": "Proc. IEEE ICASSP",
    # "icassp": "Proc. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)",
    "interspeech": "Proc. ISCA Interspeech",
    # "interspeech": "Annual Conference of the International Speech Communication Association (Interspeech)",
    "asru": "Proc. IEEE ASRU",
    # "asru": "Proc. IEEE Workshop on Automatic Speech Recognition and Understanding (ASRU)",
    "slt": "Proc. IEEE SLT",
    # "slt": "Proc. IEEE Spoken Language Technology Workshop (SLT)",
    "ieee-taslp": "IEEE Trans. Audio, Speech, Language Process.",
    # "ieee-taslp": "IEEE Transactions on Audio, Speech, and Language Processing",
    "ieee-acm-taslp": "IEEE/ACM Trans. ASLP.",
    # "ieee-acm-taslp": "IEEE/ACM Transactions on Audio, Speech and Language Processing",
    "mlsp": "Proc. International Workshop on Machine Learning for Signal Processing (MLSP)",
    # "mlsp": "Proc. MLSP",
    "nips": "Proc. NIPS",
    # "nips": "Proc. Conference on Neural Information Processing Systems (NIPS)",
    "csl": r"Computer Speech \& Language",
    # "csl": "Comput. Speech Lang.",
    "lrec": "Proc. International Conference on Language Resources and Evaluation (LREC)",
    # "lrec": "Proc. LREC",
    "icml": "Proc. ICML",
    # "icml": "Proc. International Conference on Machine Learning (ICML)",
    "acl": "Proc. ACL",
    # "acl": "Proc. Annual Meeting of the Association for Computational Linguistics (ACL)",
    "naacl": "Proc. NAACL",
    # "naacl": "Proc. Conference of the North {A}merican Chapter of the Association for Computational Linguistics (NAACL)",
    "emnlp": "Proc. EMNLP",
    # "emnlp": "Proc. Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    "waspaa": "Proc. IEEE WASPAA",
    "eusipco": "Proc. IEEE EUSIPCO",
}


def remove_brace_pair(string):
    """Remove all paired braces from the input string.
    
    Note: \{ and \} are ignored for the special grammar in LaTeX.
    """
    pattern = r'(^\{|(?<=[^\\])\{|(?<=[^\\])\})'
    left_brace_pos = []
    left_brace = False
    split_parts = re.split(pattern, string)
    for i, part in enumerate(split_parts):
        if len(part) == 0:
            continue
        if part == '{':
            left_brace = True
            left_brace_pos.append(i)
        elif part == '}' and left_brace:
            split_parts[left_brace_pos.pop(-1)] = ''
            split_parts[i] = ''
            left_brace = len(left_brace_pos) != 0
    return ''.join(split_parts)


def remove_redundant_brace_pair(string, keep_inner=True):
    """Remove all nested paired braces from the input string.
    
    Note: \{ and \} are ignored for the special grammar in LaTeX.

    Args:
        string (str): input string
        keep_inner (bool): If True, only keep the paired braces nested inside;
                           If False, only keep the outside paired braces.
    """
    pattern = r'(^\{|(?<=[^\\])\{|(?<=[^\\])\})'
    brace_pairs = []
    left_brace_pos = []
    left_brace = False
    split_parts = re.split(pattern, string)
    for i, part in enumerate(split_parts):
        if len(part) == 0:
            continue
        if part == '{':
            left_brace = True
            left_brace_pos.append(i)
        elif part == '}' and left_brace:
            pos = left_brace_pos.pop(-1)
            left_brace = len(left_brace_pos) != 0
            if keep_inner:
                brace_pairs.append((pos, i))
            elif left_brace:
                split_parts[pos] = ''
                split_parts[i] = ''
    if keep_inner:
        brace_pairs = sorted(brace_pairs)
        for idx, (left, right) in enumerate(brace_pairs):
            for l, r in brace_pairs:
                if left < l and r < right:
                    split_parts[left] = ''
                    split_parts[right] = ''
                    break
                elif l > right:
                    break
    return ''.join(split_parts)


def parse_author_list(string):
    """Parse the author list with various formats.

    Args:
        string (str): input string containing the author list in the beginning
    Returns:
        authors (List[Tuple(First name + Middle name, Last name)]): list of authors
        rest (str): remaining part of string
    """
    # import pudb
    # pudb.set_trace()
    string_new = string.strip().replace(u"\u2013", "-").replace(u"\u2014", "-")
    if string_new == "":
        return [], ""
    if string_new[0] == "{":
        # {author list}
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == "{" and string_new[i - 1] != "\\":
                count += 1
            elif string_new[i] == "}" and string_new[i - 1] != "\\":
                count -= 1
            if count == 0:
                author_list_str = string_new[1:i].strip()
                rest = string_new[i + 1 :].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for {...}
            raise ValueError("Invalid author list {...")

    elif string_new[0] == '"':
        # "author list"
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == '"' and string_new[i - 1] != "\\":
                author_list_str = string_new[1:i].strip()
                rest = string_new[i + 1 :].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for "..."
            raise ValueError('Invalid author list "..."')

    else:
        raise ValueError("Invalid author list string")

    match = re.match(r".*and\s+others", author_list_str)
    if match:
        # ignore any content after "and others"
        # and remove the leading comma before "and others"
        author_list_str = re.sub(r"\s*,\s*and\s+others", " and others", match.group())

    # three possible formats:
    #   1. Last_name1, {First_name1} and Last_name2, First_name2 and others
    #   2. First_name1 {Last_name1} and First_name2 Last_name2 and others
    #   3. mix of 1. and 2.
    authors = []
    if re.search(r"([^\\]|^)\{\s*\}", author_list_str):
        raise ValueError('Empty content "{ }" in author list')
    author_list = author_list_str.split("and")
    for author_name in author_list:
        author_name = author_name.strip()
        if author_name == "":
            continue
        if "," in author_name:
            last_name, first_name = author_name.split(",")
            last_name = re.sub(r"^\s*\{(.*)?\}\s*$", "\\1", last_name).strip()
            first_name = re.sub(r"^\s*\{(.*)?\}\s*$", "\\1", first_name).strip()
        elif (
            author_name[0] == "{"
            and author_name[-1] == "}"
            and not re.search(r"^\{|[^\\]\{|[^\\]\}", author_name[1:-1])
        ):
            # ... and {xxx yyy} and ...
            lst = author_name[1:-1].split()
            first_name = " ".join(lst[:-1])
            last_name = lst[-1]
        else:
            # ... and zzz {xxx yyy} and ...
            # ... and xxx yyy and ...
            if author_name[-1] == "}" and author_name[-2] != "\\":
                count = 1
                for idx in range(len(author_name) - 2, -1, -1):
                    # from len(author_name)-2 to 0
                    if author_name[idx] == "{" and (
                        idx == 0 or author_name[idx - 1] != "\\"
                    ):
                        count -= 1
                    elif author_name[idx] == "}" and (
                        idx == 0 or author_name[idx - 1] != "\\"
                    ):
                        count += 1
                    if count == 0:
                        last_name = re.sub(r'\s+', ' ', remove_brace_pair(author_name[idx:]).strip())
                        first_name = re.sub(r'\s+', ' ', remove_brace_pair(author_name[:idx]).strip())
                        break
                else:
                    raise ValueError("Invalid author list ...}")
            else:
                if " " in author_name:
                    lst = author_name.split()
                    first_name = " ".join(lst[:-1])
                    last_name = lst[-1]
                else:
                    first_name = author_name
                    last_name = ""
                    # raise ValueError('Invalid author name: %s' % author_name)

        if first_name == "":
            raise ValueError("Invalid empty name")
        if last_name == "":
            authors.append((first_name,))
        else:
            authors.append((first_name, last_name))

    return authors, rest


def parse_number_range(string):
    """Parse the number / number range.

    Args:
        string (str): input string containing the bib-style number range
    Returns:
        number_range (int or Tuple[int, int] or str or None): number / number range
        rest (str): remaining part of string
    """
    string_new = string.strip()
    if string_new == "":
        return None, ""
    if string_new[0] == "{":
        # {xxx--yyy} or {xxx}
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == "{" and string_new[i - 1] != "\\":
                count += 1
            elif string_new[i] == "}" and string_new[i - 1] != "\\":
                count -= 1
            if count == 0:
                number_range_str = string_new[1:i].strip()
                rest = string_new[i + 1 :].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for {...}
            raise ValueError("Invalid number range {...")

        if re.search(r"[^\\]\{|[^\\]\}", number_range_str):
            # remove all paired {}
            count = 0
            new_str = ""
            for i, c in enumerate(number_range_str):
                if c == "{" and (i == 0 or number_range_str[i - 1] != "\\"):
                    count += 1
                elif c == "}" and (i == 0 or number_range_str[i - 1] != "\\"):
                    count -= 1
                else:
                    new_str += c
            assert count == 0
            number_range_str = new_str.strip()

        if number_range_str == "":
            number_range = None
        else:
            match = re.match(r"\s*(\d+)\s*-+\s*(\d+)\s*|\s*(\d+)\s*", number_range_str)
            if match:
                n1, n2, n3 = match.groups()
                if n1 is None and n2 is None and n3 is not None:
                    number_range = int(n3)
                elif n1 is not None and n2 is not None and n3 is None:
                    number_range = (int(n1), int(n2))
                    if number_range[0] > number_range[1]:
                        print(
                            'Warning: "%d--%d" may be a wrong number range!'
                            % number_range
                        )
                else:
                    raise ValueError("Invalid match for number range")
            else:
                raise ValueError("No matched number range: {xxx--yyy} or {xxx}")

    elif string_new[0] == '"':
        # "xxx--yyy" or "xxx" or "{xxx--yyy}" or "{xxx}"
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == '"' and string_new[i - 1] != "\\":
                number_range_str = string_new[1:i].strip()
                rest = string_new[i + 1 :].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for "..."
            raise ValueError('Invalid author list "..."')

        if re.search(r"[^\\]\{|[^\\]\}", number_range_str):
            # remove all paired {}
            count = 0
            new_str = ""
            for i, c in enumerate(number_range_str):
                if c == "{" and (i == 0 or number_range_str[i - 1] != "\\"):
                    count += 1
                elif c == "}" and (i == 0 or number_range_str[i - 1] != "\\"):
                    count -= 1
                else:
                    new_str += c
            assert count == 0
            number_range_str = new_str.strip()

        if number_range_str == "":
            number_range = None
        else:
            match = re.match(r"\s*(\d+)\s*-+\s*(\d+)\s*|\s*(\d+)\s*", number_range_str)
            if match:
                n1, n2, n3 = match.groups()
                if n1 is None and n2 is None and n3 is not None:
                    number_range = int(n3)
                elif n1 is not None and n2 is not None and n3 is None:
                    number_range = (int(n1), int(n2))
                    if number_range[0] > number_range[1]:
                        print(
                            'Warning: "%d--%d" may be a wrong number range!'
                            % number_range
                        )
                else:
                    raise ValueError("Invalid match for number range")
            else:
                raise ValueError('No matched number range: "xxx--yyy" or "xxx"')

    elif re.match(r"\d", string_new[0]):
        # number
        match = re.search(r"^(\d+)\s*(?:,|$)", string_new)
        if match:
            number_range = int(match.group(1))
            rest = string_new[match.end() :]
        else:
            raise ValueError("Invalid number range xxx")

    elif re.match(r"\w", string_new[0]):
        # predefined_string
        for i in range(1, len(string_new)):
            if re.match(r"[^-\w]", string_new[i]):
                number_range = string_new[:i].strip()
                rest = string_new[i:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            number_range = string_new
            rest = ""

        if number_range not in predefined_string:
            print('Warning: "%s" is not defined in `predefined_string`!' % number_range)
        # for distinguishing the predefined string
        number_range = "#" + number_range
    else:
        raise ValueError("Invalid number range string")

    return number_range, rest


def parse_string(string):
    """Parse the bib-style string field.

    Args:
        string (str): input string containing the bib-style string
    Returns:
        ret_str (str): parsed string field
        rest (str): remaining part of string
    """
    string_new = string.strip()
    if string_new == "":
        return "", ""
    if string_new[0] == "{":
        # {xxx}
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == "{" and string_new[i - 1] != "\\":
                count += 1
            elif string_new[i] == "}" and string_new[i - 1] != "\\":
                count -= 1
            if count == 0:
                ret_str = re.sub(r"\s+", " ", string_new[1:i].strip())
                rest = string_new[i + 1 :].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for {...}
            raise ValueError("Invalid string {...")

    elif string_new[0] == '"':
        # "xxx"
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == '"' and string_new[i - 1] != "\\":
                ret_str = re.sub(r"\s+", " ", string_new[1:i].strip())
                rest = string_new[i + 1 :].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for "..."
            raise ValueError('Invalid string "..."')

    elif re.match(r"\w", string_new[0]):
        # predefined_string
        for i in range(1, len(string_new)):
            if re.match(r"[^-\w]", string_new[i]):
                ret_str = string_new[:i].strip()
                rest = string_new[i:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            ret_str = string_new
            rest = ""

        if ret_str not in predefined_string:
            print('Warning: "%s" is not defined in `predefined_string`!' % ret_str)
        # for distinguishing the predefined string
        ret_str = "#" + ret_str
    else:
        raise ValueError("Invalid string")

    return remove_redundant_brace_pair(ret_str), rest


def get_raw_text(string, not_change_letter_case=False):
    """Convert the input BibTeX style string to plain text.

    Args:
        string (str): input string
        not_change_letter_case (bool): True: keep the original letter case in `string`
                                             (e.g. for author names)
                                       False: auto capitalize a word-initial at the
                                             beginning or after a colon
    Returns:
        ret_str (str): processed plain text
    """
    string_new = re.sub(r"\s+", " ", string.strip())
    if string_new.startswith("#"):
        return predefined_string.get(string[1:], "UNDEFINED")
    while "\\" in string_new:
        # replace all LaTeX special symbols with Unicode characters
        for pattern in special_latex_symbols:
            string_new = string_new.replace(pattern, special_latex_symbols[pattern])
        if "\\" not in string_new:
            break

        for pattern in combining_symbols:
            if pattern not in string_new:
                continue
            ptn = re.escape(pattern)
            if re.match(r"\w", pattern[-1]):
                # should be separated from its modified character by a non-word char
                # or any {}-wrapped string
                ptn2 = "(" + ptn + r"\{\s*[^\s\}]*\s*\}|" + ptn + r"[^\{\w])"
            else:
                # any non-{ character or {}-wrapped string
                ptn2 = "(" + ptn + r"\{\s*[^\s\}]*\s*\}|" + ptn + r"[^\{])"
            new_str = ""
            end = 0
            for match in re.finditer(ptn2, string_new):
                if match.start() > end:
                    new_str += string_new[end : match.start()]
                end = match.end()
                count, wrapped = 0, False
                is_modified_word = False
                match_str = ""
                for c in match.group()[2:]:
                    if c == "{":
                        count += 1
                        wrapped = True
                        match_str += c
                    elif c == "}":
                        count -= 1
                        wrapped = count != 0
                        match_str += c
                    elif re.match(r"\s", c) and wrapped and not is_modified_word:
                        continue
                    elif not is_modified_word:
                        is_modified_word = True
                        match_str += c + combining_symbols[pattern]
                    else:
                        match_str += c

                assert count == 0, count
                new_str += match_str
            string_new = new_str + string_new[end:]
        break

    if re.search(r"([^\\]|^)\{", string_new):
        # remove all paired {}
        count = 0
        new_str = ""
        wrapped = False
        for i, c in enumerate(string_new):
            if c == "{" and (i == 0 or string_new[i - 1] != "\\"):
                count += 1
                wrapped = True
            elif c == "}" and (i == 0 or string_new[i - 1] != "\\"):
                count -= 1
                wrapped = count != 0
            elif re.match(r"\w", c):
                if not_change_letter_case or wrapped:
                    new_str += c
                elif i == 0:
                    new_str += c.upper()
                elif string_new[i - 1] == ":" or (
                    string_new[i - 1] == " " and string_new[i - 2 : i - 1] == ":"
                ):
                    new_str += c
                else:
                    new_str += c.lower()
            else:
                new_str += c.lower()
        assert count == 0, count
        string_new = new_str.strip()
    elif not_change_letter_case:
        string_new = string_new.strip()
    else:
        new_str = ""
        for i, c in enumerate(string_new):
            if re.match(r"\w", c):
                if i == 0:
                    new_str += c.upper()
                elif string_new[i - 1] == ":" or (
                    string_new[i - 1] == " " and string_new[i - 2 : i - 1] == ":"
                ):
                    new_str += c
                else:
                    new_str += c.lower()
            else:
                new_str += c.lower()
        string_new = new_str.strip()
    return string_new


def raw_string_to_bib_style(string, handle_letter_case=False):
    """Convert the plain text to a bib-style string.

    Args:
        string (str): input plain text
        handle_letter_case (bool): True: auto wrap upper- or mixed-case words with {}
                                   False: use the original letter case in `string`
    Returns:
        ret_str (str): bib-style string
    """
    string = re.sub(r"\s+", " ", string.strip())
    string_lst = []
    for c in string:
        if c in inverted_combining_symbols and len(string_lst) > 0:
            string_lst[-1] = string_lst[-1] + c
        else:
            string_lst.append(c)
    length = len(string_lst)
    ret_str = []

    prev_char = ""
    word_str = ""
    is_word = False
    bracket_wrapped = False
    symbol_wrapped = False
    for i, c in enumerate(string_lst):
        if re.match(r"[-\w]", c, flags=re.UNICODE):
            if c == "-":
                word_str += "-"
            elif c == u"\u2013":
                word_str += "--"
            elif c == u"\u2014":
                word_str += "---"
            else:
                if not bracket_wrapped:
                    bracket_wrapped = (
                        handle_letter_case
                        and c.isupper()
                        and prev_char not in ("", ":")
                    )
                c_encoding = c.encode("ascii", "backslashreplace").decode("ascii")
                for ptn, to_ptn in char_encoding_to_code.items():
                    match = re.match(ptn, c_encoding)
                    if match:
                        c = re.sub(ptn, to_ptn, c_encoding)
                        break
                word_str += c

            if symbol_wrapped:
                word_str += "}"
                symbol_wrapped = False

            is_word = True
            if i == length - 1:
                if bracket_wrapped:
                    ret_str.append("{%s}" % word_str)
                else:
                    ret_str.append(word_str)
        else:
            if c == u"\x7f":
                continue
            end_of_word = c not in unicode_symbol_to_combining_code
            if end_of_word:
                c_str = punctuation_encoding_to_code.get(c, c)
            else:
                # special character
                symbol_wrapped = True
                c_str = unicode_symbol_to_combining_code[c] + "{"
            if is_word:
                if end_of_word:
                    if bracket_wrapped:
                        ret_str.append("{%s}" % word_str)
                    else:
                        ret_str.append(word_str)
                    ret_str.append(c_str)
                    word_str = ""
                    is_word = bracket_wrapped = False
            else:
                ret_str.append(c_str)
        prev_char = c
    return "".join(ret_str)


class BibTeXEntry:
    """BibTeX entry parser that converts a bib string into a manageable object,
    which can be converted back into bib string or plain text as well.
    """

    def __init__(self, bibstring, indent=2):
        # tags including 'title' and 'author'
        self.tags = {}
        self.type = "unknown"
        self.name = "notdefined"
        self.indent = indent
        if len(bibstring) > 0:
            self.__parse_string(bibstring)
        self.__preferred_order = (
            "title",
            "author",
            "booktitle",
            "journal",
            "volume",
            "number",
            "pages",
            "year",
            "organization",
            "publisher",
        )

    def __repr__(self):
        return str(self)

    def __str__(self):
        """Normalize the string by:
        - Removing leading and trailing whitespace
        - Removing empty lines
        - Merging a multi-line field into a single line
        - Replacing kw="XXX" with kw={XXX}
        - Ordering the fields
        """
        keys = self.__preferred_order + tuple(
            k for k in self.tags.keys() if k not in self.__preferred_order
        )
        space = " " * self.indent
        s = "@{}{{{},\n".format(self.type, self.name)
        for k in keys:
            if k not in self.tags:
                continue
            if k == "author":
                authors_str = " and ".join(
                    [", ".join(name[-1:] + name[:-1]) for name in self.tags[k]]
                )
                s += "{}{}={{{}}},\n".format(space, k, authors_str)
            elif k in ("volume", "number", "pages", "year"):
                number_range = self.tags[k]
                if number_range is None:
                    num_str = ""
                elif isinstance(number_range, tuple):
                    num_str = "{}--{}".format(number_range[0], number_range[1])
                elif isinstance(number_range, int):
                    num_str = str(number_range)
                else:
                    raise ValueError(
                        "Unexpected value for {}: {}".format(k, number_range)
                    )
                if num_str.startswith("#"):
                    s += "{}{}={},\n".format(space, k, num_str[1:])
                else:
                    s += "{}{}={{{}}},\n".format(space, k, num_str)
            else:
                string = self.tags[k]
                if string.startswith("#"):
                    s += "{}{}={},\n".format(space, k, string[1:])
                else:
                    s += "{}{}={{{}}},\n".format(space, k, string)
        return s + "}"

    def __parse_string(self, string):
        string_new = string.strip()
        for k, v in {"\b": "\\b", "\r": "\\r", "\t": "\\t", "\v": "\\v"}.items():
            if k in string_new:
                string_new = string_new.replace(k, v)
        if re.match(r'''[^\\]'|"''', string_new):
            print(
                "WARNING: potential special characters \\' and \\\" are not handled.\n"
                "Please escape them manually (if applicable) by using \\\\' and \\\\\"."
            )

        # 1st line: @pub_type{entry_name,
        assert string_new.startswith("@") and string_new.endswith("}")
        first_line, rest = string_new[:-1].split(",", maxsplit=1)
        # self.type: publication type
        # self.name: entry name/label
        self.type, self.name = re.search(r"^@(\w+)\{([^,\s]+)", first_line).groups()
        self.type = self.type.lower()

        # following lines:
        #   field_name = {value},
        #   field_name=    value,
        #   field_name = "value",
        while True:
            rest = rest.strip()
            if rest == "":
                break
            tag_name, rest = rest.split("=", maxsplit=1)
            keyword = tag_name.strip().lower()
            assert keyword not in self.tags, keyword
            if keyword == "author":
                # parse author list
                value, rest = parse_author_list(rest)
            elif keyword in ("volume", "number", "pages", "year"):
                # parse number / number range
                value, rest = parse_number_range(rest)
            else:
                # parse string
                value, rest = parse_string(rest)

            self.tags[keyword] = value

    def to_plaintext(self, style="IEEEtran"):
        """Render the reference string in IEEE style.

        Reference:
            https://www.bibtex.com/s/bibliography-style-ieeetran-ieeetran/

        Args:
            style (str): render in IEEE style: IEEEtran or IEEEbib
        Returns:
            string (str): plain reference string
        """
        if style in ("IEEEbib", "IEEEtran"):
            # APA-like style
            string = ""
            authors = self.tags["author"]
            num_authors = len(authors)
            for i, names in enumerate(authors):
                if len(names) == 1 or names[1] == "":
                    name_str = get_raw_text(names[0], not_change_letter_case=True)
                    if name_str == "others":
                        name_str = "et al."
                else:
                    first_name = get_raw_text(names[0], not_change_letter_case=True)
                    last_name = get_raw_text(names[1], not_change_letter_case=True)
                    if style == "IEEEbib":
                        name_str = first_name + " " + last_name
                    elif style == "IEEEtran":
                        first_name_abbr = re.sub(
                            r"(\s*-?\w)[^-\s]*", "\\1.", first_name
                        )
                        name_str = first_name_abbr + " " + last_name
                if i == num_authors - 2:
                    if authors[-1] == ("others",):
                        string += name_str + " "
                    else:
                        string += name_str + ", and "
                else:
                    string += name_str + ", "

            title = get_raw_text(self.tags["title"])
            year = self.tags["year"]
            if isinstance(year, str):
                year = get_raw_text(year)

            if self.type == "article":
                pub = get_raw_text(self.tags["journal"], not_change_letter_case=True)
                vol_num_pages = ""
                for key in ("volume", "number", "pages"):
                    if self.tags.get(key, None) is None:
                        continue
                    if key == "volume":
                        volume = self.tags[key]
                        if isinstance(volume, str):
                            volume = get_raw_text(volume)
                        vol_num_pages += "vol. {}, ".format(volume)
                    elif key == "number":
                        number = self.tags[key]
                        if isinstance(number, str):
                            number = get_raw_text(number)
                        vol_num_pages += "no. {}, ".format(number)
                    elif key == "pages":
                        pages = self.tags[key]
                        if isinstance(pages, str):
                            pages = re.sub(r"-+", u"\u2013", get_raw_text(pages))
                        elif isinstance(pages, tuple):
                            pages = "{}\u2013{}".format(pages[0], pages[1])
                        vol_num_pages += "pp. {}, ".format(pages)
                if vol_num_pages == "":
                    string += u"\u201c{},\u201d {}, {}.".format(title, pub, year)
                else:
                    string += u"\u201c{},\u201d {}, {}{}.".format(
                        title, pub, vol_num_pages, year
                    )
            elif self.type == "inproceedings":
                pub = get_raw_text(self.tags["booktitle"], not_change_letter_case=True)
                pages = ""
                for key in ("pages",):
                    if self.tags.get(key, None) is None:
                        continue
                    if key == "pages":
                        pages = self.tags[key]
                        if isinstance(pages, str):
                            pages = "pp. " + re.sub(
                                r"-+", u"\u2013", get_raw_text(pages)
                            )
                        elif isinstance(pages, tuple):
                            pages = "pp. {}\u2013{}".format(pages[0], pages[1])
                        else:
                            pages = "pp. {}".format(pages)
                if pages == "":
                    string += u"\u201c{},\u201d in {}, {}.".format(title, pub, year)
                else:
                    string += u"\u201c{},\u201d in {}, {}, {}.".format(
                        title, pub, year, pages
                    )
            else:
                raise ValueError("Unsupported publication type: %s" % self.type)
        else:
            raise ValueError("Unsupported style: %s" % style)
        return string

    @staticmethod
    def plaintext_to_bibtex(plaintext, default_type="article"):
        """Convert the reference string in IEEE style (APA-like) to BibTeXEntry.

        Args:
            plaintext (str): input plain reference string
            default_type (str): default publication type
                used when the publication type cannot be guessed from `plaintext`
        Returns:
            bibtex (BibTeX): parsed BibTeXEntry object
        """
        bib = BibTeXEntry("")
        string = re.sub(r"\s+", " ", plaintext.strip())
        # convert unicode comma/colon to ascii comma/colon
        string = string.replace(u"\uff0c", ",").replace(u"\uff1a", ":")
        if string.endswith("."):
            # remove the trailing period
            string = string[:-1]
        if re.search(
            u"\u201c" + r".*,\s*" + u"\u201d", string, flags=re.UNICODE
        ) or re.search(r'".*,\s*"', string):
            # possibly a paper or technical report
            if string.startswith(u"\u201c"):
                # “title,” publisher, ...
                pass
            elif string.startswith('"'):
                # "title," publisher, ...
                pass
            else:
                # authors, “title,” publisher, ...
                quotation_mark_type = "unicode"
                match = re.search(r"^(.*?),\s*" + u"\u201c", string, flags=re.UNICODE)
                if not match:
                    quotation_mark_type = "ascii"
                    match = re.search(r'^([^"]*?),\s*"', string)
                    if not match:
                        raise ValueError(
                            "Invalid reference string: "
                            "No author list before title is detected!"
                        )
                authors = match.group(1).strip()
                authors = re.sub(r"et al\.", ", et al.", authors)
                assert len(authors) > 0
                # parse author list (add necessary {} pairs)
                #  - abbreviated names can be followed by a period, and possibly not
                split_authors = [
                    it.strip() for it in re.split(",|and", authors) if it.strip() != ""
                ]
                lst_authors = []
                for i, author in enumerate(split_authors):
                    if author == "et al." and i == len(split_authors) - 1:
                        lst_authors.append(("others",))
                    else:
                        names = author.split()
                        first_name = raw_string_to_bib_style(
                            " ".join(names[:-1]).strip()
                        )
                        last_name = raw_string_to_bib_style(names[-1])
                        lst_authors.append((first_name, last_name))
                bib.tags["author"] = lst_authors

                string = string[match.end() - 1 :]
                if quotation_mark_type == "unicode":
                    match = re.search(
                        u"^\u201c" + r"\s*([^" + u"\u201d]*)" + r"\s*,\s*" + u"\u201d",
                        string,
                        flags=re.UNICODE,
                    )
                else:
                    match = re.search(r'^"\s*([^"]*)\s*,\s*"', string)
                if not match:
                    raise ValueError(
                        "Invalid reference string: No title is detected "
                        'with quotation_mark_type="{}"!'.format(quotation_mark_type)
                    )
                title = match.group(1)
                # parse title (add necessary {} pairs); replace unicode chars with code
                bib.tags["title"] = raw_string_to_bib_style(
                    title, handle_letter_case=True
                )

                booktitle, rest = string[match.end() :].strip().split(",", maxsplit=1)
                booktitle = booktitle.strip()
                if re.search(r"journal|transactions|arxiv", booktitle, re.IGNORECASE):
                    bib.type = "article"
                elif re.search(
                    r"conference|proc\.|proc|proceedings", booktitle, re.IGNORECASE
                ):
                    bib.type = "inproceedings"
                    booktitle = re.sub(r"in\s+", "", booktitle, re.IGNORECASE)

                adjacent_to_publisher = True
                string = "".join(rest).strip()
                for item in string.split(","):
                    item = (
                        item.strip().replace(u"\u2013", "--").replace(u"\u2014", "---")
                    )

                    match = re.match(
                        r"(?:vol\.|vol|volumn)\s*(\d+)", item, re.IGNORECASE
                    )
                    if match:
                        bib.tags["volume"] = int(match.group(1))
                        adjacent_to_publisher = False
                        continue

                    match = re.match(r"(?:no\.|no|number)\s*(\d+)", item, re.IGNORECASE)
                    if match:
                        bib.tags["number"] = int(match.group(1))
                        adjacent_to_publisher = False
                        continue

                    match = re.match(
                        r"(?:pp\.|pp|page|pages)\s*([-\d]+)", item, re.IGNORECASE
                    )
                    if match:
                        bib.tags["pages"] = parse_number_range("{%s}" % match.group(1))[
                            0
                        ]
                        adjacent_to_publisher = False
                        continue

                    if re.match("\d{4}", item):
                        bib.tags["year"] = int(item)
                        adjacent_to_publisher = False
                        continue

                    if adjacent_to_publisher:
                        booktitle += ", %s" % item

                if bib.type == "article":
                    bib.tags["journal"] = raw_string_to_bib_style(booktitle)
                elif bib.type == "inproceedings":
                    bib.tags["booktitle"] = raw_string_to_bib_style(booktitle)

                # Determine the entry name based on title, author, and year
                word_lst = bib.tags["title"].split()
                word = word_lst[0].capitalize()
                for w in word_lst:
                    if not re.match("a|an|as|at|by|for|in|on|to", w, re.IGNORECASE):
                        word = w.capitalize().replace("-", "")
                        break
                ffname = bib.tags.get("author", [("Unknown",)])[0][-1].capitalize()
                year = bib.tags.get("year", 0)
                bib.name = "%s-%s%d" % (word, ffname, year)
        else:
            # possibly a book or technical report
            # e.g. "aaa bbb, ccc ddd, and xxx yyy, Title of the book, booktitle, year."
            lst = string.split(",")
            assert len(lst) >= 3, lst

        return bib
