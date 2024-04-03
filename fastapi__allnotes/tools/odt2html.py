from xml.dom.minidom import parse, parseString, Document, Node, Element
import zipfile

from fastapi__allnotes.tools.errors import UnknownTagError


def generate_html_header_tag(element: Element) -> str:
    HEADERS = {"Heading_20_1": "1", "Heading_20_2": "2", "Heading_20_3": "3"}
    h_attr = element.getAttribute('text:style-name') 
    header_number = HEADERS[h_attr]
    return f'<h{header_number}>{element.firstChild.nodeValue}</h{header_number}>'


def generate_html_a_tag(element: Element) -> str:
    a_href = element.getAttribute('xlink:href')
    return f'<a href="{a_href}">{element.firstChild.nodeValue}</a>'


def generate_html_paragraph_tag(element: Element) -> str:
    html = '<p>'
    for node in element.childNodes:
        if node.nodeType == Node.TEXT_NODE:
            html += node.nodeValue

        elif node.tagName == "text:a":
            html += generate_html_a_tag(node)

    html += '</p>'
    return html


def convert_xml_dom_to_html(document: Document) -> str:
    res = []

    new_root = document.getElementsByTagName('office:text')[0].childNodes
    for node in new_root:
        if node.tagName == "text:sequence-decls":
            continue

        if node.tagName == "text:h":
            res.append(generate_html_header_tag(node))
            continue

        if node.tagName == "text:p":
            res.append(generate_html_paragraph_tag(node))
            continue

        raise UnknownTagError(node.tagName)

    return ''.join(res)



if __name__ == "__main__": 
    with zipfile.ZipFile('tmp/tmp.odt') as myzip:
        with myzip.open('content.xml') as content:
            print(convert_xml_dom_to_html(parse(content)))
