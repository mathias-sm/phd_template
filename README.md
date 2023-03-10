# Template of Mathias Sablé-Meyer's Ph.D. Manuscript

> **Warning**
>
> The scripts here are provided `as is`. They worked for me but are far from
> polished. Things are brittle and may fail on ill-formed input — and what
> "well-formed" means here is at best loosely specified below.  
> Expect to have to dig into some of the scripts, templates, etc.

This is a collection of scripts I wrote in order to satisfy following
constraints:

1. Write the _text_ in Microsoft Word (don't ask why)
    1. Without having the figures in there because it becomes laggy after a
       little while
    2. With the references in there, handled by `zotero`
2. Have the best of `LaTeX` typesetting to generate an acceptable `.pdf`

You can take a look at what [my own manuscript looks
like](https://s-m.ac/documents/PhD_manuscript_Mathias_Sablé-Meyer.pdf), and from afar:

![mosaic of the first pages of Mathias Sablé-Meyer's Ph.D.](./media/overview.png)

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
`python=3.10`, `panflute=2.2.3`), as well as `xelatex` and a few basic Unix
tools (`make`, `sed`, `pdftk`).

# What to expect

Paragraphs starting with `#FIGUREXXlabel_float# caption` will turn into inserting
a float with the figure `./media/figure-XX.pdf` with the label `label`, a
size equal to `float*pagewidth`, and the rest of the paragraph as a caption.
Throughout the rest of the document, inserting `\ref{label}` will be replaced
with `Figure YY` in bold and in the color of the chapter, where YY is the
number generated by LaTeX, e.g. 2.3 if this is the third figure of chapter 2.

The same holds for tables, but the caption needs to be above, look like
`#TABLElabel_fontsize# caption` where `fontsize` is a valid LaTeX font size,
and you can reference them with `\ref{table:label}`

Code works as you expect: if a paragraph has style `SourceCode` in word, and
starts with a language name like `python` and a new line, then it will be
correctly turned into a code block with syntax highlight in LaTeX.

A paragraph starting with `#ABSTRACT#` will turn into a coloured box with the
right color.

Finally, quotes from the `.docx` file will be turned into LaTeX's `epigraphs`.
The script that does this assumes that the quote ends with a long dash followed
by the author reference.

# References

A note on references :

Zotero inserts references in the document, and I could just format them without
caring about parsing them as references, having a `.bib` file, etc.

With that said, it makes references unclickable, and is conceptually a bit sad,
since everything else is converted with at least some level of semantic
information. I wrote a small script to clean up references formatted by zotero
in a `.docx` file, left as `fix_ref.py`: using this one can modify the makefile
to include:

```makefile
# [...]
PhD.pdf: $(SOURCES) ./media/figure-1.pdf headers.yaml
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

This somewhat works, but placing the references at the right location (amongst
other things) proved too hard, so I ended up not going on with this. I am,
however, using it to generate a `html` version of my Ph.D.
