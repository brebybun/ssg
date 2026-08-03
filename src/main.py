from textnode import TextNode, TextType

def main():
    print("hello world")
    dummy = TextNode("Text for the text monster", TextType.LINK, "https://google.com")
    print(dummy)


if __name__ == "__main__":
    main()
