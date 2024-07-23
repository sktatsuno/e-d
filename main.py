import re
from typing import List


class EncoderDecoder:
    def __init__(self, n_encoding: int = 812):
        self.char_set = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            ".", ",", "!", "?", ":", ";", "-", "Æ", "—", "‘",
            "_", "@", "#", "$", "%", "^", "&", "“", "’", "”", "<", ">", "/",
            "\\", "|", "~", "`", "\"", "'", " ", "\n"
        ]
        self.char_set_len = len(self.char_set)
        self.n_encoding = n_encoding
        self.top_n = n_encoding - self.char_set_len
        self.encode_map = {char: i for i, char in enumerate(self.char_set)}
        self.decode_map = {i: char for i, char in enumerate(self.char_set)}
        self.encode_word_map = {}
        self.decode_word_map = {}

    def split_words_chars(self, text: str) -> List[str]:
        pattern = re.compile(r'(\w+|\s+|[^\w\s])')
        result = pattern.findall(text)
        return result

    def create_top_word_map(self, text: str) -> None:
        # extract words
        words = text.split()
        # each time a word shows up tally its char length
        word_char_counts = {}
        for word in words:
            if word in word_char_counts:
                word_char_counts[word] += len(word)
            else:
                word_char_counts[word] = len(word)
        # sort by total characters in text descending
        sorted_words = sorted(word_char_counts.items(),
                              key=lambda item: item[1],
                              reverse=True)
        # map top words to number of available integers
        top_words = sorted_words[:self.top_n]
        for i, (word, _) in enumerate(top_words):
            # offset word map indices by len of char set
            self.encode_word_map[word] = i + self.char_set_len
            self.decode_word_map[i + self.char_set_len] = word

    def encode(self, raw_string: str) -> List[int]:
        self.create_top_word_map(text=raw_string)
        encoded = []
        # split raw string into words and chars 
        strings = self.split_words_chars(raw_string)

        for string in strings:
            # encode top words using word map
            if string in self.encode_word_map:
                encoded.append(self.encode_word_map[string])
            # encode other chars with map
            else:
                for char in string:
                    encoded.append(self.encode_map[char])

        return encoded

    def decode(self, encoded: List[int]) -> str:
        decoded = []
        for code in encoded:
            # decode top words using word map
            if code in self.decode_word_map:
                decoded.append(self.decode_word_map[code])
            # decode other chars with map
            else:
                decoded.append(self.decode_map[code])

        return ''.join(decoded)


if __name__ == '__main__':

    file_path = '../encode-decode/shakespeare.txt'
    with open(file_path, 'r') as file:
        shakespeare_text = file.read()

    encoder_decoder = EncoderDecoder()

    encoded = encoder_decoder.encode(raw_string=shakespeare_text)
    decoded = encoder_decoder.decode(encoded)

    print(decoded == shakespeare_text)
