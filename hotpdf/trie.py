from collections import defaultdict

from .data.classes import HotCharacter, PageResult


class TrieNode:
    def __init__(self) -> None:
        """Initialize a TrieNode.

        Args:
            children (dict): Mapping of characters to TrieNode objects.
            is_end_of_word (bool): Flag indicating the end of a word.
            hot_characters (list[HotCharacter]): List of HotCharacter instances associated with the word.
        """
        self.children: defaultdict[str, TrieNode] = defaultdict(TrieNode)
        self.is_end_of_word: bool = False
        self.hot_characters: list[HotCharacter] = []


class Trie:
    def __init__(self) -> None:
        """Initialize a Trie."""
        self.root = TrieNode()

    def insert(self, word: str, hot_character: HotCharacter) -> None:
        """Insert a word and a HotCharacter into the Trie.

        Args:
            word (str): The word to insert.
            hot_character (HotCharacter): The HotCharacter to insert.
        """
        node: TrieNode = self.root
        for char in word:
            node = node.children[char]
        node.is_end_of_word = True
        node.hot_characters = node.hot_characters + [hot_character]

    def search_all(self, text: str) -> tuple[list[str], PageResult]:
        """Search for words in the Trie that match a given text.

        Args:
            text (str): The text to search for.

        Returns:
            tuple: A tuple containing a list of the target characters found and corresponding PageResult.
        """
        node: TrieNode = self.root
        found: list[str] = []
        hot_characters: PageResult = []
        for char in text:
            if char in node.children and node.children[char].is_end_of_word:
                found.append(char)
                if node.children[char].hot_characters:
                    hot_characters.append(node.children[char].hot_characters)
            node = self.root
        return found, hot_characters
