class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.coords = None


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
        if node.coords is not None:
            node.coords = node.coords + [coords]
        else:
            node.coords = [coords]

    def search_all(self, text):
        node = self.root
        found = []
        current_match = []
        coords = []
        for char in text:
            if char in node.children:
                current_match.append(char)
                node = node.children[char]
                if node.is_end_of_word:
                    found.append("".join(current_match))
                    coords.append(node.coords)
            else:
                if current_match:
                    found.extend(char)
                    coords.append(node.coords)
                    current_match = []
                node = self.root  # Reset to the root

        return found, coords
