import pandas as pd
import rdflib
import collections
from setlr import isempty
from .sdd2setl import SemanticDataDictionary

def load_ontology(urls):
    graph = rdflib.ConjunctiveGraph()
    attempted_load = set()
    todo = [rdflib.URIRef(url) for url in urls]
    while len(todo) > 0:
        uri = todo.pop()
        g = graph.get_context(rdflib.URIRef(uri))
        if uri not in attempted_load:
            try:
                f = rdflib.util.guess_format(uri)
                g.parse(uri, format=f)
                imports = [o for s,p,o in g.triples((None,rdflib.OWL.imports, None))]
                local = [s for s,p,o in g.triples((None,rdflib.OWL.imports, None))]
                attempted_load.update(local)
                #print (imports)
                todo.extend(imports)
                #print("Loaded", uri)
            except Exception as e:
                pass
                #print("Error loading", str(uri), e)
        attempted_load.add(uri)
    return graph

def get_classes(sdd):
    def resolve_curie(curie):
        s = curie.split(":", 1)
        if len(s) == 1:
            return s[0]
        elif s[0] in sdd.prefixes:
            return sdd.prefixes[s[0]][s[1]]
        else:
            return s[1]
    result_map = collections.defaultdict(dict)

    curie_map = {}
    column_mappings = collections.defaultdict(set)
    for col in sdd.columns.values():
        for annotation in ['Attribute','Entity','Type']:
            if annotation in col and not isempty(col[annotation]):
                curies = col[annotation]
                for curie in curies:
                    uri = resolve_curie(curie)
                    column_mappings[col['Column']].add(uri)
                    result_map[uri]['uri'] = uri
                    result_map[uri]['curie'] = curie
                    result_map[uri]['label'] = col.get('Label',"")
                    result_map[uri]['definition'] = col.get('Definition',"")
                    result_map[uri]['type'] = "owl:Class"
                    curie_map[curie] = uri
        for annotation in ['Unit','Role','Relation']:
            if annotation in col and not isempty(col[annotation]):
                curie = col[annotation]
                if curie in sdd.columns:
                    continue
                uri = resolve_curie(curie)
                result_map[uri]['uri'] = uri
                result_map[uri]['curie'] = curie
                curie_map[curie] = uri
    for (column, code), curies in sdd.codebook.items():
        col_classes = column_mappings[column]
        for curie in curies:
            uri = resolve_curie(curie)
            result_map[uri]['uri'] = uri
            result_map[uri]['type'] = "owl:Class"
            result_map[uri]['curie'] = curie
            result_map[uri]['subClassOf'] = '\, '.join(col_classes)
    for column, mappings in sdd.resource_codebook.items():
        col_classes = column_mappings[column]
        for code, curie in mappings.items():
            for curie in curies:
                uri = resolve_curie(curie)
                result_map[uri]['uri'] = uri
                result_map[uri]['type'] = "\, ".join(col_classes)
                result_map[uri]['curie'] = curie
    return list(result_map.values())

def filter_unmatched(classes, ontology):
    return [c for c in classes
            if (c['uri'], rdflib.RDF.type, None) not in ontology]

data_file_types = {
  "xml" : "setl:XML",
  "excel" : "setl:Excel",
  "csv" : "csvw:Table"
}
def sddmarkup_main():
    import argparse
    from openpyxl import load_workbook

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', "--ontology")
    parser.add_argument('-t', '--datatype',
                        help="Data File type (xml, csv (default), excel)",
                        nargs='?', type=str, const=1, default="csv")
    parser.add_argument("semantic_data_dictionary")
    parser.add_argument("output_file")

    args = parser.parse_args()

    ontology = load_ontology(args.ontology.split(','))
    sdd = SemanticDataDictionary(args.semantic_data_dictionary, "http://example.org", data_file_types[args.datatype])

    classes = get_classes(sdd)
    new_classes = filter_unmatched(classes, ontology)

    new_classes_df = pd.DataFrame.from_records(new_classes)
    new_classes_df.to_csv(args.output_file)
