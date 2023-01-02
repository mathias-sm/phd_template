# Template of Mathias Sablé-Meyer's Ph.D. Manuscript

> **Warning**
> The scripts here are provided `as is`. They workd for me but are far from
> polished. Expect to have to dig into some of the scripts, templates, etc.

This is a collection of scripts I wrote in order to satisfy following
constraints:

1. Write the _text_ in Microsoft Word (don't ask why)
    1. Without having the figures in there because it becomes laggy after a
       little while
    2. With the references in there, handled by `zotero`
2. Have the best of `LaTeX` typesetting to generate an acceptable `.pdf`

You can take a look at what [my own manuscript looks
like](https://s-m.ac/documents/PhD_manuscript_Mathias_Sablé-Meyer.pdf).

It relies heavily on `pandoc` to perform the `.docx -> .tex` translation,
together with a souped-up template I needed. On top of this, a few `panflute`
scripts work on pandoc's `AST` to be able to insert figures where needed,
format tables better, handle references to figures in a `LaTeX` way, and a few
other things.

Then `XeLaTeX` performs the final compilation step, and just because my
doctoral school required a specific template for the front and the back,
`pdftk` makes a few page changes.

In order for this to work you need some version of `pandoc` (all I can say is,
it works on `2.19.2`) and some version of python and panflute (worked on
`python=3.10`, `panflute=2.2.3`), as well as `xelatex` and a few basic unix
tools (`make`, `sed`, `pdftk`).

A note on references : I wrote a small script to clean up references formatted by zotero in a `.docx` file, left as `fix_ref.py`: using this one can modify the makefile to include:

```makefile
	python fix_ref.py $(SOURCES) tmp.docx
	pandoc tmp.docx --from docx+citations --citeproc -o bib.bib
	pandoc tmp.docx \
		--[...] \
		--reference-links \
		--reference-location=block \
		--citeproc \
		--natbib \
		--bibliography=bib.bib \
		--[...]
		--[...]
  rm tmp.docx
```

This somewhat works but placing the references at the right location (amongst
other things) proved too hard, so I ended up not going on with this. I am,
however, using it to generate a `html` version of my Ph.D.
