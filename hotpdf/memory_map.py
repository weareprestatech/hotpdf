import math
import xml.etree.ElementTree as ET


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.coords = {'x': 0, 'y': 0}


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, coords):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.coords = coords

    def search_all(self, text):
        node = self.root
        found = []
        current_match = []
        coords = []
        for char in text:
            if char in node.children:
                current_match.append(char)
                node = node.children[char]
                coords.append(node.coords)
                if node.is_end_of_word:
                    found.append("".join(current_match))
            else:
                if current_match:
                    found.extend(char)
                    coords.append(node.coords)
                    current_match = []
                node = self.root  # Reset to the root

        return found, coords


class MemoryMap:
    def __init__(self, xmin=0, ymin=0, xmax=0, ymax=0, precision=0.5):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.precision = precision
        self.text_trie = Trie()

    def build_memory_map(self):
        num_x_cells = int(self.xmax / self.precision)
        num_y_cells = int(self.ymax / self.precision)
        self.memory_map = [["" for _ in range(num_x_cells)] for _ in range(num_y_cells)]

    def display_memory_map(self, save=False, filename="memory_map.txt"):
        memory_map_str = ""
        if hasattr(self, "memory_map"):
            for row in range(len(self.memory_map)):
                for col in range(len(self.memory_map[row])):
                    memory_map_str += self.memory_map[row][col]
                memory_map_str += "\n"
        else:
            print("Memory Map not built yet!")

        if save:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(memory_map_str)
        else:
            print(memory_map_str)

    def load_memory_map(self, pages, format="xml"):
        for page in pages:
            root = ET.fromstring(page)
            for char in root.findall(".//char"):
                char_x = float(char.attrib["x"])
                char_y = float(char.attrib["y"])
                char_c = char.attrib["c"]

                # Calculate the cell coordinates
                cell_x = int(math.ceil(char_x))
                cell_y = int(math.ceil((self.ymax - char_y)))

                # Update the MemoryMap with the character
                if self.memory_map[cell_y][cell_x] != "":
                    cell_x += 1
                self.memory_map[cell_y][cell_x] = char_c
                self.text_trie.insert(char_c, {'x': cell_x, 'y': cell_y})

    def extract_text_from_bbox(self, x0, x1, y0, y1):
        if not hasattr(self, "memory_map"):
            print("Memory Map not built yet!")
            return ""

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
        found_text, coords = self.text_trie.search_all(query)
        return "".join(found_text), coords
