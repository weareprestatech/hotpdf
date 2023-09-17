import math
import xml.etree.ElementTree as ET
from .trie import Trie

class MemoryMap:
    def __init__(self, width=0, height=0, precision=0.5):
        self.height = height
        self.width = width
        self.precision = precision
        self.text_trie = Trie()

    def build_memory_map(self):
        num_columns = int((self.height) / self.precision)
        num_rows = int((self.width) / self.precision)
        self.memory_map = [["" for _ in range(num_rows)] for _ in range(num_columns)]

    def display_memory_map(self, save=False, filename="memory_map.txt"):
        memory_map_str = ""
        if hasattr(self, "memory_map"):
            for row in range(len(self.memory_map)):
                for col in range(len(self.memory_map[row])):
                    memory_map_str += self.memory_map[row][col]
                memory_map_str += "\n"
        else:
            raise Exception("Memory map not built yet!")

        if save:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(memory_map_str)
        else:
            print(memory_map_str)

    def load_memory_map(self, page, format="xml"):
        if  not hasattr(self, "memory_map"):
            raise Exception("Memory map not built yet!")

        root = ET.fromstring(page)
        char_instances = []

        for char in root.findall(".//char"):
            char_x = float(char.attrib["x"])
            char_y = float(char.attrib["y"])
            char_c = char.attrib["c"]
            quads = char.attrib["quad"].split()
            char_x_end = float(quads[2])
            # Calculate the cell coordinates
            cell_x = int(math.ceil(char_x))
            cell_y = int(math.ceil((self.height - char_y)))

            # Update the MemoryMap with the character
            if self.memory_map[cell_y][cell_x] != "":
                cell_x += 1
            self.memory_map[cell_y][cell_x] = char_c
            char_instances.append((char_c, {"x": cell_x, "y": cell_y, "x_end": char_x_end}))

        for char_c, coords in char_instances:
            self.text_trie.insert(char_c, coords)

    def extract_text_from_bbox(self, x0, x1, y0, y1):
        if not hasattr(self, "memory_map"):
            raise Exception("Memory map not built!")

        # Convert coordinates to cell indices
        cell_x0 = int(math.floor(x0))
        cell_x1 = int(math.ceil(x1))
        cell_y0 = int(math.floor(y0))
        cell_y1 = int(math.ceil(y1))

        # Extract text within the specified bounding box
        extracted_text = ""
        for row in range(cell_y0, cell_y1 + 1):
            if row >= 0 and row < len(self.memory_map):
                for col in range(cell_x0, cell_x1 + 1):
                    if col >= 0 and col < len(self.memory_map[row]):
                        extracted_text += self.memory_map[row][col]

        return extracted_text

    def find_text(self, query):
        found_text = self.text_trie.search_all(query)
        return found_text
