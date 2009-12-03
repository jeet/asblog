from applications.init.modules.markdown import markdown

def highlight_code(text, safe = False):
    """
    Odpowiada za formatowanie kodu przy uzyciu Markdown + kolorowanie skladni.
    """

    if safe:
        markdowned = markdown(text, ['codehilite'], safe_mode=True)
    else:
        markdowned = markdown(text, ['codehilite'])

    return unicode(markdowned)

def highlight_code_filter(value, arg=''):
    if arg == "safe":
        safe = True
    else:
        safe = False
    return highlight_code(value, safe)
