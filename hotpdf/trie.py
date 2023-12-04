class TrieNode:
    def __init__(self):
        """
        Initialize a TrieNode.

        Attributes:
            children (dict): Mapping of characters to TrieNode objects.
            is_end_of_word (bool): Flag indicating the end of a word.
            coords (list): List of coordinates associated with the word.
        """
        self.children = {}
        self.is_end_of_word = False
        self.coords = None


class Trie:
    def __init__(self):
        """Initialize a Trie."""
        self.root = TrieNode()

    def insert(self, word, coords):
        """
        Insert a word into the Trie.

        Args:
            word (str): The word to insert.
            coords: Coordinates associated with the word.
        """
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
        """
        Search for words in the Trie that match a given text.

        Args:
            text (str): The text to search for.

        Returns:
            tuple: A tuple containing a list of found words and a list of coordinates.
        """
        node = self.root
        found, coords = [], []
        for char in text:
            if char in node.children:
                if node.children[char].is_end_of_word:
                    found.append(char)
                    coords.append(node.children[char].coords)
            node = self.root
        return found, coords
