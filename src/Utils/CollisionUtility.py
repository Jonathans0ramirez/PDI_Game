def collision_box_check(box_position, box_dimensions, cursor):
    box_pos_x, box_pos_y = box_position
    box_width, box_height = box_dimensions
    cursor_pos_x, cursor_pos_y = cursor
    return_value = True if box_pos_x < cursor_pos_x < (box_pos_x + box_width) and box_pos_y < cursor_pos_y < (
            box_pos_y + box_height) else False
    return return_value


def collision_circle_check(center, radius, cursor):
    center_x, center_y = center
    cursor_pos_x, cursor_pos_y = cursor
    return_value = (cursor_pos_x - center_x) ** 2 + (cursor_pos_y - center_y) ** 2 < radius ** 2
    return return_value
