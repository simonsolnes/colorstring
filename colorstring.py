class ColorString():
    colors = {
        "black" : 0,
        "red" : 1,
        "green" : 2,
        "yellow" : 3,
        "blue" : 4,
        "magenta" : 5,
        "cyan" : 6,
        "white" : 7,
        "normal" : 8
    }
    formats = {
        "normal" : 0,
        "bold" : 1,
        "faint" : 2,
        "italic" : 3,
        "underline" : 4,
        "slowblink" : 5,
        "rapidblink" : 6,	# NS
        "negative" : 7,
        "conceal" : 8,		# NS
        "crossedout" : 9,	# NA
        "jkl" : 12
    }
    class SubString():

        pre = '\x1b['
        post = '\x1b[0m'

        def __init__(self, string):
            self.string = string

        def __str__(self):
            return self.pre + self.frmt + ";" + self.fg + ";" + self.bg + "m" + self.string + self.post

    def __init__(self, string=None, fg = "normal", bg = "normal", frmt = "normal"):

        self.substrings = []
        if not string == None:

            substring = self.SubString(string)

            if not fg in self.colors.keys():
                raise Exception("Not a valid color")
            else:
                substring.fg = str(30 + self.colors[fg])
            if not bg in self.colors.keys():
               raise Exception("Not a valid color")
            else:
                substring.bg = str(40 + self.colors[bg])
            if not frmt in self.formats.keys():
                raise Exception("Not a valid format")
            else:
                substring.frmt = str(self.formats[frmt])
            
            self.substrings.append(substring)
    def __split_substrings(self):
        subchars = []
        for substring in self.substrings:
            for char in substring.string:
                subchar = self.SubString(char)
                subchar.fg = substring.fg
                subchar.bg = substring.bg
                subchar.frmt = substring.frmt
                subchars.append(subchar)
        self.substrings = subchars

    # Currently not working
    def __merge_substrings(self):
        return
        if len(self.substrings) == 0:
            return

        substrings = []
        buf = ''
        fg = self.substrings[0].fg
        bg = self.substrings[0].bg
        frmt = self.substrings[0].frmt
        for substring in self.substrings:
            buf += substring.string
            if substring.fg != fg and substring.bg != bg and substring.frmt != frmt:
                newsubstring = self.SubString(buf)
                newsubstring.fg = fg
                newsubstring.bg = bg
                newsubstring.frmt = frmt
                substrings.append(newsubstring)
                buf = ''
            fg = substring.fg
            bg = substring.bg
            frmt = substring.frmt
        self.substrings = substrings
        
    def copy(self):
        newstring = ColorString()
        for substring in self.substrings:
            newsubstring = self.SubString(substring.string)
            newsubstring.fg = substring.fg
            newsubstring.bg = substring.bg
            newsubstring.frmt = substring.frmt
            newstring.substrings.append(newsubstring)
        return newstring

    def __repr__(self):
        return self.string

    def __getitem__(self, key):

        newstring = self.copy()
        newstring.__split_substrings()
        newstring.substrings = newstring.substrings[key]
        # newstring.__merge_substrings()
        
        return newstring

    def __str__(self):
        final = ''
        for substring in self.substrings:
            final += str(substring)
        return final

    def __len__(self):
        lenght = 0
        for substring in self.substrings:
            lenght += len(substring.string)
        return lenght

    def __add__(self, other):
        if not isinstance(other, ColorString):
            raise TypeError("Please add a ColorString with ColorString")
        newstring = ColorString()
        newstring.substrings = [sub for sub in self.substrings] + [sub for sub in other.substrings]
        return newstring
