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


