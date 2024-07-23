import re
from typing import List


class EncoderDecoder:
    def __init__(self, n_encoding: int = 812):
        self.char_set = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            ".", " "
        ]
        self.n_encoding = n_encoding
        self.top_n = n_encoding - len(self.char_set)
        self.encode_map = {char: i for i, char in enumerate(self.char_set)}
        self.decode_map = {i: char for i, char in enumerate(self.char_set)}
        self.encode_word_map = {}
        self.decode_word_map = {}

    def split_words_chars(self, text: str) -> None:
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
        sorted_words = sorted(word_char_counts.items(), key=lambda item: item[1], reverse=True)
        # map top words to number of available integers
        top_words = sorted_words[:self.top_n]
        for i, (word, _) in enumerate(top_words):
            self.encode_word_map[word] = i
            self.decode_word_map[i] = word

    def encode(self, raw_string: str) -> List[int]:
        self.create_top_word_map(text=raw_string)
        encoded = []
        # split raw string into words and chars 
        strs = self.split_words_chars(raw_string)

        for str in strs:
            # encode top words using word map
            if str in self.encode_word_map:
                encoded.append(self.encode_word_map[str])
            # encode other chars with map
            else:
                for char in str:
                    encoded.append(self.encode_map[char])

        return encoded

    def decode(self, encoded: List[int]) -> str:
        decoded = ''
        for code in encoded:
            # decode using word map
            decoded += self.decode_word_map[code]

        return decoded


if __name__ == '__main__':

    file_path = '/home/encode-decode/shakespeare.txt'
    with open(file_path, 'r') as file:
        shakespeare_text = file.read()

    encoder_decoder = EncoderDecoder()

    encoded = encoder_decoder.encode(raw_string=shakespeare_text)
    decoded = encoder_decoder.decode(encoded)

    print(decoded == shakespeare_text)


        
        # # Calculate characters saved (frequency * length)
        # words_with_savings = [(word, count, count * len(word)) for word, count in word_counts.items()]
        # # Sort by characters saved in descending order
        # sorted_words = sorted(words_with_savings, key=lambda x: x[2], reverse=True)
        # top_words = sorted_words[:top_n]
        
        # # Create a map for top words
        # for idx, (word, _, _) in enumerate(top_words):
        #     self.word_map[word] = idx
        #     self.reverse_word_map[idx] = word

    
     