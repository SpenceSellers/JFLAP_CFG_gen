import xml.etree.ElementTree as ET
import argparse
class CFG(object):
    def __init__(self):
        self.rules = {}

    def add_rule(self, variable, result):
        self.rules.setdefault(variable, set()).add(result)

    def JFLAP_export(self):
        ''' Exports the CFG into the JFLAP CFG format.'''
        structure = ET.Element("structure")
        ET.SubElement(structure, "type").text = "grammar"
        for variable, varrules in self.rules.iteritems():
            for rule in varrules:
                jrule = ET.SubElement(structure, "production")
                ET.SubElement(jrule, "left").text = variable
                if (rule):
                    ET.SubElement(jrule, "right").text = rule
        return ET.tostring(structure)

    def parse_rule(self, string, epsilon=None, separator=None):
        ''' Parses a single statement from a string. '''
        if epsilon == None: raise ValueError("No epsilon specified!")
        if separator == None: separator = ValueError("No separator specified!")
        try:
            (variable, rules) = string.split(separator)
        except ValueError:
            raise ValueError("Invalid rule:" + string + ". Check transitions and separators!")
            
        variable = variable.strip()
        rules = rules.split("|")
        rules = map(lambda s: s.strip(), rules)

        for r in rules:
            if r == epsilon: r = ""    
            self.add_rule(variable, r)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cfg", type=str, help="The CFG to be converted. Example: 'S -> aSb | ~")
    parser.add_argument("-e", default="~", type=str, help="Epsilon designator. Default: %(default)s")
    parser.add_argument("-t", default="->", type=str, help="Transition Separator. Default: %(default)s")
    parser.add_argument("-s", default=";", type=str, help="The line/rule separator. Default: %(default)s")
    parser.add_argument("-o", type=str, help="Output file")
    args = parser.parse_args()

    linesep = args.s if args.s else ";"

    g = CFG()
    for r in args.cfg.split(linesep):
        g.parse_rule(r, epsilon=args.e, separator=args.t)

    out = g.JFLAP_export()
    if args.o:
        try:
            f = open(args.o, "w")
        except IOError:
            raise IOError("Unable to open the output file: " + args.o)
        f.write(out)
        f.close()
    else:
        print out
main()
