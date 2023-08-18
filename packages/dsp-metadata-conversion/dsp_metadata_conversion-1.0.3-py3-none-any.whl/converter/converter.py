import os
import sys
import argparse
from typing import Any, Dict, Generator, List, Optional, Tuple
import json
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.term import BNode
from rdflib.namespace import SDO, XSD, PROV
import glob
from pyshacl import validate
from pathlib import Path

DSP = Namespace('http://ns.dasch.swiss/repository#')


# Conversion Methods
# ------------------


def convert_and_save(files: List[str], target: str) -> int:
    """Convert a list of metadata files and save output to files.

    Takes a list of `.json` files, converts each of them, and stores it to the specified target directory.

    Args:
        files (List[str]): paths to `.json` files that should be transformed.
        target (str): path to the target directory where the output files should be saved.

    Returns:
        int: The number of files that were converted.
    """
    def __write(path: str, data: str) -> None:
        with open(path, mode='w+', encoding='utf-8') as fw:
            fw.write(data)

    res = 0
    for f in files:
        serializations = convert_file(f)
        if not serializations:
            continue
        ttl, jsonld, xml = serializations
        path_file = f'{target}/{Path(f).stem}'
        __write(f'{path_file}.ttl', ttl)
        __write(f'{path_file}.jsonld', jsonld)
        __write(f'{path_file}.xml', xml)
        res += 1
    return res


def convert_string(data_string: str, filename: str) -> Graph:
    """Convert the string representation of a V2 JSON metadata set to an RDF graph.

    Args:
        data_string (str): A string of V2 JSON metadata
        filename (str): the filename of the input for error logging purposes

    Returns:
        Graph: a Graph representing the RDF mapping of the input metadata
    """
    data: Dict[str, Any] = json.loads(data_string)
    g = Graph()
    g.bind('dsp', DSP)
    g.bind('rdf', RDF)
    g.bind('sdo', SDO)
    g.bind('prov', PROV)

    project = data.get('project')
    if not project:
        raise Exception(f'Metadata set {filename} did not contain a project, which is required.')
    _get_project(g, project)

    datasets = data.get('datasets')
    if not datasets:
        raise Exception(f'Metadata set "{filename}.json" did not contain any datasets, at least one is required.')
    for dataset in datasets:
        _get_dataset(g, dataset)

    persons = data.get('persons')
    if persons:
        for p in persons:
            _get_person(g, p)

    organizations = data.get('organizations')
    if organizations:
        for o in organizations:
            _get_organization(g, o)

    grants = data.get('grants')
    if grants:
        for gr in grants:
            _get_grant(g, gr)

    return g


def convert_file(file: str) -> Optional[Tuple[str, str, str]]:
    """Convert a file containing V2 JSON metadata set to RDF serializations.

    Args:
        file (str): path of a JSON file

    Returns:
        Optional[Tuple[str, str]]: None if the conversion failed. Otherwise a tuple with the turtle and the JSON-LD serialization of the metadata.
    """
    filename = file.rsplit('.', 1)[0]
    try:
        with open(file, mode='r+', encoding='utf-8') as f:
            data = f.read()
        graph = convert_string(data, filename)
        ttl = graph.serialize()
        ttl = ttl.replace('<http://schema.org/>', '<https://schema.org/>')
        jsonld = graph.serialize(format='json-ld')
        jsonld = jsonld.replace('<http://schema.org/>', '<https://schema.org/>')
        xml = graph.serialize(format='pretty-xml')
        xml = xml.replace('http://schema.org/', 'https://schema.org/')
        return ttl, jsonld, xml
    except Exception as e:
        print(f'WARNING: failed to convert file {file}! ({type(e).__name__} caused by: {e})')
        return None


def convert_files(files: List[str]) -> None:
    """Convert multiple files"""
    for file in files:
        convert_file(file)


# RDF Mapping Methods
# -------------------


