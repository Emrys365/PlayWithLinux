#!/usr/bin/env python3
import re


combining_symbols = {
    '\\`': u'\u0300',   # Grave accent
    "\\'": u'\u0301',   # Acute accent
    '\\^': u'\u0302',   # Circumflex
    '\\~': u'\u0303',   # Tilde
    '\\=': u'\u0304',   # Macron
    '\\u': u'\u0306',   # Breve
    '\\.': u'\u0307',   # Dot above
    '\\"': u'\u0308',   # Diaeresis
    '\\H': u'\u030b',   # Double acute accent
    '\\r': u'\u030a',   # Ring above
    '\\v': u'\u030c',   # Caron
    '\\d': u'\u0323',   # Dot below
    '\\c': u'\u0327',   # Cedilla
    '\\b': u'\u0331',   # Macron below
    '\\t': u'\u0361',   # Double inverted breve (two args required)
}

special_symbols = {
    '\\\\': '\n',
    '\\ ':  ' ',
    '\\,':  ' ',
    '\\;':  ' ',
    '\\:':  ' ',
    '\\!':  '',
    '~':  ' ',
    '\\quad': '    ',
    '\\qquad': '        ',
    '\\&':  '&',
    '\\%':  '%',
    '\\#':  '#',
    '\\oe': u'\u0153',  # Ligature oe
    '\\ae': u'\xe6',    # Ligature ae
    '\\aa': u'a\u030a', # a followed by a combining symbols \u030a
    '\\AA': u'A\u030a', # A followed by a combining symbols \u030a
    '\\AE': u'\xc6',    # Ligature AE
    '\\o':  u'\xf8',    # o with stroke
    '\\O':  u'\xd8',    # O with stroke
    '\\l':  u'\u0142',  # l with stroke
    '\\ss': u'\xdf',    # Sharp s
    '?`':   u'\xbf',    # Inverted question mark
    '!`':   u'\xa1',    # Inverted exclamation mark
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
    "csl": "Computer Speech \& Language",
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


def parse_author_list(string):
    """Parse the author list with various formats

    Args:
        string (str): input string containing the author list in the beginning
    Returns:
        authors (List[Tuple(First name + Middle name, Last name)]): list of authors
        rest (str): remaining part of string
    """
    string_new = string.strip()
    if string_new == "":
        return [], ""
    if string_new[0] == "{":
        # {author list}
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == "{" and string_new[i-1] != "\\":
                count += 1
            elif string_new[i] == "}" and string_new[i-1] != "\\":
                count -= 1
            if count == 0:
                author_list_str = string_new[1:i].strip()
                rest = string_new[i+1:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for {...}
            raise ValueError('Invalid author list {...')

    elif string_new[0] == '"':
        # "author list"
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == '"' and string_new[i-1] != "\\":
                author_list_str = string_new[1:i].strip()
                rest = string_new[i+1:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for "..."
            raise ValueError('Invalid author list "..."')

    else:
        raise ValueError('Invalid author list string')

    match = re.match(r'.*and\s+others', author_list_str)
    if match:
        # ignore any content after "and others"
        # and remove the leading comma before "and others"
        author_list_str = re.sub(r'\s*,\s*and\s+others', ' and others', match.group())

    # three possible formats:
    #   1. Last_name1, {First_name1} and Last_name2, First_name2 and others
    #   2. First_name1 {Last_name1} and First_name2 Last_name2 and others
    #   3. mix of 1. and 2.
    authors = []
    if re.search(r'([^\\]|^)\{\s*\}', author_list_str):
        raise ValueError('Empty content "{ }" in author list')
    author_list = author_list_str.split('and')
    for author_name in author_list:
        author_name = author_name.strip()
        if author_name == "":
            continue
        if ',' in author_name:
            last_name, first_name = author_name.split(',')
            last_name = re.sub(r"^\s*\{(.*)?\}?\s*$", "{\\1}", last_name).strip()
            first_name = re.sub(r"^\s*\{(.*)?\}\s*$", "{\\1}", first_name).strip()
        elif author_name[0] == "{" and author_name[-1] == "}" and not re.search(r'^\{|[^\\]\{|[^\\]\}', author_name[1:-1]):
            # ... and {xxx yyy} and ...
            lst = author_name[1:-1].split()
            first_name = " ".join(lst[:-1])
            last_name = lst[-1]
        else:
            # ... and zzz {xxx yyy} and ...
            # ... and xxx yyy and ...
            if author_name[-1] == "}" and author_name[-2] != "\\":
                count = 1
                for idx in range(len(author_name)-2, -1, -1):
                    # from len(author_name)-2 to 0
                    if author_name[idx] == "{" and (
                        idx == 0
                        or author_name[idx-1] != "\\"
                    ):
                        count -= 1
                    elif author_name[idx] == "}" and (
                        idx == 0
                        or author_name[idx-1] != "\\"
                    ):
                        count += 1
                    if count == 0:
                        last_name = " ".join(author_name[idx:].split())
                        first_name = " ".join(author_name[:idx].split())
                        break
                else:
                    raise ValueError('Invalid author list ...}')
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
            raise ValueError('Invalid empty name')
        if last_name == "":
            authors.append((first_name,))
        else:
            authors.append((first_name, last_name))

    return authors, rest


def parse_number_range(string):
    """Parse the number / number range

    Args:
        string (str): input string containing the author list in the beginning
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
            if string_new[i] == "{" and string_new[i-1] != "\\":
                count += 1
            elif string_new[i] == "}" and string_new[i-1] != "\\":
                count -= 1
            if count == 0:
                number_range_str = string_new[1:i].strip()
                rest = string_new[i+1:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for {...}
            raise ValueError('Invalid number range {...')

        if re.search(r'[^\\]\{|[^\\]\}', number_range_str):
            # remove all paired {}
            count = 0
            new_str = ""
            for i, c in enumerate(number_range_str):
                if c == "{" and (i == 0 or number_range_str[i-1] != "\\"):
                    count += 1
                elif c == "}" and (i == 0 or number_range_str[i-1] != "\\"):
                    count -= 1
                else:
                    new_str += c
            assert count == 0
            number_range_str = new_str.strip()

        if number_range_str == "":
            number_range = None
        else:
            match = re.match(r'\s*(\d+)\s*-+\s*(\d+)\s*|\s*(\d+)\s*', number_range_str)
            if match:
                n1, n2, n3 = match.groups()
                if n1 is None and n2 is None and n3 is not None:
                    number_range = int(n3)
                elif n1 is not None and n2 is not None and n3 is None:
                    number_range = (int(n1), int(n2))
                    if number_range[0] > number_range[1]:
                        print('Warning: "%d--%d" may be a wrong number range!' % number_range)
                else:
                    raise ValueError('Invalid match for number range')
            else:
                raise ValueError('No matched number range: {xxx--yyy} or {xxx}')

    elif string_new[0] == '"':
        # "xxx--yyy" or "xxx" or "{xxx--yyy}" or "{xxx}"
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == '"' and string_new[i-1] != "\\":
                number_range_str = string_new[1:i].strip()
                rest = string_new[i+1:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for "..."
            raise ValueError('Invalid author list "..."')

        if re.search(r'[^\\]\{|[^\\]\}', number_range_str):
            # remove all paired {}
            count = 0
            new_str = ""
            for i, c in enumerate(number_range_str):
                if c == "{" and (i == 0 or number_range_str[i-1] != "\\"):
                    count += 1
                elif c == "}" and (i == 0 or number_range_str[i-1] != "\\"):
                    count -= 1
                else:
                    new_str += c
            assert count == 0
            number_range_str = new_str.strip()

        if number_range_str == "":
            number_range = None
        else:
            match = re.match(r'\s*(\d+)\s*-+\s*(\d+)\s*|\s*(\d+)\s*', number_range_str)
            if match:
                n1, n2, n3 = match.groups()
                if n1 is None and n2 is None and n3 is not None:
                    number_range = int(n3)
                elif n1 is not None and n2 is not None and n3 is None:
                    number_range = (int(n1), int(n2))
                    if number_range[0] > number_range[1]:
                        print('Warning: "%d--%d" may be a wrong number range!' % number_range)
                else:
                    raise ValueError('Invalid match for number range')
            else:
                raise ValueError('No matched number range: "xxx--yyy" or "xxx"')

    elif re.match(r'\d', string_new[0]):
        # number
        match = re.search(r'^(\d+)\s*(?:,|$)', string_new)
        if match:
            number_range = int(match.group(1))
            rest = string_new[match.end():]
        else:
            raise ValueError('Invalid number range xxx')

    elif re.match(r'\w', string_new[0]):
        # predefined_string
        for i in range(1, len(string_new)):
            if re.match(r'[^-\w]', string_new[i]):
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
        raise ValueError('Invalid number range string')

    return number_range, rest


def parse_string(string):
    """Parse the string field

    Args:
        string (str): input string containing the author list in the beginning
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
            if string_new[i] == "{" and string_new[i-1] != "\\":
                count += 1
            elif string_new[i] == "}" and string_new[i-1] != "\\":
                count -= 1
            if count == 0:
                ret_str = re.sub(r'\s+', ' ', string_new[1:i].strip())
                rest = string_new[i+1:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for {...}
            raise ValueError('Invalid author list {...')

    elif string_new[0] == '"':
        # "xxx"
        count = 1
        for i in range(1, len(string_new)):
            if string_new[i] == '"' and string_new[i-1] != "\\":
                ret_str = re.sub(r'\s+', ' ', string_new[1:i].strip())
                rest = string_new[i+1:].strip()
                assert rest == "" or rest[0] == ",", rest
                if rest != "":
                    rest = rest[1:].strip()
                break
        else:
            # no match for "..."
            raise ValueError('Invalid author list "..."')

    elif re.match(r'\w', string_new[0]):
        # predefined_string
        for i in range(1, len(string_new)):
            if re.match(r'[^-\w]', string_new[i]):
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
        raise ValueError('Invalid author list string')

    return ret_str, rest


def get_raw_text(string, not_change_letter_case=False):
    """Convert the input BibTeX style string to plain text

    Args:
        string (str): input string
        not_change_letter_case (bool): True: keep the original letter case in `string`
                                             (e.g. for author names)
                                       False: auto capitalize a word-initial at the beginning
                                             or after a colon
    Returns:
        ret_str (str): processed plain text
    """
    string_new = re.sub(r'\s+', ' ', string.strip())
    if string_new.startswith("#"):
        return predefined_string.get(string[1:], "UNDEFINED")
    while '\\' in string_new:
        # replace all LaTeX special symbols with Unicode characters
        for pattern in special_symbols:
            string_new = string_new.replace(pattern, special_symbols[pattern])
        if "\\" not in string_new:
            break
        for pattern in combining_symbols:
            if pattern not in string_new:
                continue
            ptn = re.escape(pattern)
            if re.match(r'\w', pattern[-1]):
                # should be separated from its modified character by a non-word character
                # or any {}-wrapped string
                ptn2 = '(' + ptn + r'\{\s*[^\s\}]*\s*\}|' + ptn + r'[^\{\w])'
            else:
                # any non-{ character or {}-wrapped string
                ptn2 = '(' + ptn + r'\{\s*[^\s\}]*\s*\}|' + ptn + r'[^\{])'
            new_str = ""
            start, end = 0, 0
            for match in re.finditer(ptn2, string_new):
                if match.start() > end:
                    new_str += string_new[end:match.start()]
                start, end = match.start(), match.end()
                count, wrapped = 0, False
                is_modified_word = False
                match_str = ""
                for c in match.group()[2:]:
                    if c == '{':
                        count += 1
                        wrapped = True
                        match_str += c
                    elif c == '}':
                        count -= 1
                        wrapped = count != 0
                        match_str += c
                    elif re.match(r'\s', c) and wrapped and not is_modified_word:
                        continue
                    elif not is_modified_word:
                        is_modified_word = True
                        match_str += (c + combining_symbols[pattern])
                    else:
                        match_str += c

                assert count == 0, count
                new_str += match_str
            string_new = new_str + string_new[end:]
        break

    if re.search(r'([^\\]|^)\{', string_new):
        # remove all paired {}
        count = 0
        new_str = ""
        wrapped = False
        for i, c in enumerate(string_new):
            if c == "{" and (i == 0 or string_new[i-1] != "\\"):
                count += 1
                wrapped = True
            elif c == "}" and (i == 0 or string_new[i-1] != "\\"):
                count -= 1
                wrapped = count != 0
            elif re.match(r'\w', c):
                if not_change_letter_case or wrapped:
                    new_str += c
                elif i == 0:
                    new_str += c.upper()
                elif string_new[i-1] == ":" or (string_new[i-1] == " " and string_new[i-2:i-1] == ":"):
                    new_str += c.upper()
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
            if re.match(r'\w', c):
                if i == 0:
                    new_str += c.upper()
                elif string_new[i-1] == ":" or (string_new[i-1] == " " and string_new[i-2:i-1] == ":"):
                    new_str += c.upper()
                else:
                    new_str += c.lower()
            else:
                new_str += c.lower()
        string_new = new_str.strip()
    return string_new


class BibTeXEntry:
    def __init__(self, bibstring, indent=2):
        # tags including 'title' and 'author'
        self.tags = {}
        self.indent = indent
        self.__parse_string(bibstring)
        self.__preferred_order = (
            'title',
            'author',
            'booktitle',
            'journal',
            'volume',
            'number',
            'pages',
            'year',
            'organization',
            'publisher',
        )

    def __repr__(self):
        return str(self)

    def __str__(self):
        '''Normalize the string by:
         - Removing leading and trailing whitespace
         - Removing empty lines
         - Merging a multi-line field into a single line
         - Replacing kw="XXX" with kw={XXX}
         - Ordering the fields
        '''
        keys = tuple(k for k in self.tags.keys() if k not in self.__preferred_order) + self.__preferred_order
        space = ' ' * self.indent
        s = '@{}{{{},\n'.format(self.type, self.name)
        for k in keys:
            if k not in self.tags:
                continue
            if k == "author":
                authors_str = " and ".join([", ".join(name) for name in self.tags[k]])
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
                    raise ValueError('Unexpected value for {}: {}'.format(k, number_range))
                if num_str.startswith('#'):
                    s += "{}{}={},\n".format(space, k, num_str[1:])
                else:
                    s += "{}{}={{{}}},\n".format(space, k, num_str)
            else:
                string = self.tags[k]
                if string.startswith('#'):
                    s += "{}{}={},\n".format(space, k, string[1:])
                else:
                    s += "{}{}={{{}}},\n".format(space, k, string)
        return s + "}"

    def __parse_string(self, string):
        string_new = string.strip()

        # 1st line: @pub_type{entry_name,
        assert string_new.startswith("@") and string_new.endswith("}")
        first_line, rest = string_new[:-1].split(",", maxsplit=1)
        # self.type: publication type
        # self.name: entry name/label
        self.type, self.name = re.search(r'^@(\w+)\{([^,\s]+)', first_line).groups()
        self.type = self.type.lower()

        # following lines:
        #   field_name = {value},
        #   field_name =   value,
        #   field_name = "value",
        pattern = r'^([^=\s]+)(?:\s+)?=(?:\s+)?'
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
        '''Render the reference string in IEEE style
        '''
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
                        first_name_abbr = re.sub(r'(\s*\w)\S*', '\\1.', first_name)
                        name_str = first_name_abbr + " " + last_name
                if i == num_authors - 2:
                    if authors[-1] == ("others",):
                        string += (name_str + " ")
                    else:
                        string += (name_str + ", and ")
                else:
                    string += (name_str + ", ")

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
                            pages = re.sub(r'-+', u'\u2013', get_raw_text(pages))
                        elif isinstance(pages, tuple):
                            pages = "{}\u2013{}".format(pages[0], pages[1])
                        vol_num_pages += "pp. {}, ".format(pages)
                if vol_num_pages == "":
                    string += u"\u201c{},\u201d {}, {}.".format(title, pub, year)
                else:
                    string += u"\u201c{},\u201d {}, {}{}.".format(title, pub, vol_num_pages, year)
            elif self.type == "inproceedings":
                pub = get_raw_text(self.tags["booktitle"], not_change_letter_case=True)
                pages = ""
                for key in ("pages",):
                    if self.tags.get(key, None) is None:
                        continue
                    if key == "pages":
                        pages = self.tags[key]
                        if isinstance(pages, str):
                            pages = "pp. " + re.sub(r'-+', u'\u2013', get_raw_text(pages))
                        elif isinstance(pages, tuple):
                            pages = "pp. {}\u2013{}".format(pages[0], pages[1])
                        else:
                            pages = "pp. {}".format(pages)
                if pages == "":
                    string += u"\u201c{},\u201d in {}, {}.".format(title, pub, year)
                else:
                    string += u"\u201c{},\u201d in {}, {}, {}.".format(title, pub, year, pages)
            else:
                raise ValueError('Unsupported publication type: %s' % self.type)
        else:
            raise ValueError('Unsupported style: %s' % style)
        return string
