import lxml.etree as et


class ColorSetNumerical(object):
    class Range(object):
        class Limit(object):
            def __init__(self, op, vl):
                self.operator = op
                self.value = vl

        def __init__(self, _rgb, _desc, _lim):
            self.rgb = _rgb
            self.description = _desc
            self.limits = []
            for l in _lim:
                self.limits.append(self.Limit(l[0], l[1]))

    def __init__(self, n, sh_n, d, gr, t, r):
        self.name = n
        self.short_name = sh_n
        self.description = d
        self.groups = gr
        self.type = t
        self.ranges = []
        for _r in r:
            self.ranges.append(self.Range(_r[0], _r[1], _r[2]))

    def show(self):
        print('name: {}'.format(self.name))
        print('short name: {}'.format(self.short_name))
        print('description: {}'.format(self.description))
        print('groups: {}'.format(self.groups))
        print('type: {}'.format(self.type))
        for r in self.ranges:
            print('index {:<5} color {:>10} {:>10}'.format(self.ranges.index(r), r.rgb, r.description))
            for l in r.limits:
                print('{:>10} {:>12}'.format(l.operator, l.value))

    def createDescription(self):
        for index, x in enumerate(self.ranges):
            _limits = {}
            for y in x.limits:
                _limits[y.value] = y.operator
            if not x.description:
                if len(_limits) == 2:
                    operator_min = list(_limits.values())[0]
                    value_min = (float(list(_limits.keys())[0]))
                    operator_max = list(_limits.values())[1]
                    value_max = (float(list(_limits.keys())[1]))
                    min_str = f'{"[" if ">=" in operator_min else "("}{value_min:.2f}'
                    max_str = f'{value_max:.2f}{"]" if "<=" in operator_max else ")"}'
                    self.ranges[index].description = ', '.join([min_str, max_str])
                elif len(_limits) == 1:
                    operator = list(_limits.values())[0]
                    value = (float(list(_limits.keys())[0]))
                    if operator in ('<=', '<'):
                        self.ranges[index].description = f'(Min, {value:.2f}{"]" if "<=" in operator else ")"}'
                    elif operator in ('>=', '>'):
                        self.ranges[index].description = f'{"[" if ">=" in operator else "("}{value:.2f}, Max)'
                    elif operator == '=':
                        self.ranges[index].description = value
                else:
                    print('Error Limits')

    def valueToColor(self, value):
        clr = -1
        for color_range in self.ranges:
            inRange = True
            for condition in color_range.limits:
                limitChecker = {
                    '<': value < float(condition.value),
                    '<=': value <= float(condition.value),
                    '>': value > float(condition.value),
                    '>=': value >= float(condition.value),
                    '=': value == float(condition.value)
                }
                inRange = inRange if limitChecker[condition.operator] else False
            if inRange:
                clr = ((int(color_range.rgb) & 255) << 16 | (int(color_range.rgb) & (255 << 8)) | (
                        int(color_range.rgb) & (255 << 16)) >> 16)
        return clr


class ColorSetString(object):
    class Range(object):
        def __init__(self, _rgb, _desc, _string):
            if isinstance(_rgb, tuple):
                r, g, b = _rgb
                self.rgb = r << 16 | g << 8 | b
            else:
                self.rgb = _rgb
            self.description = _desc
            self.string = _string

    def __init__(self, n, sh_n, d, gr, t, r):
        self.name = n
        self.short_name = sh_n
        self.description = d
        self.groups = gr
        self.type = t
        self.ranges = []
        for _r in r:
            self.ranges.append(self.Range(_r[0], _r[1], _r[2]))

    def show(self):
        print('name: {}'.format(self.name))
        print('short name: {}'.format(self.short_name))
        print('description: {}'.format(self.description))
        print('groups: {}'.format(self.groups))
        print('type: {}'.format(self.type))

        for r in self.ranges:
            print('index {:<5} color {:>10} {:>10} {:>10}'.format(self.ranges.index(r), r.rgb, r.description, r.string))

    def createDescription(self):
        for index, x in enumerate(self.ranges):
            if not x.description:
                self.ranges[index].description = x.string

    def valueToColor(self, value):
        clr = -1
        for r in self.ranges:
            if r.string == value:
                clr = ((int(r.rgb) & 255) << 16 | (int(r.rgb) & (255 << 8)) | (int(r.rgb) & (255 << 16)) >> 16)
                break
        return clr


class ColorSetAutomatic(object):
    class Range(object):
        def __init__(self, _rgb, _desc, _string):
            r, g, b = _rgb
            self.rgb = r << 16 | g << 8 | b
            self.description = _desc
            self.string = _string

    def __init__(self, n, sh_n, d, gr, t, p):
        self.name = n
        self.short_name = sh_n
        self.description = d
        self.groups = gr
        self.type = t
        self.palette = p
        self.ranges = []

    def show(self):
        print('name: {}'.format(self.name))
        print('short name: {}'.format(self.short_name))
        print('description: {}'.format(self.description))
        print('groups: {}'.format(self.groups))
        print('type: {}'.format(self.type))

        for r in self.ranges:
            print('index {:<5} color {:>10} {:>10} {:>10}'.format(self.ranges.index(r), r.rgb, r.description, r.string))

    def createDescription(self):
        for index, x in enumerate(self.ranges):
            if not x.description:
                self.ranges[index].description = x.string

    def valueToColor(self, value):
        clr = -1
        for r in self.ranges:
            if r.string == value:
                clr = ((int(r.rgb) & 255) << 16 | (int(r.rgb) & (255 << 8)) | (int(r.rgb) & (255 << 16)) >> 16)
                break
        return clr


def getLegend(csFile, csSysFile, csName):
    # попытка получения легенды из Colorset.xml
    parser = et.XMLParser(encoding='cp1251')
    tree = et.parse(csFile, parser)

    root = tree.getroot()
    found = False
    legend, csType = None, None
    for elem in root:
        for subelem in elem:
            if subelem.attrib['name'] == csName:
                found = True
                cs, csType = subelem, subelem.attrib['type']
                break
    if not found:
        # попытка получения легенды из SystemColorset.xml
        tree = et.parse(csSysFile)
        root = tree.getroot()
        for elem in root:
            for subelem in elem:
                if subelem.attrib['name'] == csName:
                    found = True
                    cs, csType = subelem, subelem.attrib['type']
                    break

    if found:
        if csType == 'numerical':
            # все атрибуты легенды теперь будут находиться в структуре
            legend = ColorSetNumerical(cs.attrib['name'],
                                       cs.attrib['short_name'],
                                       cs.attrib['description'],
                                       cs.attrib['groups'],
                                       cs.attrib['type'],
                                       [
                                           [y.attrib['rgb'],
                                            y.attrib['description'],
                                            [(x.attrib['operator'], x.attrib['value']) for x in y]
                                            ] for y in cs
                                       ]
                                       )
            legend.createDescription()

        elif csType == 'string':
            legend = ColorSetString(cs.attrib['name'],
                                    cs.attrib['short_name'],
                                    cs.attrib['description'],
                                    cs.attrib['groups'],
                                    cs.attrib['type'],
                                    [
                                        [y.attrib['rgb'],
                                         y.attrib['description'],
                                         y.attrib['string']] for y in cs
                                    ]
                                    )
            legend.createDescription()

        elif csType == 'automatic':
            legend = ColorSetAutomatic(cs.attrib['name'],
                                       cs.attrib['short_name'],
                                       cs.attrib['description'],
                                       cs.attrib['groups'],
                                       cs.attrib['type'],
                                       cs.attrib['palette'])
            legend.createDescription()

        return legend, csType

    else:
        return None, None
