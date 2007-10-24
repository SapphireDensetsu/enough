from gui.TextEdit import TextStyle

def _make_style(color=(220, 220, 220), font_size=16, font_name='gui/fonts/FreeMonoBold.ttf',
                bgcolor=None, is_italic=False, is_underline=False, is_bold=False):
    return TextStyle(color, font_size, font_name, bgcolor,
                     is_italic, is_underline, is_bold)

unnamed_bg_color = (80, 20, 20)

key_name = _make_style(font_size=12, color=(80, 255, 80))
key_space_width = 30
keydoc_name = _make_style(font_size=12, color=(255, 255, 255))

indent_width = 40
braces = _make_style(color=(200, 200, 255))
paren = _make_style(color=(220, 220, 255))
bracket = _make_style(color=(200, 200, 255))
comma = _make_style(color=(200, 200, 255))
operator = _make_style(color=(220, 220, 255))
semicolon = _make_style(color=(200, 200, 255))
space = _make_style()

keyword = _make_style(color=(255, 30, 30))
if_ = _make_style(color=keyword.color)
else_ = _make_style(color=keyword.color)
return_ = _make_style(color=keyword.color)

type_ = _make_style(color=(60, 255, 60))
base_type = _make_style(color=(30, 255, 30))
func_name = _make_style(color=(220, 220, 50))
module_name = _make_style(color=(255, 255, 255))
variable_name = _make_style(color=(100, 100, 255))
define = _make_style(color=(120, 255, 150))

identifier = _make_style(color=(150, 150, 255))
enum = _make_style(color=keyword.color)
enum_value = _make_style(color=identifier.color)
import_ = _make_style(color=(255, 130, 130))

def emphasize(style):
    s = TextStyle.from_style(style)
    s.is_bold = True
    return s

import nodes
literal_style_for = {
    nodes.LiteralInt : _make_style(color=(180, 255, 255)),
    nodes.LiteralChar : _make_style(color=(100, 255, 255)),
    nodes.LiteralString : _make_style(color=(0, 255, 255)),
}