def _get_project(g: Graph, d: Dict[str, Any]) -> None:
    iri = URIRef(d['__id'])
    g.add((iri, RDF.type, DSP.Project))

    prop = d['shortcode']
    g.add((iri, DSP.hasShortcode, Literal(prop, datatype=XSD.string)))

    prop = d['name']
    g.add((iri, DSP.hasName, Literal(prop, datatype=XSD.string)))

    prop = d['howToCite']
    g.add((iri, DSP.hasHowToCite, Literal(prop, datatype=XSD.string)))

    prop = d['description']
    for txt in __get_multi_language_text(g, prop):
        g.add((iri, DSP.hasDescription, txt))

    prop = d['startDate']
    g.add((iri, DSP.hasStartDate, Literal(prop, datatype=XSD.date)))

    prop = d['teaserText']
    g.add((iri, DSP.hasTeaser, Literal(prop, datatype=XSD.string)))

    props = d['datasets']
    for prop in props:
        g.add((iri, DSP.hasDataset, URIRef(prop)))

    props = d['keywords']
    for prop in props:
        for txt in __get_multi_language_text(g, prop):
            g.add((iri, DSP.hasKeyword, txt))

    props = d['disciplines']
    for prop in props:
        if prop.get('__type') == 'URL':
            bn_url = __get_url(g, prop)
            g.add((iri, DSP.hasDiscipline, bn_url))
        else:
            for txt in __get_multi_language_text(g, prop):
                g.add((iri, DSP.hasDiscipline, txt))

    props = d['temporalCoverage']
    for prop in props:
        if prop.get('__type') == 'URL':
            bn_url = __get_url(g, prop)
            g.add((iri, DSP.hasTemporalCoverage, bn_url))
        else:
            for txt in __get_multi_language_text(g, prop):
                g.add((iri, DSP.hasTemporalCoverage, txt))

    props = d['spatialCoverage']
    for prop in props:
        bn_url = __get_url(g, prop)
        g.add((iri, DSP.hasSpatialCoverage, bn_url))

    props = d['funders']
    for prop in props:
        g.add((iri, DSP.hasFunder, URIRef(prop)))

    prop = d['url']
    bn_url = __get_url(g, prop)
    g.add((iri, DSP.hasURL, bn_url))

    prop = d.get('secondaryURL')
    if prop:
        bn_url = __get_url(g, prop)
        g.add((iri, DSP.hasSecondaryURL, bn_url))

    prop = d.get('dataManagementPlan')
    if prop:
        dmp = BNode()
        av = prop.get('available')
        if av:
            g.add((dmp, DSP.isAvailable, Literal(True, datatype=XSD.boolean)))
        url = prop.get('url')
        if url:
            bn_url = __get_url(g, prop)
            g.add((dmp, DSP.hasURL, bn_url))
        if av or url:
            g.add((dmp, RDF.type, DSP.DataManagementPlan))
            g.add((iri, DSP.hasDataManagementPlan, dmp))

    prop = d.get('endDate')
    if prop:
        g.add((iri, DSP.hasEndDate, Literal(prop, datatype=XSD.date)))

    prop = d.get('contactPoint')
    if prop:
        g.add((iri, DSP.hasContactPoint, URIRef(prop)))

    props = d.get('publications')
    if props:
        for prop in props:
            g.add((iri, DSP.hasPublication, Literal(prop, datatype=XSD.string)))

    props = d.get('grants')
    if props:
        for prop in props:
            g.add((iri, DSP.hasGrant, URIRef(prop)))

    props = d.get('alternativeNames')
    if props:
        for prop in props:
            for txt in __get_multi_language_text(g, prop):
                g.add((iri, DSP.hasAlternativeName, txt))


