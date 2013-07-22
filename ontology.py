from collections import defaultdict

import gene_ontology.obo as obo

TAG_FORMAT = "%s:%10d"


def parse_obo(obo_file):
    """Parse OBO file"""
    parser = obo.Parser(open(obo_file))
    ontology = dict(pso={}, roto={}, psro={})
    for stanza in parser:
        stanza_id = stanza.tags["id"][0].value
        prefix = stanza_id.split(":")[0].lower()
        ontology[prefix][stanza_id] = stanza.tags
    return ontology


def by_namespace(ontology):
    namespaces = defaultdict()
    for name, value in ontology.items():
        for ns in value.get("namespace", ["None"]):
            ns = str(ns)
            namespaces[ns][name] = value
    return dict(namespaces)
