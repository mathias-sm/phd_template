# What to compile by default?
SOURCES = manuscript.docx

default: PhD.pdf

PhD.pdf: $(SOURCES) ./media/figure-1.pdf headers.yaml
	python fix_ref.py $(SOURCES) tmp.docx
	pandoc tmp.docx --from docx+citations --citeproc -o bib.bib
	pandoc tmp.docx \
		--pdf-engine=xelatex \
		-s \
		--from docx+citations \
		--extract-media docx-media \
		--template template.tex \
		--filter handle_code.py \
		--filter handle_titles.py \
		--filter handle_figures.py \
		--filter handle_tables.py \
		--filter handle_refs.py \
		--filter quotes_to_epi.py \
		--filter handle_sb.py \
		--reference-links \
		--reference-location=block \
		--citeproc \
		--natbib \
		--bibliography=bib.bib \
		--highlight-style tango \
		--metadata-file headers.yaml \
		--wrap none \
		--top-level-division=chapter \
		-o body.tex
	sed -ie 's/\(In chapter\) \([0-9]\)\,/\\textcolor\{color\2\}\{\\strong\{\1 \2,\}\}/g' body.tex
	sed -ie 's/\([cC]hapter\) \([0-9]\)/\\textcolor\{color\2\}\{\\strong\{\1 \2\}\}/g' body.tex
	latexmk -xelatex body.tex
	pdftk E=blank.pdf D=real_cover.pdf A=couverture.pdf B=body.pdf C=quatrieme.pdf cat D1 E1 A1 B4-r2 C1 output tmp.pdf
	pdftk body.pdf dump_data > in.info
	pdftk tmp.pdf update_info in.info output PhD.pdf
	#gs -dPDFA=1 -dNOOUTERSAVE -sProcessColorModel=DeviceRGB -sDEVICE=pdfwrite -o PhD_thesis.pdf ./PDFA_def.ps -dPDFACompatibilityPolicy=1 tmp2.pdf
	rm tmp.pdf in.info tmp.docx

clean:
	latexmk -C
	rm -f PhD.pdf ./media/cropped*.pdf body.tex
