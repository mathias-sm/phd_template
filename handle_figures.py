from panflute import *
import re

figure = re.compile("#FIGURE([0-9]+)([a-zA-Z0-9-]*)_?(f?)([oOiIlLrR]?)([0-9.]*)#")

def handle_figures(elem, doc):
    if isinstance(elem, Para):
        if len(elem.content) > 0 and isinstance(elem.content[0], Str):
            txt = elem.content[0].text
            z = figure.match(txt)
            if z is not None:
                z = z.groups()
                fig_idx = int(z[0])
                fig_ref = ""
                if len(z[1]) != 0:
                    fig_ref = "\\label{" + str(z[1]) + "}"
                fig_path = f"./media/figure-{fig_idx}.pdf"
                caption = elem.content[2:]
                latex_begin = None
                latex_end = None
                if z[2] != "f":
                    latex_begin = r'\begin{figure}'
                    latex_end = fig_ref+r'\end{figure}'
                    scale = '1.0' if z[4] == "" else z[4]
                    latex_fig = r'\centering\includegraphics[width='+scale+r'\textwidth]{' + fig_path  + '}'
                else:
                    width = '0.5' if z[4] == "" else z[4]
                    latex_begin = r'\begin{wrapfigure}{'+z[3]+r'}{'+width+r'\textwidth}'
                    latex_end = fig_ref+r'\end{wrapfigure}'
                    latex_fig = r'\centering\includegraphics{' + fig_path  + '}'
                if len(caption) != 0:
                    latex_fig = latex_fig + r'\caption{\scriptsize{'
                    latex_end = r'}}' + latex_end
                if len(caption) == 0 and len(z[1]) != 0:
                    latex_fig = latex_fig + r'\caption{'
                    latex_end = r'}' + latex_end
                begin = ListContainer(RawInline(latex_begin + latex_fig, format="latex"))
                end = ListContainer(RawInline(latex_end, format="latex"))
                return Para(*begin, *caption, *end)


def main(doc=None):
    return run_filter(handle_figures, doc=doc)

if __name__ == "__main__":
    main()
