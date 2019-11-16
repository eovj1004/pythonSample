from django import template


register = template.Library()


@register.filter
def add(left, right):
    '''
    templateでint type dataを演算する時使用
    '''
    return left + right
