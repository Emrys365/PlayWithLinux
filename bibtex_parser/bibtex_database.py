#!/usr/bin/env python3
import argparse
import re
import sqlite3

from bibtex import BibTeXEntry
from bibtex import get_raw_text
from bibtex import remove_brace_pair


class BibTeXDatabase:
    def __init__(self, dbfile="mybib.db", dbname="bibtex"):
        columns = [
            # meta info
            ("uid", "INTEGER PRIMARY KEY AUTOINCREMENT"),
            ("type", "TEXT"),
            ("name", "TEXT", "UNIQUE ON CONFLICT FAIL"),
            # citation
            ("bibstring", "TEXT"),
            ("citestring", "TEXT"),
            # bibtex fields
            ("title", "TEXT"),
            ("author", "TEXT"),
            ("booktitle", "TEXT"),
            ("journal", "TEXT"),
            ("volume", "INTEGER"),
            ("number", "INTEGER"),
            ("pages", "TEXT"),
            ("year", "INTEGER"),
            ("organization", "TEXT"),
            ("publisher", "TEXT"),
        ]
        self.name = dbname
        self.__dbfile = dbfile
        self.__conn = sqlite3.connect(dbfile)
        self.__cursor = self.__conn.cursor()
        self.connected = True

        self.__cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {dbname} '
            '({})'.format(
                ', '.join(' '.join(it) for it in columns)
            )
        )

    def commit(self):
        self.__conn.commit()

    def close(self, do_commit=False):
        if do_commit:
            self.commit()
        self.__cursor.close()
        self.__conn.close()
        self.connected = False

    def reconnect(self):
        if not self.connected:
            self.__conn = sqlite3.connect(self.__dbfile)
            self.__cursor = self.__conn.cursor()
            self.connected = True
        else:
            print("Already Connected. Nothing to do.")

    def operate(self, option, **kwargs):
        keys = tuple(
            k for k in [
                "type",
                "name",
                "bibstring",
                "citestring",
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
            ]
            if kwargs.get(k, None) is not None
        )
        if option == "insert":
            self.__cursor.execute(
                f"INSERT INTO {self.name} ({', '.join(keys)}) VALUES "
                f"({', '.join(['?' for _ in keys])})",
                tuple(kwargs[k] for k in keys)
            )
        elif option == "update":
            self.__cursor.execute(
                f"UPDATE {self.name} SET " +
                ", ".join([f"{k} = ?" for k in keys if k != "name"]) +
                " WHERE name = ?",
                tuple(kwargs[k] for k in keys if k != "name") + (kwargs["name"],),
            )
        elif option == "delete":
            self.__cursor.execute(
                f"DELETE FROM {self.name} WHERE " +
                " AND ".join([f"{k} = ?" for k in keys]),
                tuple(kwargs[k] for k in keys)
            )
        elif option == "select":
            self.__cursor.execute(
                f"SELECT * FROM {self.name} WHERE " +
                # " AND ".join([f"{k} = ?" for k in keys]),
                " AND ".join([f"{k} LIKE '%'||?||'%'" for k in keys]),
                tuple(kwargs[k] for k in keys)
            )
        else:
            raise ValueError(f"Unsupported option: {option}")

    def __proc_bib_dict(self, dic):
        ret = {}
        for k, v in dic.items():
            if v is None or (hasattr(v, "__len__") and len(v) == 0):
                continue
            if isinstance(v, dict):
                ret[k] = {k2: self.__proc_bib_dict(v2) for k2, v2 in v.items()}
            elif k in ("title", "journal", "booktitle") and isinstance(v, str):
                ret[k] = get_raw_text(v, not_change_letter_case=True)
            elif isinstance(v, str):
                ret[k] = remove_brace_pair(v)
            elif k == "author" and isinstance(v, (list, tuple)):
                ret[k] = remove_brace_pair(
                    re.sub(
                        r', others$', ' et al.',
                        ", ".join([
                            get_raw_text(" ".join(each), not_change_letter_case=True)
                            for each in v
                        ]),
                    )
                )
            elif k == "pages" and isinstance(v, (list, tuple)):
                ret[k] = remove_brace_pair(u"\u2013".join([str(vv) for vv in v]))
            else:
                ret[k] = v
        return ret

    def add_bibtex(self, bibtex, name=None, style="IEEEtran"):
        bib = bibtex if isinstance(bibtex, BibTeXEntry) else BibTeXEntry(bibtex, force_name=True)
        if name is not None:
            bib.name = name
        tags = self.__proc_bib_dict(bib.tags)
        try:
            self.operate(
                "insert",
                type=bib.type,
                name=bib.name,
                bibstring=str(bib),
                citestring=bib.to_plaintext(style=style),
                **tags,
            )
        except sqlite3.IntegrityError:
            bib_existing = BibTeXEntry(self.search_bibtex(name=bib.name)[0][3])
            if (
                bib.tags.get("journal", "") != bib_existing.tags.get("journal", "")
                or bib.tags.get("booktitle", "") != bib_existing.tags.get("booktitle", "")
            ):
                idx = 1
                retry = True
                while retry:
                    idx += 1
                    name = bib.name + f"_{idx}"
                    retry = len(self.search_bibtex(name=name)) > 0
                return self.add_bibtex(bibtex, name=name, style=style)
            else:
                return f"Record already exists. Nothing to do."
        return f"Inserted with UID={self.__cursor.lastrowid}."

    def add_refstr(self, refstr, name=None, type="article", style="IEEEtran"):
        bib = BibTeXEntry.plaintext_to_bibtex(refstr, default_type=type)
        return self.add_bibtex(bib, name=name, style=style)

    def update_bibtex(self, bibtex, name=None, style="IEEEtran"):
        bib = bibtex if isinstance(bibtex, BibTeXEntry) else BibTeXEntry(bibtex, force_name=True)
        if name is not None:
            bib.name = name
        tags = self.__proc_bib_dict(bib.tags)
        match = self.search_bibtex(name=bib.name)
        match = [m for m in match if m[2] == bib.name]
        if len(match) != 1:
            return f"{len(match)} records found. Do nothing."
        # bib_existing = BibTeXEntry(match[0][3])
        # bib_existing.type = bib.type
        # bib_existing.name = bib.name
        # tags_existing = self.__proc_bib_dict(bib_existing.tags)
        # tags_existing.update(tags)

        try:
            self.operate(
                "update",
                type=bib.type,
                name=bib.name,
                bibstring=str(bib),
                citestring=bib.to_plaintext(style=style),
                **tags,
            )
            # self.operate(
            #     "update",
            #     type=bib_existing.type,
            #     name=bib_existing.name,
            #     bibstring=str(bib_existing),
            #     citestring=bib_existing.to_plaintext(style=style),
            #     **tags_existing,
            # )
        except:
            return f"Fail to update record: '{bib.name}'"
        return f"Updated record '{bib.name}' with UID={match[0][0]}."

    def remove_bibtex(self, **kwargs):
        opt = {
            k: str(v) if isinstance(v, (list, tuple, dict)) else v
            for k, v in kwargs.items()
            if v is not None and (not hasattr(v, "__len__") or len(v) > 0)
        }
        ret = self.search_bibtex(**opt)
        if len(ret) > 0:
            self.operate("delete", **opt)
            return f"Deleted {len(ret)} records."
        else:
            return "No match found. Nothing to do."

    def search_bibtex(self, **kwargs):
        opt = {
            k: str(v) if isinstance(v, (list, tuple, dict)) else v
            for k, v in kwargs.items()
            if v is not None and (not hasattr(v, "__len__") or len(v) > 0)
        }
        self.operate("select", **opt)
        return self.__cursor.fetchall()

    def list_database(self):
        self.__cursor.execute(f"SELECT * FROM {self.name}")
        return self.__cursor.fetchall()

    def __len__(self):
        if self.connected:
            self.__cursor.execute(f"SELECT COUNT(*) FROM {self.name}")
            length = self.__cursor.fetchone()[0]
        else:
            self.reconnect()
            self.__cursor.execute(f"SELECT COUNT(*) FROM {self.name}")
            length = self.__cursor.fetchone()[0]
            self.close()
        return length

    def add_fromfile(self, bibfile, skipNlines=0):
        count_insert = 0
        count_duplicate = 0
        level = 0
        found = False
        bibstring = ""
        with open(bibfile, "r") as f:
            for i, line in enumerate(f):
                if i < skipNlines:
                    continue
                line = line.lstrip()
                if not line or line.startswith("%"):
                    # skip empty or commented lines
                    continue
                if level == 0:
                    found = re.match(r'^\s*@\w+\{', line) is not None
                prev = ""
                for c in line:
                    if c == "{" and prev != "\\":
                        level += 1
                    elif c == "}" and prev != "\\":
                        level -= 1
                    prev = c
                if found:
                    bibstring = bibstring + line
                    if level == 0:
                        found = False
                        try:
                            ret = self.add_bibtex(bibstring)
                        except:
                            print(bibstring)
                            raise
                        if ret.startswith("Inserted with UID="):
                            count_insert += 1
                        else:
                            count_duplicate += 1
                        bibstring = ""
        if count_insert == 0:
            return f"No new records found in {bibfile}. Nothing to do.\n{count_duplicate} duplicate records already exist."
        else:
            return f"Inserted {count_insert} new record(s).\n{count_duplicate} duplicate records already exist."

    def clear(self):
        self.__cursor.execute(f"DELETE FROM {self.name}")

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--add-bibtex", type=str, default=None, help="parse and insert a bibtex entry"
    )
    parser.add_argument(
        "--add-refstr",
        type=str,
        default=None,
        help="parse and insert a plain reference string",
    )
    parser.add_argument(
        "--remove",
        type=str,
        default=None,
        help="remove a bibtex with the specified key from the database",
    )
    parser.add_argument(
        "--search",
        type=str,
        default=None,
        help="search for a bibtex containing the specified keyword(s) from the database",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list all bibtex entries in the current database",
    )
    return parser


if __name__ == "__main__":
    db = BibTeXDatabase()

    parser = get_parser()
    args = parser.parse_args()
    check_args_num = [
        args.add_bibtex is not None,
        args.add_refstr is not None,
        args.remove is not None,
        args.search is not None,
        args.list,
    ]

    do_commit = False
    if sum(check_args_num) > 1:
        print(
            "%s\n\nNOTE:\n  only one optional argument is allowed."
            % parser.format_help()
        )
    elif check_args_num[0]:
        ret = db.add_bibtex(args.add_bibtex)
        do_commit = True
    elif check_args_num[1]:
        ret = db.add_refstr(args.add_refstr)
        do_commit = True
    elif check_args_num[2]:
        ret = db.remove_bibtex(args.remove)
        do_commit = True
    elif check_args_num[3]:
        ret = db.search_bibtex(args.search)
    elif check_args_num[4]:
        ret = db.list_database()

    db.close(do_commit=do_commit)
