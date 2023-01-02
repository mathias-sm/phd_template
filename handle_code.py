from panflute import *


def handle_code(elem, doc):
    if isinstance(elem, CodeBlock):
        lang, *text = elem.text.split("\n")
        return CodeBlock(classes=[lang], text="\n".join(text))


def main(doc=None):
    return run_filter(handle_code, doc=doc)

if __name__ == "__main__":
    main()
