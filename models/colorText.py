from termcolor import colored


class ColorText:
    def __init__(self, text):
        self.text = text

    def color_words(self, dict_color):
        for word_l, color in (dict_color.items()):
            for word in word_l:
                self.text = self.text.replace(word, colored(word, color))
        return self.text


if __name__ == "__main__":
    text = "a b c d"
    c = ColorText(text)
    print(c.color_words({('a'): 'red', ('b'): 'blue', ('c'): 'grey', ('d'): 'yellow'}))
