from xml.dom.minidom import parseString, parse
import zipfile

from allnotes.tools.odt2html import convert_xml_dom_to_html



def main():
    with zipfile.ZipFile('tmp/tmp.odt') as myzip:
        with myzip.open('content.xml') as content:
            print(convert_xml_dom_to_html(parse(content)))


if __name__ == "__main__": 
    # main()

    from allnotes.kb.crud import session, add_note
    add_note(session, 'test_note_1')