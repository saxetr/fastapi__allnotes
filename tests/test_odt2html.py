from xml.dom.minidom import parseString

import pytest

from fastapi__allnotes.tools.odt2html import convert_xml_dom_to_html
from fastapi__allnotes.tools.errors import UnknownTagError





s2 = '<office:text xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">' \
'<text:h text:style-name="Heading_20_3" text:outline-level="3">Header 3</text:h>' \
'</office:text>'


s3 = '<office:text xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">' \
'<text:p text:style-name="P1">default_text&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;</text:p>' \
'</office:text>'    


s4 = '<office:text xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:xlink="http://www.w3.org/1999/xlink">' \
'<text:p text:style-name="P1"> some text ' \
    '<text:a xlink:type="simple" xlink:href="https://docs.python.org/3/library/xml.html" ' \
        'text:style-name="Internet_20_link" ' \
        'text:visited-style-name="Visited_20_Internet_20_Link">' \
        'https://docs.python.org/3/library/xml.html' \
    '</text:a>' \
'</text:p>' \
'</office:text>'   


s5 = '<office:text xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">' \
'<text:f>default_text</text:f>' \
'</office:text>'


def test__convert_xml_dom_to_html__return_html_paragraph_with_text_inside():
    xml_src = parseString(s3)

    assert convert_xml_dom_to_html(xml_src) == '<p>default_text&nbsp;&nbsp;&nbsp;&nbsp;</p>'


def test__convert_xml_dom_to_html__return_html_paragraph_tag_with_nested_a_tag():
    xml_src = parseString(s4)

    assert convert_xml_dom_to_html(xml_src) == '<p> some text <a href="https://docs.python.org/3/library/xml.html">https://docs.python.org/3/library/xml.html</a></p>'


def test__convert_xml_dom_to_html__raise_unknown_tag_error():
    xml_src = parseString(s5)

    with pytest.raises(UnknownTagError):
        convert_xml_dom_to_html(xml_src)


def test__convert_xml_dom_to_html__return_html_block_h():
    xml_src = parseString(s2)

    assert convert_xml_dom_to_html(xml_src) == '<h3>Header 3</h3>'

