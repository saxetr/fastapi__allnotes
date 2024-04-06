"""
конвернтирует odt документ в html
поддерживает тэги: h, p, a
заголовок и абзац - отдельные строки
абзац может вмещать тег <a> и текст
"""

from xml.dom.minidom import Document, Node, Element


from fastapi__allnotes.tools.errors import OdtUnknownTagError, OdtMissedElementAttrError, OdtUnknownHeaderError


HEADERS = {"Heading_20_1": "1", "Heading_20_2": "2", "Heading_20_3": "3"}


def generate_html_header_tag(element: Element) -> str:
    if not element.hasAttribute('text:style-name'):
        raise OdtMissedElementAttrError('text:style-name')
    
    h_attr = element.getAttribute('text:style-name') 
    try:
        header_number = HEADERS[h_attr]
    except KeyError:
        raise OdtUnknownHeaderError(h_attr)
        
    return f'<h{header_number}>{element.firstChild.nodeValue}</h{header_number}>'


def generate_html_a_tag(element: Element) -> str:
    if not element.hasAttribute('xlink:href'):
        raise OdtMissedElementAttrError('xlink:href')
    
    a_href = element.getAttribute('xlink:href')
    return f'<a href="{a_href}">{element.firstChild.nodeValue}</a>'


def generate_html_paragraph_tag(element: Element) -> str:
    html = ['<p>']
    for node in element.childNodes:
        if node.nodeType == Node.TEXT_NODE:
            html.append(node.nodeValue)

        elif node.tagName == "text:a":
            html.append(generate_html_a_tag(node))

    html.append('</p>')
    return ''.join(html)


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

        raise OdtUnknownTagError(node.tagName)

    return ''.join(res)
