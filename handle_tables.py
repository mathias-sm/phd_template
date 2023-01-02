from panflute import *
import re

table = re.compile("#TABLE([a-zA-Z0-9-]*)_([a-z]+)#")


def handle_tables(elem, doc):
    if isinstance(elem, Para):
        if len(elem.content) > 0 and isinstance(elem.content[0], Str):
            txt = elem.content[0].text
            z = table.match(txt)
            if z is not None:
                z = z.groups()
                table_pointer = elem.next
                tbl_ref = ""
                if len(z[0]) != 0:
                    tbl_ref = r"\label{table:" + str(z[0]) + "}"
                tbl_ref = RawInline(tbl_ref, format="latex")
                caption = Caption(Plain(*elem.content[2:], tbl_ref))
                table_pointer.caption = caption
                size_begin = RawBlock(r"\begin{"+z[1]+"}", format="latex")
                size_end = RawBlock(r"\end{"+z[1]+"}", format="latex")
                return [size_begin, table_pointer, size_end]
    elif isinstance(elem, Table):
        return []


def main(doc=None):
    return run_filter(handle_tables, doc=doc)

if __name__ == "__main__":
    main()
