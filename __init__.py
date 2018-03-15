#!/usr/local/bin/python3
colors = {color: idx for idx, color in enumerate([
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'normal',
    ])}

formats = {frmt: idx for idx, frmt in enumerate([
    'normal',
    'bold',
    'faint',
    'italic',
    'underline',
    'slowblink',
    'rapidblink',
    'negative',
    'conceal',
    'crossedout',]) }

class ColorPart():

    pre = '\x1b['
    post = '\x1b[0m'

    def __init__(self, text = '', frmt = 'normal', fg = 'normal', bg = 'normal'):
        self.text = text
        self.fg = fg
        self.bg = bg

        if not isinstance(frmt, list):
            frmt = [frmt]
        for f in frmt[:-1]:
            self.text = ColorPart(self.text, f)
        self.frmt = frmt[-1]

    def __str__(self):
        fg = str(self.fg)
        bg = str(self.bg)
        frmt = str(self.frmt)
        return self.pre + frmt + ';' + fg + ';' + bg + 'm' + str(self.text) + self.post

    @property
    def fg(self):
        return self._fg

    @fg.setter
    def fg(self, x):
        if isinstance(x, int):
            if x < 39 and x > 29:
                self._fg = x
            else:
                self._fg = 30 + x
        else:
            assert(x in colors)
            self._fg = 30 + colors[x]

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, x):
        if isinstance(x, int):
            if x < 49 and x > 39:
                self._bg = x
            else:
                self._bg = 40 + x
        else:
            assert(x in colors)
            self._bg = 40 + colors[x]

    @property
    def frmt(self):
        return self._frmt

    @frmt.setter
    def frmt(self, x):
        if isinstance(x, int):
            self._frmt = x
        else:
            assert(x in formats)
            self._frmt = formats[x]



class Color():
    def __init__(self, text = '', frmt = 'normal', fg = 'normal', bg = 'normal'):
        self.parts = [ColorPart(text, frmt, fg, bg)]
        
    def separated(self):
        separated = []
        for part in self.parts:
            for ch in part.text:
                separated.append(ColorPart(ch, part.frmt, part.fg, part.bg))
        return separated

    def cohesed(self):
        cohesed = []
        for part in self.parts: 
            if len(cohesed) == 0:
                cohesed.append(part)
                continue
            last = cohesed[-1]
            if cohesed and part.fg == last.fg and part.bg == last.bg and part.frmt == last.frmt:
                last.text += part.text
            else:
                cohesed.append(part)

        return list(filter(lambda x: x.text, cohesed))

    def __str__(self):
        return ''.join([str(i) for i in self.parts])

    def __repr__(self):
        return ''.join([i.text for i in self.parts])

    def __add__(self, x):
        if isinstance(x, Color):
            self.parts += x.parts
        elif isinstance(x, str):
            self.parts.append(ColorPart(x))
        else:
            raise TypeError('Requires either Color or str')
        return self

    def __len__(self):
        return sum([len(part.text) for part in self.parts])

    def __getitem__(self, key):
        filtered = self.separated()[key]
        ret = Color()
        ret.parts = [filtered] if not isinstance(filtered, list) else filtered
        ret.parts = ret.cohesed()
        return ret

def test():

    teststrings = [
        
        # Argument usage

        'keywords', 
        Color('fish', frmt='italic', fg = 'red', bg = 'yellow'),
        'positional',
        Color('fish', 'bold', 'blue', 'normal'),
        'only frmt',
        Color('fish', 'faint'),
        'numbers',
        Color('fish', fg = 1),
        'several formats (not colors)',
        Color('fish', ['italic', 'bold', 'faint', 'underline'], 'red'),

        # Features
        
        'len',
        str(len(Color('this string has a length of 30', 'bold'))),
        'addition',
        Color('one', fg='red') + Color('two', fg='blue'),
        'indexing',
        (Color('one', fg='red') + Color('two', fg='blue'))[2],
        'splice',
        (Color('one', fg='red') + Color('two', fg='blue'))[2:5],
        'splice 2',
        (Color('oioi', fg='red') + Color('apap', fg='blue'))[::2],
        'nested strings',
        Color(Color('s')+ Color(Color('s') + Color('s'))),
        'length of nested strings works',
        str(len(Color(Color('s')+ Color(Color(Color('ss', 'faint'), 'bold') + Color('s'), 'italic'))))

    ]

    for test in zip(teststrings[::2], teststrings[1::2]):
        print(test[0])
        print(Color('\t') + test[1])

if __name__ == '__main__':
    test()
