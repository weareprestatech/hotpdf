from .data.classes import HotCharacter


class TrieNode:
    def __init__(self):
        """
        Initialize a TrieNode.

        Attributes:
            children (dict): Mapping of characters to TrieNode objects.
            is_end_of_word (bool): Flag indicating the end of a word.
            hot_characters (list[HotCharacter]): List of HotCharacter instances associated with the word.
        """
        self.children: dict = {}
        self.is_end_of_word: bool = False
        self.hot_characters: list[HotCharacter] = None


class Trie:
    def __init__(self):
        """Initialize a Trie."""
        self.root = TrieNode()

    def insert(self, word, hot_character: HotCharacter):
        """
        Insert a word into the Trie.

        Args:
            word (str): The word to insert.
            coords: Coordinates associated with the word.
        """
        node: TrieNode = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        if node.hot_characters is not None:
            node.hot_characters = node.hot_characters + [hot_character]
        else:
            node.hot_characters = [hot_character]

    def search_all(self, text):
        """
        Search for words in the Trie that match a given text.

        Args:
            text (str): The text to search for.

        Returns:
            tuple: A tuple containing a list of found words and a list of coordinates.
        """
        node: TrieNode = self.root
        found, hot_characters = [], []
        for char in text:
            if char in node.children:
                if node.children[char].is_end_of_word:
                    found.append(char)
                    hot_characters.append(node.children[char].hot_characters)
            node = self.root
        return found, hot_characters
