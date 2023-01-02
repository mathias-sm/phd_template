from panflute import *

# Dirty hack: things are processed in order, so a flag can tell us whether we
# are "in" the introduction section. This makes the demode function non-pure
global bigflag
bigflag = False

def demote_titles(elem, doc):
    global bigflag
    if isinstance(elem, Header):
        if elem.level == 1:
            if elem.identifier in ["preface", "introduction", "references", "appendix", "conclusion"]:
                elem.classes = elem.classes + ["unnumbered"]
                if elem.identifier == "introduction":
                    bigflag = True
                if elem.identifier == "preface":
                    bigflag = True
                if elem.identifier == "conclusion":
                    bigflag = True
                    return(RawBlock(r"\setcounter{chapter}{0}\hypertarget{conclusion}{\chapter*{Conclusion}\label{conclusion}}\addcontentsline{toc}{chapter}{Conclusion}\renewcommand{\leftmark}{Conclusion}", format="latex"))
                if elem.identifier == "references":
                    return(RawBlock(r'\twocolumn\hypertarget{references}{\chapter*{References}\label{references}}\addcontentsline{toc}{chapter}{References}\renewcommand{\leftmark}{References}\begin{hangparas}{.1in}{1}\tiny', format="latex"))
                if elem.identifier == "appendix":
                    return(RawBlock(r'\end{hangparas}\onecolumn\hypertarget{appendix}{\chapter*{Appendix}\label{appendix}}\addcontentsline{toc}{chapter}{Appendix}\renewcommand{\leftmark}{Appendix}\normalsize', format="latex"))
                else:
                    return elem
        if elem.level == 2:
            if elem.identifier in ["remerciements", "acknowledgements-remerciements", "open-data-statement", "originality-of-the-work"]:
                elem.classes = elem.classes + ["unnumbered"]
                return elem
        if "in-which-we" in elem.identifier:
            bigflag = False
            return(RawBlock(r'\hypertarget{in-which-we-talk-about-the-first-things}{\chapter{In which we talk about the first things}\label{in-which-we-talk-about-the-first-things}}\renewcommand{\leftmark}{In which we talk about the first things}', format="latex"))
        if "in-that-one-we" in elem.identifier:
            return(RawBlock(r'\hypertarget{in-that-one-we-talk-about-that-other-things}{\chapter{In that one we talk about that other things}\label{in-that-one-we-talk-about-that-other-things}}\renewcommand{\leftmark}{In that one we talk about that other things}', format="latex"))
        if bigflag:
            elem.classes = elem.classes + ["unnumbered"]


def main(doc=None):
    return run_filter(demote_titles, doc=doc)

if __name__ == "__main__":
    main()
