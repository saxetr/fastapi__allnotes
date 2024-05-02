from xml.dom.minidom import parseString

import pytest

from allnotes.tools.odt2html import convert_xml_dom_to_html
from allnotes.tools.errors import (
    OdtUnknownTagError,
    OdtMissedElementAttrError,
    OdtUnknownHeaderError
)


def test__convert_xml_dom_to_html__return_html_paragraph_with_text_inside(make_xml):
    xml_src = parseString(make_xml(tag_name='p',
                                   tag_value='default_text&amp;nbsp;&amp;nbsp; 1'))

    assert convert_xml_dom_to_html(xml_src) == '<p>default_text&nbsp;&nbsp; 1</p>'


def test__convert_xml_dom_to_html__return_html_paragraph_tag_with_nested_a_tag(make_xml):
    xml_src = parseString(make_xml(tag_name='p',
                                   tag_value=' some text ',
                                   nested_tag_a=True))

    assert convert_xml_dom_to_html(xml_src) == '<p> some text <a href="https://docs.python.org/3/library/xml.html">https://docs.python.org/3/library/xml.html</a></p>'


def test__convert_xml_dom_to_html__return_html_header_tag(make_xml):
    xml_src = parseString(make_xml(tag_name='h',
                                   tag_style_k='text:style-name',
                                   tag_style_v='Heading_20_3',
                                   tag_value='Header 3'))

    assert convert_xml_dom_to_html(xml_src) == '<h3>Header 3</h3>'


def test__convert_xml_dom_to_html__raise_unknown_tag_error(make_xml):
    xml_src = parseString(make_xml(tag_name='f'))

    with pytest.raises(OdtUnknownTagError):
        convert_xml_dom_to_html(xml_src)


def test__convert_xml_dom_to_html__raise_missed_element_attribute_error(make_xml):
    xml_src = parseString(make_xml(tag_name='h',
                                   tag_style_k=None))

    with pytest.raises(OdtMissedElementAttrError):
        convert_xml_dom_to_html(xml_src)


def test__convert_xml_dom_to_html__raise_unknown_header_error(make_xml):
    xml_src = parseString(make_xml(tag_name='h',
                                   tag_style_k='text:style-name',
                                   tag_style_v='Heading_20_f'))

    with pytest.raises(OdtUnknownHeaderError):
        convert_xml_dom_to_html(xml_src)