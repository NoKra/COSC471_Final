
# instead of hard-coding the sizes and connections, using classes to build the printer parts
# probably best to have head_height and head_length be even in size
class PrinterHead:
    def __init__(self, dimension, x_offset, current_x, current_y):
        self.__x_offset = x_offset
        self.__current_x = current_x
        self.__current_y = current_y

        self.__head_width = dimension / 5
        self.__head_height = dimension / 2
        self.__head_length = dimension / 2

        self.__main_box = self.__create_main_box()
        self.__fan_box = self.__create_fan_box()
        self.__nozzle = self.__create_nozzle()
        self.__carriage_block = self.__create_carriage_block()
        self.all_parts = (self.__main_box, self.__fan_box, self.__nozzle, self.__carriage_block)

    def get_nozzle_position(self):
        return self.__nozzle[0][42]

    def __create_main_box(self):
        right_bottom_back = (self.__head_width + self.__current_x + self.__x_offset, -self.__head_height + self.__current_y, -self.__head_length)
        right_top_back = (self.__head_width + self.__current_x + self.__x_offset, self.__head_height + self.__current_y, -self.__head_length)
        left_top_back = (-self.__head_width + self.__current_x + self.__x_offset, self.__head_height + self.__current_y, -self.__head_length)
        left_bottom_back = (-self.__head_width + self.__current_x + self.__x_offset, -self.__head_height + self.__current_y, -self.__head_length)
        right_bottom_front = (self.__head_width + self.__current_x + self.__x_offset, -self.__head_height + self.__current_y, self.__head_length)
        right_top_front = (self.__head_width + self.__current_x + self.__x_offset, self.__head_height + self.__current_y, self.__head_length)
        left_bottom_front = (-self.__head_width + self.__current_x + self.__x_offset, -self.__head_height + self.__current_y, self.__head_length)
        left_top_front = (-self.__head_width + self.__current_x + self.__x_offset, self.__head_height + self.__current_y, self.__head_length)

        vertices = (
            right_bottom_back,  # 0
            right_top_back,  # 1
            left_top_back,  # 2
            left_bottom_back,  # 3
            right_bottom_front,  # 4
            right_top_front,  # 5
            left_bottom_front,  # 6
            left_top_front  # 7
        )

        edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)
        )
        return vertices, edges

    def __create_fan_box(self):
        offset = self.__head_height / 2.5 # Used for constant distance measurements
        # Box attachment points
        box_left_bottom_front = self.__main_box[0][6]
        box_left_top_front = self.__main_box[0][7]
        box_left_bottom_back = self.__main_box[0][3]
        box_left_top_back = self.__main_box[0][2]
        # Fan attachment points
        bottom_front_connection = (box_left_bottom_front[0], box_left_bottom_front[1] + offset, box_left_bottom_front[2] - offset)
        top_front_connection = (box_left_top_front[0], box_left_top_front[1] - offset, box_left_top_front[2] - offset)
        bottom_back_connection = (box_left_bottom_back[0], box_left_bottom_back[1] + offset, box_left_bottom_back[2] + offset)
        top_back_connection = (box_left_top_back[0], box_left_top_back[1] - offset, box_left_top_back[2] + offset)
        # Fan body points
        bottom_front_fan = (bottom_front_connection[0] - offset, bottom_front_connection[1], bottom_front_connection[2])
        top_front_fan = (top_front_connection[0] - offset, top_front_connection[1], top_front_connection[2])
        bottom_back_fan = (bottom_back_connection[0] - offset, bottom_back_connection[1], bottom_back_connection[2])
        top_back_fan = (top_back_connection[0] - offset, top_back_connection[1], top_back_connection[2])

        vertices = (
            box_left_bottom_front,  # 0
            box_left_top_front,  # 1
            box_left_bottom_back,  # 2
            box_left_top_back,  # 3
            bottom_front_connection,  # 4
            top_front_connection,  # 5
            bottom_back_connection,  # 6
            top_back_connection,  # 7
            bottom_front_fan,  # 8
            top_front_fan,  # 9
            bottom_back_fan,  # 10
            top_back_fan  # 11
        )

        edges = (
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
            (4, 8),
            (5, 9),
            (6, 10),
            (7, 11),
            (8, 9),
            (8, 10),
            (9, 11),
            (10, 11)
        )
        return vertices, edges

    def __create_nozzle(self):
        offset = self.__head_length / 2.5
        # Box attachment points
        box_left_front = self.__main_box[0][6]
        box_right_front = self.__main_box[0][4]
        box_left_back = self.__main_box[0][3]
        box_right_back = self.__main_box[0][0]
        # Stem attachment points
        left_front_attach = (box_left_front[0] + (offset * .6), box_left_front[1], box_left_front[2] - offset)
        right_front_attach = (box_right_front[0] - (offset * .6), box_right_front[1], box_right_front[2] - offset)
        left_back_attach = (box_left_back[0] + (offset * .6), box_left_back[1], left_front_attach[2] - offset)
        right_back_attach = (box_right_back[0] - (offset * .6), box_right_back[1], right_front_attach[2] - offset)
        # Stem length points
        left_front_stem = (left_front_attach[0], left_front_attach[1] - (offset / 2), left_front_attach[2])
        right_front_stem = (right_front_attach[0], right_front_attach[1] - (offset / 2), right_front_attach[2])
        left_back_stem = (left_back_attach[0], left_back_attach[1] - (offset / 2), left_back_attach[2])
        right_back_stem = (right_back_attach[0], right_back_attach[1] - (offset / 2), right_back_attach[2])
        # Heat sink top points
        left_front_sink_top = (box_left_front[0], left_front_stem[1], box_left_front[2])
        right_front_sink_top = (box_right_front[0], right_front_stem[1], box_right_front[2])
        left_back_sink_top = (box_left_back[0], left_back_stem[1], left_back_stem[2] - offset)
        right_back_sink_top = (box_right_back[0], right_back_stem[1], right_back_stem[2] - offset)
        # Heat sink bottom points
        left_front_sink_bottom = (left_front_sink_top[0], left_front_sink_top[1] - (offset / 2), left_front_sink_top[2])
        right_front_sink_bottom = (right_front_sink_top[0], right_front_sink_top[1] - (offset / 2), right_front_sink_top[2])
        left_back_sink_bottom = (left_back_sink_top[0], left_back_sink_top[1] - (offset / 2), left_back_sink_top[2])
        right_back_sink_bottom = (right_back_sink_top[0], right_back_sink_top[1] - (offset / 2), right_back_sink_top[2])
        left_mid_sink_bottom = (left_front_sink_bottom[0], left_back_sink_bottom[1] - (offset / 2), left_back_stem[2])
        right_mid_sink_bottom = (right_front_sink_bottom[0], right_back_sink_bottom[1] - (offset / 2), right_back_stem[2])
        # Nozzle attachment points (y coordinates are temporary, may do some linear interpolation)
        left_front_nozzle_top = (left_front_sink_bottom[0] + (offset / 2), left_front_sink_bottom[1] - offset / 3, left_front_sink_bottom[2] - (offset / 2))
        right_front_nozzle_top = (right_front_sink_bottom[0] - (offset / 2), right_front_sink_bottom[1] - offset / 3, right_front_sink_bottom[2] - (offset / 2))
        mid_front_nozzle_top = (0 + self.__current_x + self.__x_offset, left_front_sink_bottom[1] - offset / 3, left_front_nozzle_top[2] + (offset / 4))
        mid_front_sink_attach = (0 + self.__current_x + self.__x_offset, left_front_sink_bottom[1], left_front_sink_bottom[2])
        left_back_nozzle_top = (left_front_nozzle_top[0], left_front_nozzle_top[1], left_front_nozzle_top[2] - (offset / 2))
        right_back_nozzle_top = (right_front_nozzle_top[0], right_front_nozzle_top[1], right_front_nozzle_top[2] - (offset / 2))
        mid_back_nozzle_top = (0 + self.__current_x + self.__x_offset, left_front_nozzle_top[1], left_back_nozzle_top[2] - (offset / 4))
        mid_back_sink_attach = (0 + self.__current_x + self.__x_offset, left_mid_sink_bottom[1], left_mid_sink_bottom[2])
        # Nozzle body points
        left_front_nozzle_bottom = (left_front_nozzle_top[0], left_front_nozzle_top[1] - (offset / 2), left_front_nozzle_top[2])
        right_front_nozzle_bottom = (right_front_nozzle_top[0], right_front_nozzle_top[1] - (offset / 2), right_front_nozzle_top[2])
        mid_front_nozzle_bottom = (0 + self.__current_x + self.__x_offset, mid_back_nozzle_top[1] - (offset / 2), mid_front_nozzle_top[2])
        left_back_nozzle_bottom = (left_back_nozzle_top[0], left_back_nozzle_top[1] - (offset / 2), left_back_nozzle_top[2])
        right_back_nozzle_bottom = (right_back_nozzle_top[0], right_back_nozzle_top[1] - (offset / 2), right_back_nozzle_top[2])
        mid_back_nozzle_bottom = (0 + self.__current_x + self.__x_offset, mid_back_nozzle_top[1] - (offset / 2), mid_back_nozzle_top[2])
        # Nozzle tip points
        left_front_tip_attach = (left_front_nozzle_bottom[0] + (offset / 6), left_front_nozzle_bottom[1], left_front_nozzle_bottom[2] - (offset / 6))
        right_front_tip_attach = (right_front_nozzle_bottom[0] - (offset / 6), right_front_nozzle_bottom[1], right_front_nozzle_bottom[2] - (offset / 6))
        mid_front_tip_attach = (0 + self.__current_x + self.__x_offset, mid_front_nozzle_bottom[1], mid_front_nozzle_bottom[2] - (offset / 6))
        left_back_tip_attach = (left_back_nozzle_bottom[0] + (offset / 6), left_back_nozzle_bottom[1], left_back_nozzle_bottom[2] + (offset / 6))
        right_back_tip_attach = (right_back_nozzle_bottom[0] - (offset / 6), right_back_nozzle_bottom[1], right_back_nozzle_bottom[2] + (offset / 6))
        mid_back_tip_attach = (0 + self.__current_x + self.__x_offset, mid_back_nozzle_bottom[1], mid_back_nozzle_bottom[2] + (offset / 6))
        nozzle_tip = (0 + self.__current_x + self.__x_offset, mid_front_tip_attach[1] - (offset / 3), left_front_nozzle_bottom[2] - (offset / 4))

        vertices = (
            box_left_front,  # 0
            box_right_front,  # 1
            box_left_back,  # 2
            box_right_back,  # 3
            left_front_attach,  # 4
            right_front_attach,  # 5
            left_back_attach,  # 6
            right_back_attach,  # 7
            left_front_stem,  # 8
            right_front_stem,  # 9
            left_back_stem,  # 10
            right_back_stem,  # 11
            left_front_sink_top,  # 12
            right_front_sink_top,  # 13
            left_back_sink_top,  # 14
            right_back_sink_top,  # 15
            left_front_sink_bottom,  # 16
            right_front_sink_bottom,  # 17
            left_back_sink_bottom,  # 18
            right_back_sink_bottom,  # 19
            left_mid_sink_bottom,  # 20
            right_mid_sink_bottom,  # 21
            left_front_nozzle_top,  # 22
            right_front_nozzle_top,  # 23
            mid_front_nozzle_top,  # 24
            mid_front_sink_attach,  # 25
            left_back_nozzle_top,  # 26
            right_back_nozzle_top,  # 27
            mid_back_nozzle_top,  # 28
            mid_back_sink_attach,  # 29
            left_front_nozzle_bottom,  # 30
            right_front_nozzle_bottom,  # 31
            mid_front_nozzle_bottom,  # 32
            left_back_nozzle_bottom,  # 33
            right_back_nozzle_bottom,  # 34
            mid_back_nozzle_bottom,  # 35
            left_front_tip_attach,  # 36
            right_front_tip_attach,  # 37
            mid_front_tip_attach,  # 38
            left_back_tip_attach,  # 39
            right_back_tip_attach,  # 40
            mid_back_tip_attach,  # 41
            nozzle_tip,  # 42
        )

        edges = (
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
            (4, 8),
            (5, 9),
            (6, 10),
            (7, 11),
            (8, 9),
            (8, 10),
            (9, 11),
            (10, 11),
            (8, 12),
            (9, 13),
            (10, 14),
            (11, 15),
            (12, 13),
            (12, 14),
            (13, 15),
            (14, 15),
            (12, 16),
            (13, 17),
            (14, 18),
            (15, 19),
            (16, 17),
            (18, 19),
            (16, 20),
            (18, 20),
            (17, 21),
            (19, 21),
            (20, 21),
            (16, 22),
            (17, 23),
            (22, 24),
            (23, 24),
            (24, 25),
            (20, 26),
            (22, 26),
            (21, 27),
            (23, 27),
            (26, 28),
            (27, 28),
            (28, 29),
            (22, 30),
            (23, 31),
            (24, 32),
            (26, 33),
            (27, 34),
            (28, 35),
            (30, 32),
            (31, 32),
            (30, 33),
            (31, 34),
            (33, 35),
            (34, 35),
            (30, 36),
            (31, 37),
            (32, 38),
            (33, 39),
            (34, 40),
            (35, 41),
            (36, 38),
            (37, 38),
            (36, 39),
            (37, 40),
            (39, 41),
            (40, 41),
            (36, 42),
            (37, 42),
            (38, 42),
            (39, 42),
            (40, 42),
            (41, 42)

        )
        return vertices, edges


    def __create_carriage_block(self):
        offset = self.__head_length / 1.5
        # Box attachment points
        box_left_top_back = self.__main_box[0][2]
        box_right_top_back = self.__main_box[0][1]
        box_left_bottom_back = self.__main_box[0][3]
        box_right_bottom_back = self.__main_box[0][0]
        # Carriage body
        body_left_top = (box_left_top_back[0], box_left_top_back[1], box_left_top_back[2] - offset)
        body_mid_left_top_anchor = (box_left_top_back[0], box_left_top_back[1], box_left_top_back[2] - offset / 2)
        body_right_top = (box_right_top_back[0], box_right_top_back[1], box_right_top_back[2] - offset)
        body_mid_right_top_anchor = (box_right_top_back[0], box_right_top_back[1], box_right_top_back[2] - offset / 2)
        body_left_bottom = (box_left_bottom_back[0], box_left_bottom_back[1], box_left_bottom_back[2] - offset)
        body_mid_left_bottom_anchor = (box_left_bottom_back[0], box_left_bottom_back[1], box_left_bottom_back[2] - offset / 2)
        body_right_bottom = (box_right_bottom_back[0], box_right_bottom_back[1], box_right_bottom_back[2] - offset)
        body_mid_right_bottom_anchor = (box_right_bottom_back[0], box_right_bottom_back[1], box_right_bottom_back[2] - offset / 2)
        # figure out the mid-point, probably height / 2 of the main box or something
        body_left_mid_top_anchor = (body_left_top[0], body_left_top[1], body_left_top[2])
        body_left_mid_bottom_anchor = (body_left_bottom[0], body_left_bottom[1], body_left_bottom[2])
        body_right_mid_top_anchor = (body_right_top[0], body_right_top[1], body_right_top[2])
        body_right_mid_bottom_anchor = (body_right_bottom[0], body_right_bottom[1], body_right_bottom[2])
        # Guide rod bearing top (abbr. tbl = top bearing left, bbl = bottom bearing left, etc.)
        tbl_mid_top_attach = (body_left_top[0], body_left_top[1] - offset / 3, body_left_top[2] + (offset / 2))
        tbl_left_top_attach = (tbl_mid_top_attach[0], tbl_mid_top_attach[1] - offset / 2, tbl_mid_top_attach[2] - offset / 3)
        tbl_left_one_top_attach = (tbl_mid_top_attach[0], tbl_left_top_attach[1] + offset / 2.5, tbl_left_top_attach[2] + offset / 5)
        tbl_left_two_top_attach = (tbl_mid_top_attach[0], tbl_left_top_attach[1] + offset / 5, tbl_left_top_attach[2] + offset / 15)
        body_left_top_mid_back_anchor = (tbl_left_top_attach[0], tbl_left_top_attach[1], body_left_top[2])
        tbl_right_top_attach = (tbl_mid_top_attach[0], tbl_mid_top_attach[1] - offset / 2, tbl_mid_top_attach[2] + offset / 3)
        tbl_right_one_top_attach = (tbl_mid_top_attach[0], tbl_right_top_attach[1] + offset / 2.5, tbl_right_top_attach[2] - offset / 5)
        tbl_right_two_top_attach = (tbl_mid_top_attach[0], tbl_right_top_attach[1] + offset / 5, tbl_right_top_attach[2] - offset / 15)
        body_right_top_mid_back_anchor = (tbl_left_top_attach[0], tbl_right_top_attach[1], box_left_top_back[2])




        vertices = (
            box_left_top_back,  # 0
            box_right_top_back,  # 1
            box_left_bottom_back,  # 2
            box_right_bottom_back,  # 3
            body_left_top,  # 4
            body_right_top,  # 5
            body_left_bottom,  # 6
            body_right_bottom,  # 7
            body_mid_left_top_anchor,  # 8,
            body_mid_right_top_anchor,  # 9
            body_mid_left_bottom_anchor,  # 10
            body_mid_right_bottom_anchor,  # 11
            body_left_mid_top_anchor,  # 12
            body_left_mid_bottom_anchor,  # 13
            body_right_mid_top_anchor,  # 14
            body_right_mid_bottom_anchor,  # 15
            tbl_mid_top_attach,  # 16
            tbl_left_one_top_attach,  # 17
            tbl_left_two_top_attach,  # 18
            tbl_left_top_attach,  # 19
            body_left_top_mid_back_anchor,  # 20
            tbl_right_one_top_attach,  # 21
            tbl_right_two_top_attach,  # 22
            tbl_right_top_attach,  # 23
            body_right_top_mid_back_anchor,  # 24
        )

        edges = (
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
            #(8, 16), using a simplified version of the carriabe block for now, bearings seemed too busy
            #(16, 17),
            #(4, 17),
            #(17, 18),
            #(4, 18),
            #(18, 19),
            #(19, 20),
            #(16, 21),
            #(0, 21),
            #(21, 22),
            #(0, 22),
            #(22, 23),
            #(23, 24)
        )

        return vertices, edges
