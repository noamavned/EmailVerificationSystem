class Colored(str):
    def __init__(self, text: str):
        self.text = text
        self.additions = []

    def __str__(self):
        codes = ';'.join(self.additions)
        colored_text = f"\033[{codes}m{self.text}\033[0m"
        return colored_text

    def __addColor__(self, a):
        self.additions.append(a)

    # Colors
    def color_black(self):
        self.__addColor__("30")
    def color_red(self):
        self.__addColor__("31")
    def color_green(self):
        self.__addColor__("32")
    def color_yellow(self):
        self.__addColor__("33")
    def color_blue(self):
        self.__addColor__("34")
    def color_magenta(self):
        self.__addColor__("35")
    def color_cyan(self):
        self.__addColor__("36")
    def color_white(self):
        self.__addColor__("37")

    # Background Colors
    def color_bg_black(self):
        self.__addColor__("40")
    def color_bg_red(self):
        self.__addColor__("41")
    def color_bg_green(self):
        self.__addColor__("42")
    def color_bg_yellow(self):
        self.__addColor__("43")
    def color_bg_blue(self):
        self.__addColor__("44")
    def color_bg_magenta(self):
        self.__addColor__("45")
    def color_bg_cyan(self):
        self.__addColor__("46")
    def color_bg_white(self):
        self.__addColor__("47")

    # Text Effects
    def color_bold(self):
        self.__addColor__("1")
    def color_italic(self):
        self.__addColor__("3")
    def color_underline(self):
        self.__addColor__("4")
    def color_strike(self):
        self.__addColor__("9")

x = Colored(__file__)
x.color_blue()
x.color_bold()
print(x)