from gui.TextEdit import TextStyle

def _make_style(color=(220, 220, 220), font_size=16, font_name='../gui/fonts/FreeMonoBold.ttf',
                bgcolor=None, is_italic=False, is_underline=False, is_bold=False):
    return TextStyle(color, font_size, font_name, bgcolor,
                     is_italic, is_underline, is_bold)

default = _make_style


key_name = _make_style(font_size=12, color=(80, 255, 80))
keydoc_name = _make_style(font_size=12, color=(255, 255, 255))

