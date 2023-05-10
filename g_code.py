from queue import Queue

class GCode:
    def __init__(self, printer, file_name):
        self.printer = printer
        self.__file_name = file_name
        self.__all_lines = self.__file_to_array()
        self.command_queue = Queue(maxsize=0)

    def __file_to_array(self):
        file = open(self.__file_name, "r")
        lines = file.readlines()
        file.close()
        return lines

    def populate_command_queue(self):
        g_90_count = 0  # G90 sets the mode to absolute-positioning, the 2nd G90 seems to start the actual print (maybe)
        for line in self.__all_lines:
            if g_90_count != 2 and line[:3] == "G90":
                g_90_count += 1
            if g_90_count == 2 and line[:2] == "G1":
                self.command_queue.put(line)

    def process_g_code(self):
        command = self.command_queue.get()
        print("Processing: %s" % command)
        code_x = 0
        code_y = 0
        code_z = 0
        extrude = False
        parameters = command[2:].split()
        for param in parameters:
            match param[:1]:
                case "F":
                    self.printer.adjust_feed_rate(param[1:])
                case "X":
                    code_x = param[1:]
                case "Y":
                    code_y = param[1:]
                case "Z":
                    code_z = param[1:]
                case "E":
                    extrude = True
        if code_x != 0 or code_y != 0:
            self.printer.g_code_plane_movement((code_x, code_y, extrude))
        elif code_z != 0:
            self.printer.g_code_layer_movement(code_z)

