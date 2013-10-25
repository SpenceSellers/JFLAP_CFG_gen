import xml.etree.ElementTree as ET
class CFG(object):
    def __init__(self):
        self.rules = {}

    def add_rule(self, variable, result):
        self.rules.setdefault(variable, set()).add(result)

    def JFLAP_export(self):
        structure = ET.Element("structure")
        ET.SubElement(structure, "type").text = "grammar"
        for variable, varrules in self.rules.iteritems():
            for rule in varrules:
                jrule = ET.SubElement(structure, "production")
                ET.SubElement(jrule, "left").text = variable
                if (rule):
                    ET.SubElement(jrule, "right").text = rule
        return ET.dump(structure)
                
def main():
    g = CFG()
    g.add_rule("S", "aSb")
    g.add_rule("S", "")
    g.JFLAP_export();
main()
