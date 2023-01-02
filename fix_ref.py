from docx import Document
import copy
import json
import fire


def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True


def fix_ref(infile, outfile):
    document = Document(infile)
    prefix = " ADDIN ZOTERO_ITEM CSL_CITATION "

    xx = None
    for x in document._element.xpath('//w:instrText[contains(., CSL_CITATION)]'):
        xt = copy.copy(x.text)
        if prefix in xt:
            xt = xt.removeprefix(prefix)
            parsed = None
            current = x
            fullstr = xt
            while not is_json(fullstr):
                current = current.getparent().getnext().getchildren()[-1]
                fullstr += current.text
            parsed = json.loads(fullstr)
            for item in parsed["citationItems"]:
                item["itemData"]["id"] = item["id"]
            x.text = prefix + json.dumps(parsed)

    document.save(outfile)


if __name__ == "__main__":
    fire.Fire(fix_ref)
