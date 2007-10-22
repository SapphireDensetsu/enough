from gui.TextEdit import make_label, TextEdit
import style

def stylify_textedit_kws(kw):
    if 'font_size' not in kw:
        kw['font_size'] = style.default_font_size
        
    if 'color' not in kw:
        kw['color'] = style.default_font_color
        
    if 'font_name' not in kw:
        kw['font_name'] = style.default_font_name

    
def styled_label(*args, **kw):
    stylify_textedit_kws(kw)
    return make_label(*args, **kw)
    

class StyledTextEdit(TextEdit):
    def __init__(self, *args, **kw):
        stylify_textedit_kws(kw)
        TextEdit.__init__(self, *args, **kw)
