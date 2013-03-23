from django import template

register = template.Library()
@register.simple_tag
def naactive(request, pattern):
    import re
    if re.search(pattern, request.path):
        #print pattern, request.path
        return 'active'
    #print 'fail'
    return ''

