# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

from gui.TextEdit import TextStyle

def _make_style(color=(220, 220, 220), font_size=16, font_name='../gui/fonts/FreeMonoBold.ttf',
                bgcolor=None, is_italic=False, is_underline=False, is_bold=False):
    return TextStyle(color, font_size, font_name, bgcolor,
                     is_italic, is_underline, is_bold)


unnamed_bg_color = (80, 20, 20)

key_name = _make_style(font_size=12, color=(80, 255, 80))
keydoc_name = _make_style(font_size=12, color=(255, 255, 255))

indent_width = 40
braces = _make_style(color=(200, 200, 255))
paren = _make_style(color=(220, 220, 255))
bracket = _make_style(color=(200, 200, 255))
comma = _make_style(color=(200, 200, 255))
operator = _make_style(color=(220, 220, 255))
semicolon = _make_style(color=(200, 200, 255))
ellipsis = _make_style(color=(200, 200, 255), bgcolor=(200, 20, 20),
                       is_bold=True, is_italic=True)
space = _make_style()

keyword = _make_style(color=(255, 90, 90))
if_ = keyword
else_ = keyword
return_ = keyword
enum = keyword

type_ = _make_style(color=(60, 255, 60))
base_type = _make_style(color=(30, 255, 30))
func_name = _make_style(color=(220, 220, 50))
module_name = _make_style(color=(255, 255, 255))
variable_name = _make_style(color=(100, 100, 255))
define_value = _make_style(color=(120, 255, 150))

identifier = _make_style(color=(150, 150, 255))
enum_value = _make_style(color=identifier.color)
import_ = _make_style(color=(255, 160, 160))

define = _make_style(color=(90, 255, 50))

def emphasize(style):
    s = TextStyle.from_style(style)
    s.is_bold = True
    return s

literal_int = _make_style(color=(180, 255, 255))
literal_char = _make_style(color=(100, 255, 255))
literal_string = _make_style(color=(0, 255, 255))

literal_string_delimiter = _make_style(color=(200, 200, 255))
literal_char_delimiter = _make_style(color=(200, 200, 255))

example_string = literal_string
example_char_int = _make_style(color=(255, 255, 255))
example_int = _make_style(color=(255, 255, 255))

filler = _make_style(color=(20, 50, 255), bgcolor=(200, 0, 0))

unknown_c_code = _make_style(color=(20, 255, 255), bgcolor=(100, 0, 0))
