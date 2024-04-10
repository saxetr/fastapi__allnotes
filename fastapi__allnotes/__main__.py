from xml.dom.minidom import parseString, parse
import zipfile

from fastapi__allnotes.tools.odt2html import convert_xml_dom_to_html



def main():
    with zipfile.ZipFile('tmp/tmp.odt') as myzip:
        with myzip.open('content.xml') as content:
            print(convert_xml_dom_to_html(parse(content)))


if __name__ == "__main__": 
    # main()
    from fastapi__allnotes.kb.dbschema import metadata_obj
    from fastapi__allnotes.kb.crud import engine
    print(metadata_obj)
    metadata_obj.create_all(engine)
