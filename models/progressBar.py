class ProgressBar():
    def __init__(self, total):
        self.total = total

    def print_bar_progress(self, count):
        bar_prog_float = count * 100 / self.total
        bar_prog_int = int(bar_prog_float)
        print("|{}{}| {}%".format("█" * int(bar_prog_int / 2), "-" * (50 - int(bar_prog_int / 2)), round(bar_prog_float, 1)), end="")
