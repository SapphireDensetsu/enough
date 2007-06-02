from Lib.Point import Point


def TableLayout(width, height, widgets, scale=1, autoscale=True, offset = None):
    if offset is None:
        offset = Point(0,0)

    # if scale is None - scale to fit the whole size
    margin = 10
    if not autoscale:
        margin *= scale
        
    x_margin = y_margin = margin
        
    pos = Point(x_margin, y_margin)
    next_row = 0


    # order the widgets according to level, and find the maximum widget size
    
    ordered = []
    max_size = Point(0,0)
    for widget in widgets:
        if autoscale:
            widget.scale = 1
        else:
            widget.scale = scale
        
        level = widget.order.level
        sublevel = widget.order.sublevel
            
        ordered.append((level, sublevel, widget))
        max_size.x = max(max_size.x, widget.size.x)
        max_size.y = max(max_size.y, widget.size.y)

    ordered.sort()

    # setup the widgets in a table

    prev_level = 0
    pos = Point(x_margin,y_margin)
    table_size = Point(0,0)
    for level, sublevel, widget in ordered:
        if ((pos.x + max_size.x >= width)
            or (level > prev_level)):
            prev_level = level
            pos.y += max_size.y + y_margin
            pos.x = x_margin
                
        widget.pos = pos.shallow_copy()
        pos.x += max_size.x + x_margin

        table_size.x = max(table_size.x, widget.pos.x + widget.size.x)
        table_size.y = max(table_size.y, widget.pos.y + widget.size.y)


    if autoscale:
        # STUPID IMPLEMENTATION
        # todo change it
        # go back and relayout with the calculated scale
        new_scale = min(float(width-10) / table_size.x, float(height-10) / table_size.y)
        TableLayout(width, height, widgets, new_scale * scale, autoscale=False)
        return
    
    # center the table
    size = Point(width, height)
    center_pos = size*0.5 - table_size*0.5 - Point(x_margin, y_margin)
    # now center the table
    for widget in widgets:
        widget.pos += center_pos + offset


from math import pi
def SurroundLayout(width, height, source_widget, subwidgets_of, scale=1, subwidgets_center_offset=None):
    if subwidgets_center_offset is None:
        subwidgets_center_offset = Point(0,source_widget.size.norm()*scale)
        span = pi
    else:
        span = pi
    source_widget.scale = scale
    subwidgets = reversed(sorted((widget.order.sublevel, widget) for widget in list(subwidgets_of(source_widget))))
    subwidgets = list(subwidgets)
    num = len(subwidgets)
    if num <= 1:
        return
    center_angle = subwidgets_center_offset.angle() - (span/2)
    radius = subwidgets_center_offset.norm()
    angle_step = span/(num-1)
    center = source_widget.pos
    for i,(sublevel, subwidget) in enumerate(subwidgets):
        angle = center_angle + angle_step*i
        subwidget.pos = center + Point.from_polar(angle, radius)
        new_offset = Point.from_polar(angle, radius/3.0)
        SurroundLayout(width, height, subwidget, subwidgets_of, scale=scale*0.8, subwidgets_center_offset=new_offset)
    
