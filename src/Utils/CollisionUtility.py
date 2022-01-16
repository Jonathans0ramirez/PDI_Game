def collision_box_check(box_position, box_dimensions, cursor):
    box_pos_x, box_pos_y = box_position
    box_width, box_height = box_dimensions
    cursor_pos_x, cursor_pos_y = cursor
    return_value = True if box_pos_x < cursor_pos_x < (box_pos_x + box_width) and box_pos_y < cursor_pos_y < (
            box_pos_y + box_height) else False
    return return_value
