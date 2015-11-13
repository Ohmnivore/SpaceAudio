class StyleProcessor:
    def __init__(self, defs):
        self.vardefs = {}
        self.parse_defs(defs)

    def parse_defs(self, defs):
        arr = defs.split('\n')
        for a in arr:
            a = a.strip()
            if len(a) > 0 and a[0] == '@':
                space = a.find(' ')
                name = a[1:space]
                value = a[space + 1:]
                self.vardefs[name] = value

    def process(self, css):
        nest_lvl = 0
        i = 0
        while i < len(css):
            c = css[i]
            if c == '{':
                nest_lvl += 1
            elif c == '}':
                nest_lvl -= 1
            elif c == '@' and nest_lvl != 0:
                j = i + 1
                name = ''
                while not (css[j].isspace() or css[j] == ';'):
                    name += css[j]
                    j += 1
                value = self.vardefs[name]
                css = css[:i] + value + css[j:]
            i += 1
        return css
