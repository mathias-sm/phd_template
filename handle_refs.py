from panflute import *
import re

ref = re.compile("(.*)\\\\ref{([a-zA-Z0-9_-]+)}(.*)")
ref_tab = re.compile("(.*)\\\\ref{table:([a-zA-Z0-9:_-]+)}(.*)")

def handle_figures(elem, doc):
    if isinstance(elem, Str):
        z = ref.match(elem.text)
        if z is not None:
            m = [str(x) for x in z.groups()]
            # \textcolor{\chapterbackcolor}\{\strong\{\1 \2,\}\
            return RawInline(m[0]+"\\textcolor{\\chapterbackcolor}{\\strong{Figure \\ref{"+m[1]+"}}}"+m[2], format="latex")
        z = ref_tab.match(elem.text)
        if z is not None:
            m = [str(x) for x in z.groups()]
            return RawInline(m[0]+"\\textcolor{\\chapterbackcolor}{\\strong{Table \\ref{table:"+m[1]+"}}}"+m[2], format="latex")


def main(doc=None):
    return run_filter(handle_figures, doc=doc)

if __name__ == "__main__":
    main()
