from django import template
from html.parser import HTMLParser

register = template.Library()


@register.filter
def add(left, right):
    '''
    templateでint type dataを演算する時使用
    '''
    return left + right


@register.filter
def minus(left, right):
    '''
    templateでint type dataを演算する時使用
    '''
    return left - right


@register.filter
def decode(value):
    """HTML decodes a string """
    h = HTMLParser()
    return h.unescape(value)
