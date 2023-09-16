class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.coords = {"x": 0, "y": 0}


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
