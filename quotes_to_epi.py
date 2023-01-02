from panflute import *

def to_str(x):
    if isinstance(x, Space):
        return " "
    elif isinstance(x, LineBreak):
        return "\\\\"
    else:
        return x.text


def quotes_to_epi(elem, doc):
    if isinstance(elem, BlockQuote):
        quote = "".join([to_str(x) for x in [*elem.content[0].content]])
        quote, author = quote.split("\\\\— ")
        return(RawBlock(rf"\epigraph{{{quote}}}{{{author}}}", format="latex"))

def main(doc=None):
    return run_filter(quotes_to_epi, doc=doc)

if __name__ == "__main__":
    main()
