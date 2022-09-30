# #########################################################################
# MARKDOWN EDITOR
# tags:[]
#
# This module implements a function that creates a markdown document
# using formatting commands provided by the user and saves the file.
# #########################################################################=

# List of markdown formatters
MD_FORMATTERS = [
    "plain", "bold", "italic", "header", "link", "inline-code", "new-line",
    "ordered-list", "unordered-list"
]

# List of markdown special commands
SPECIAL_CMD = ["!help", "!done"]

#   Formatter functions
#   The functions are subdivided for lists (ordered and unordered lists),
#   headers and link. The link function implements the validation for the
#   link
#   ==================================================


def formatter_func(user_input, text_format):
    """Applies selected formatter to text entered by user except the header, new line, ordered and unordered list

    Args:
        text_format (str): Formatter to be applied.
        user_input (str): Text to be formatted.

    Returns:
        md_text: Formatted text.
    """
    if text_format == "plain":
        md_text = user_input
    elif text_format == "bold":  # bold
        md_text = "**" + user_input + "**"
    elif text_format == "italic":  # italic
        md_text = "*" + user_input + "*"
    elif text_format == "link":  # link
        md_text = "[" + user_input[0] + "](" + user_input[1] + ")"
    elif text_format == "inline-code":  # inline-code
        md_text = "`" + user_input + "`"
    return md_text


def format_link():
    """Set the input values for link 

    Returns:
        Label: label of the link set by user
        URL: link provided by user that starts with http
    """
    label = input("Label: ")
    url = input("URL: ")
    while not url.startswith("http"):
        print("The URL should start with http")
        url = input("URL: ")
    return (label, url)


def list_func(list_formatter):
    """Applies selected formatter to text.

    Returns:
        md_text: Formatted text.
    """
    number_of_rows = int(input("Enter number of rows: "))
    while number_of_rows <= 0:
        print("The number of rows should be greater than zero")
        number_of_rows = int(input("Enter number of rows: "))

    formatted_list = []
    for row in range(number_of_rows):
        formatted_item = list_input((row + 1), list_formatter)
        formatted_list.append(formatted_item)
    return formatted_list


def list_input(idx, formatter):
    """Formats ordered and unordered list

    Args:
        idx(int): The row number
        formatter(str): the selected formatter
    """
    text = input(f"Row #{idx}: ")
    if formatter == "unordered-list":
        return "* " + text + "\n"
    return str(idx) + ". " + text + "\n"


def format_headers():
    """Format headings of markdown

    Returns:
        header_level: heading level
        Text: the header text    
    """
    header_level = int(input("Level: "))
    while header_level not in range(1, 6):
        print("The level should be within the range of 1 to 6")
        header_level = int(input("Level: "))  # input

    header_txt = input("Text: ")
    md_text = "#" * header_level + " " + header_txt + "\n"
    return md_text


# =============================================================
#               Main Program
# ==============================================================
FORMATTER = ''
INPUT_ = ''
MARKDOWN_TXT = ''

while FORMATTER != "!done":
    # Request user input
    FORMATTER = input("Choose a formatter: ")

    if FORMATTER in (MD_FORMATTERS + SPECIAL_CMD):
        # Check if user input is a valid formatter
        if FORMATTER in MD_FORMATTERS:
            # list markdown
            if (FORMATTER == "ordered-list" or FORMATTER == "unordered-list"):
                list_of_items = list_func(FORMATTER)
                for item in list_of_items:
                    MARKDOWN_TXT += item
            # headers
            elif FORMATTER == "header":
                MARKDOWN_TXT += format_headers()
            # new line
            elif FORMATTER == "new-line":
                MARKDOWN_TXT += "\n"
            else:
                # link
                if FORMATTER == "link":
                    INPUT_ = format_link()
                else:
                    INPUT_ = input("Text: ")
                MARKDOWN_TXT += formatter_func(INPUT_, FORMATTER)

        elif FORMATTER in SPECIAL_CMD:
            if FORMATTER == "!help":
                print("Available formatters: " + " ".join(MD_FORMATTERS))
                print("Available special commands: " + " ".join(SPECIAL_CMD))
            elif FORMATTER == "!done":
                # Send the output to markdown file
                output = open("./output.md", "w", encoding="utf-8")
                output.writelines(MARKDOWN_TXT)
                output.close()
    else:
        print("Unknown formatting type or command.")
    print(MARKDOWN_TXT)
