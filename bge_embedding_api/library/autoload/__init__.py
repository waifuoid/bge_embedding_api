import os
import sys


class LoadFile:
    root_path = sys.path[0]
    __ignore = [".DS_Store", "__pycache__"]

    def __init__(self, callback, ends=""):
        self.callback = callback
        self.ends = ends + ".py"

    def loop_up(self, relative):

        absolute = self.root_path + "/" + relative
        files = os.listdir(absolute)

        for file in files:
            if file not in LoadFile.__ignore:
                filepath = absolute + "/" + file

                if os.path.isfile(filepath):
                    if self.ends is not None:
                        if file.endswith(self.ends):
                            self.__callback(self.__str_link(relative, file))
                    else:
                        self.__callback(self.__str_link(relative, file))
                else:
                    self.loop_up(self.__str_link(relative, file))

    @staticmethod
    def __str_link(relative, filename):
        if filename == 'param.py':
            return relative
        if relative is None or len(relative) == 0:
            return filename
        return relative + "/" + filename

    def __callback(self, relative):
        if relative.endswith(".py"):
            relative = relative[:-3]
        packet = relative.replace("/", ".")
        self.callback(packet)
