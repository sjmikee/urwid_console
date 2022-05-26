import urwid
from scrollable import Scrollable, ScrollBar

text1 = '''
Not
a
very
long
Text.
'''

text2 = '''
Another
not
very
long
Text.
'''

main = urwid.Pile([('pack', urwid.Text(text1)),
                   ('pack', urwid.Text(text2))])
mainloop = urwid.MainLoop(ScrollBar(Scrollable(main)))
mainloop.run()
