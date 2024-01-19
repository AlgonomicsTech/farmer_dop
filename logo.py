def print_ALGONOMICS(message):

    patterns = {
        'A': ["  #  ", " # # ", "#####", "#   #", "#   #"],
        'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
        'G': [" ### ", "#   #", "#    ", "#  ##", " ### "],
        'O': [" ### ", "#   #", "#   #", "#   #", " ### "],
        'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
        'M': ["#   #", "## ##", "# # #", "#   #", "#   #"],
        'I': ["#####", "  #  ", "  #  ", "  #  ", "#####"],
        'C': [" ### ", "#    ", "#    ", "#    ", " ### "],
        'S': [" ####", "#    ", " ### ", "    #", "#### "]
    }

    blue_color = '\033[94m'
    reset_color = '\033[0m'

    lines = ['' for _ in range(5)]
    for char in message.upper():

        char_pattern = patterns.get(char, ["?    ", "?    ", "?    ", "?    ", "?    "])
        for i in range(5):
            lines[i] += char_pattern[i] + "    "

    for line in lines:
        print(blue_color + line + reset_color)





