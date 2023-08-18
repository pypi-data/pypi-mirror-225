"""
Tries to figure out the file type based on content.
"""
import csv
import re


def magic(file_path):
    """
    Based on the first few blocks of `file_path` contents, figure out the likely
    data file serialization type.
    """
    # if XML, it's likely rdf/xml
    # if JSON, it's likely json-ld
    # we go through the various text-based formats before finally seeing if we can parse it
    # as CSV or similar (regular separator character, line feeds, etc.)
    with open(file_path, "r") as file:
        blocks = file.read(8096)  # read 8k - should be enough to figure out what we have
        if re.match(r'^\s*<\?xml', blocks):
            return 'application/rdf+xml'
        if re.match(r'^\s*<!--', blocks):
            return 'application/rdf+xml'
        if re.match(r'^\s*<[a-zA-Z]+://', blocks):
            return 'application/n-triples'
        if re.match(r'^\s*<\S', blocks):
            return 'application/rdf+xml'
        if re.match(r'^\s*@(base|prefix)\s+', blocks):
            return 'text/turtle'
        if re.match(r'^\s*(BASE|PREFIX)\s+', blocks):
            return 'text/turtle'
        if re.match(r'^\s*[{[]', blocks):
            return 'application/ld+json'
        if _maybe_csv(blocks):
            return 'text/csv'
        return 'text/plain'


def _maybe_csv(blocks):
    """
    Try to figure out if the file is likely to be CSV or similar.
    """
    dialect = csv.Sniffer().sniff(blocks)
    return dialect is not None
