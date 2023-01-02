from panflute import *
import re

def to_str(x):
    if isinstance(x, Space):
        return " "
    else:
        return x.text

figure = re.compile("#ABSTRACT#")

def handle_figures(elem, doc):
    if isinstance(elem, Para):
        if len(elem.content) > 0 and isinstance(elem.content[0], Str):
            txt = elem.content[0].text
            z = figure.match(txt)
            if z is not None:
                para = "".join([to_str(x) for x in [*elem.content[2:]]])
                raw_latex = r"\begin{tcolorbox}[width=\textwidth,colback=\chapterbackcolor!20,title={\sffamily\textbf{\textcolor{white}{Abstract}}},colbacktitle=\chapterbackcolor]"
                raw_latex += para
                raw_latex += r"\end{tcolorbox}\clearpage"
                return RawBlock(raw_latex, format="latex")

def main(doc=None):
    return run_filter(handle_figures, doc=doc)

if __name__ == "__main__":
    main()