def _get_dataset(g: Graph, d: Dict[str, Any]) -> None:
    iri = URIRef(d['__id'])
    g.add((iri, RDF.type, DSP.Dataset))

    title = d['title']
    g.add((iri, DSP.hasTitle, Literal(title, datatype=XSD.string)))

    conds = d['accessConditions']
    g.add((iri, DSP.hasAccessConditions, Literal(conds, datatype=XSD.string)))

    htc = d['howToCite']
    g.add((iri, DSP.hasHowToCite, Literal(htc, datatype=XSD.string)))

    status = d['status']
    g.add((iri, DSP.hasStatus, Literal(status, datatype=XSD.string)))

    abstracts = d['abstracts']
    for abstract in abstracts:
        if abstract.get('__type') == 'URL':
            bn_url = __get_url(g, abstract)
            g.add((iri, DSP.hasAbstract, bn_url))
        else:
            for txt in __get_multi_language_text(g, abstract):
                g.add((iri, DSP.hasAbstract, txt))

    types = d['typeOfData']
    for t in types:
        g.add((iri, DSP.hasTypeOfData, Literal(t, datatype=XSD.string)))

    licenses = d['licenses']
    for lic in licenses:
        license = BNode()
        g.add((license, RDF.type, DSP.License))
        bn_url = __get_url(g, lic['license'])
        g.add((license, DSP.hasURL, bn_url))
        g.add((license, DSP.hasDate, Literal(lic['date'], datatype=XSD.date)))
        if lic.get('details'):
            g.add((license, DSP.hasDetails, Literal(lic['details'], datatype=XSD.string)))
        g.add((iri, DSP.hasLicense, license))

    langs = d['languages']
    for lang in langs:
        for txt in __get_multi_language_text(g, lang):
            g.add((iri, DSP.hasLanguage, txt))

    attrs = d['attributions']
    for attr in attrs:
        attribution = BNode()
        g.add((attribution, RDF.type, PROV.Attribution))
        g.add((attribution, PROV.agent, URIRef(attr['agent'])))
        for role in attr['roles']:
            g.add((attribution, DSP.hasRole, Literal(role, datatype=XSD.string)))
        g.add((iri, DSP.hasQualifiedAttribution, attribution))

    date = d.get('datePublished')
    if date:
        g.add((iri, DSP.hasDatePublished, Literal(date, datatype=XSD.date)))

    date = d.get('dateCreated')
    if date:
        g.add((iri, DSP.hasDateCreated, Literal(date, datatype=XSD.date)))

    date = d.get('dateModified')
    if date:
        g.add((iri, DSP.hasDateModified, Literal(date, datatype=XSD.date)))

    distro = d.get('distribution')
    if distro:
        bn_url = BNode()
        g.add((bn_url, RDF.type, SDO.DataDownload))
        g.add((bn_url, SDO.url, Literal(distro['url'])))
        g.add((iri, DSP.hasDistribution, bn_url))

    alt_titles = d.get('alternativeTitles')
    if alt_titles:
        for title in alt_titles:
            for txt in __get_multi_language_text(g, title):
                g.add((iri, DSP.hasAlternativeTitle, txt))

    urls = d.get('urls')
    if urls:
        for url in urls:
            bn_url = __get_url(g, url)
            g.add((iri, DSP.hasURL, bn_url))

    additional = d.get('additional')
    if additional:
        for add in additional:
            if abstract.get('__type') == 'URL':
                bn_url = __get_url(g, abstract)
                g.add((iri, DSP.hasAdditional, bn_url))
            else:
                for txt in __get_multi_language_text(g, abstract):
                    g.add((iri, DSP.hasAdditional, txt))


def _get_person(g: Graph, d: Dict[str, Any]) -> None:
    iri = URIRef(d['__id'])
    g.add((iri, RDF.type, DSP.Person))

    titles = d['jobTitles']
    for title in titles:
        g.add((iri, DSP.hasJobTitle, Literal(title, datatype=XSD.string)))

    given_names = d['givenNames']
    given_name = ' '.join(given_names)
    g.add((iri, DSP.hasGivenName, Literal(given_name, datatype=XSD.string)))

    family_names = d['familyNames']
    family_name = ' '.join(family_names)
    g.add((iri, DSP.hasFamilyName, Literal(family_name, datatype=XSD.string)))

    affiliations = d['affiliation']
    for affiliation in affiliations:
        g.add((iri, DSP.hasAffiliation, URIRef(affiliation)))

    addr = d.get('address')
    if addr:
        address = __get_address(g, addr)
        g.add((iri, DSP.hasAddress, address))

    email = d.get('email')
    if email:
        g.add((iri, DSP.hasEmail, Literal(email, datatype=XSD.string)))

    email = d.get('secondaryEmail')
    if email:
        g.add((iri, DSP.hasSecondaryEmail, Literal(email, datatype=XSD.string)))

    authRefs = d.get('authorityRefs')
    if authRefs:
        for ref in authRefs:
            bn_url = __get_url(g, ref)
            g.add((iri, DSP.hasAuthorityFileReference, bn_url))


def _get_organization(g: Graph, d: Dict[str, Any]) -> None:
    iri = URIRef(d['__id'])
    g.add((iri, RDF.type, DSP.Organization))

    name = d['name']
    g.add((iri, DSP.hasName, Literal(name, datatype=XSD.string)))

    url = d.get('url')
    if url:
        bn_url = __get_url(g, url)
        g.add((iri, DSP.hasURL, bn_url))

    addr = d.get('address')
    if addr:
        address = __get_address(g, addr)
        g.add((iri, DSP.hasAddress, address))

    email = d.get('email')
    if email:
        g.add((iri, DSP.hasEmail, Literal(email, datatype=XSD.string)))

    names = d.get('alternativeNames')
    if names:
        for n_multilang in names:
            for txt in __get_multi_language_text(g, n_multilang):
                g.add((iri, DSP.hasAbstract, txt))

    authRefs = d.get('authorityRefs')
    if authRefs:
        for ref in authRefs:
            bn_url = __get_url(g, ref)
            g.add((iri, DSP.hasAuthorityFileReference, bn_url))


