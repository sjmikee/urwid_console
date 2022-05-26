
from time import sleep
import urwid
from term import test
import os
from scrollable import Scrollable, ScrollBar

class Console:
    def __init__(self):
        self.output_text = urwid.Text('Output: \n')
        self.output_box = urwid.LineBox(urwid.Pile([('flow', self.output_text),]), title='Output')
        self.output_scrollable = ScrollBar(Scrollable(self.output_box))
        self.output_filler = urwid.Filler(self.output_text)
        self.terminal = urwid.Terminal(self.input_loop, encoding='utf-8')
        self.cmd = ''


    def input_loop(self):
        self.cmd = input('>>> ')
        while(self.cmd != 'exit'):
            try:
                os.write(self.write_fd, self.cmd.encode())
            except Exception as e:
                print(e)
            self.cmd = input('>>> ')


    def received_output(self, data):
        try:
            self.output_text.set_text(self.output_text.text + data.decode('utf-8') + '\n')
        except Exception as e:
            print(e)


    def main(self):
        urwid.set_encoding('utf8')
        mainframe = urwid.LineBox(
            urwid.Columns([
                ('fixed', 50, self.terminal),
                ('weight', 1, self.output_scrollable),
            ]),
        )

        def set_title(widget, title):
            mainframe.set_title(title)

        def quit(*args, **kwargs):
            raise urwid.ExitMainLoop()

        def handle_key(key):
            if key in ('q', 'Q'):
                quit()

        urwid.connect_signal(self.terminal, 'title', set_title)
        urwid.connect_signal(self.terminal, 'closed', quit)

        self.loop = urwid.MainLoop(
            mainframe,
            handle_mouse=True,
            unhandled_input=handle_key)

        self.terminal.main_loop = self.loop
        self.write_fd = self.loop.watch_pipe(self.received_output)
        self.loop.run()


if __name__ == '__main__':
    console = Console()
    console.main()