import os


class Menu:

    @staticmethod
    def collect_input(prompt):
        return input(prompt)

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def blank():
        print()

    @staticmethod
    def hbar(buffer_char='*', head_char=None, tail_char=None, text=None, align='left', autowrap=True):
        return Menu.text(text, align, autowrap, buffer_char, head_char, tail_char)

    @staticmethod
    def htext(text=None, align='center', autowrap=True, buffer_char=' ', head_char='* ', tail_char=' *'):
        return Menu.text(text, align, autowrap, buffer_char, head_char, tail_char)

    @staticmethod
    def text(text=None, align='left', autowrap=True, buffer_char=' ', head_char=' ', tail_char=' '):
        line = ''
        length = os.get_terminal_size()[0]
        remainder = None

        if head_char is not None:
            length -= len(head_char)
            line += head_char
        if tail_char is not None:
            length -= len(tail_char)
        elif head_char is not None:
            length -= len(head_char)
            tail_char = head_char

        if isinstance(text, str) and len(text):
            text_length = len(text)
            trunc_text = text[:length]
            trunc_length = len(trunc_text)

            if autowrap and text_length > trunc_length:
                remainder = text[trunc_length:]

            if text_length == length:
                line += trunc_text
            else:
                buffer = length - trunc_length

                if align == 'center':

                    buffers = []

                    for x in range(2):
                        buffers.append(buffer // 2 + (1 if x < buffer % 2 else 0))

                    for i in range(buffers[0]):
                        line += buffer_char

                    line += trunc_text

                    for i in range(buffers[1]):
                        line += buffer_char

                elif align == 'left':

                    line += trunc_text

                    if buffer:
                        for i in range(buffer):
                            line += buffer_char

                elif align == 'right':

                    for i in range(buffer):
                        line += buffer_char

                    line += trunc_text

        elif text is None:

            for i in range(length):
                line += buffer_char

        if tail_char is not None:
            line += tail_char

        print(line)

        if isinstance(remainder, str):
            Menu.text(remainder, align, autowrap, buffer_char, head_char, tail_char)