def _get_grant(g: Graph, d: Dict[str, Any]) -> None:
    iri = URIRef(d['__id'])
    g.add((iri, RDF.type, DSP.Grant))

    funders = d['funders']
    for funder in funders:
        g.add((iri, DSP.hasFunder, URIRef(funder)))

    nr = d.get('number')
    if nr:
        g.add((iri, DSP.hasNumber, Literal(nr, datatype=XSD.string)))

    n = d.get('name')
    if n:
        g.add((iri, DSP.hasName, Literal(n, datatype=XSD.string)))

    url = d.get('url')
    if url:
        bn_url = __get_url(g, url)
        g.add((iri, DSP.hasURL, bn_url))


# Helper Methods
# --------------


def __get_url(g: Graph, d: Dict[str, Any]) -> BNode:
    text = d.get('text')
    url = d.get('url')
    bn_url = BNode()
    g.add((bn_url, RDF.type, SDO.URL))
    g.add((bn_url, SDO.url, Literal(url)))
    if text and not text == url:
        propID_bn = BNode()
        g.add((propID_bn, RDF.type, SDO.PropertyValue))
        g.add((propID_bn, SDO.propertyID, Literal(text)))
        g.add((bn_url, SDO.propertyID, propID_bn))
    return bn_url


def __get_address(g: Graph, d: Dict[str, Any]) -> BNode:
    bn_addr = BNode()
    g.add((bn_addr, RDF.type, SDO.PostalAddress))
    g.add((bn_addr, SDO.streetAddress, Literal(d['street'], datatype=XSD.string)))
    if d.get('additional'):
        g.add((bn_addr, DSP.additional, Literal(d['additional'], datatype=XSD.string)))
    g.add((bn_addr, SDO.postalCode, Literal(d['postalCode'], datatype=XSD.string)))
    g.add((bn_addr, SDO.addressLocality, Literal(d['locality'], datatype=XSD.string)))
    if d.get('canton'):
        g.add((bn_addr, SDO.addressRegion, Literal(d['canton'], datatype=XSD.string)))
    g.add((bn_addr, SDO.addressCountry, Literal(d['country'], datatype=XSD.string)))
    return bn_addr


def __get_multi_language_text(g: Graph, d: Dict[str, Any]) -> Generator[Literal, None, None]:
    for lang in d.keys():
        txt = d[lang]
        yield Literal(txt, lang=lang)


# Validation Functions
# --------------------


def validate_files(files: List[str]) -> None:
    """Validate multiple files"""
    for file in files:
        validate_file(file)


def validate_file(file: str) -> None:
    """Validate a V2 RDF metadata file against the SHACL ontology"""
    shacl = "https://raw.githubusercontent.com/dasch-swiss/dsp-meta-svc/main/docs/services/metadata/schema-metadata.shacl"
    print(file)
    conforms, result_graph, result_text = validate(data_graph=file,
                                                   shacl_graph=shacl,
                                                   inference='none')
    print(result_text)
    print('\n-------------\n\n')


# CLI entry point
# ---------------

def cli():
    parser = argparse.ArgumentParser(description='Convert a JSON metadata file to RDF')
    parser.add_argument('path', help='path of the JSON file or folder to be converted')
    parser.add_argument('-d', '--dir', action="store_true",
                        help='indicates that the given path is a directory, not a file, and should be used for bulk conversion')
    args = parser.parse_args()
    f = args.path
    isDir = args.dir
    if not os.path.exists(f):
        print(f'Error: The specified file/path {f} does not exist.')
        sys.exit(1)
    if isDir:
        if not os.path.isdir(f):
            print(f'Error: The specified file/path {f} does not exist.')
            sys.exit(1)
        path = Path(f)
        ff = glob.glob(f'{path}/*.json')
        if not ff:
            print(f'Error: No JSON files in the specified directory {f}')
            sys.exit(1)
        convert_and_save(ff, path)
    else:
        out = Path(f).parent
        convert_and_save([f], out)
