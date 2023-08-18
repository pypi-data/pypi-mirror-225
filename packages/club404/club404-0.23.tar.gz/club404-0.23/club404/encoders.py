#!/usr/bin/env python3
import sys
import argparse
import io
import json
import yaml
import csv


def toTEXT(data): return '{}'.format(data)
def toHTML(data): return '<pre>{}</pre>'.format(toTEXT(data))


def toJSON(data): return json.dumps(data)
def fromJSON(data): return json.loads(data)


def toYAML(data):
    with io.StringIO() as buffer:
        yaml.dump(data, buffer, default_flow_style=False)
        return buffer.getvalue()


def fromYAML(data):
    with io.StringIO(initial_value=data) as stream:
        return yaml.safe_load(stream)


def toCSV(data):
    data = [data] if not type(data) == list else data
    fields = data[0].keys() if len(data) else []
    with io.StringIO() as buffer:
        writer = csv.DictWriter(buffer, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        return buffer.getvalue()


def fromCSV(data, collapse=False):
    list = []
    with io.StringIO(initial_value=data) as buffer:
        reader = csv.DictReader(buffer)
        for row in reader:
            list.append(row)
    if collapse and len(list) < 2:
        return None if len(list) == 0 else list[0]
    return list


def fromFile(input):
    with open(input, 'r') as f:
        content = f.read()

        # Check if we can match the input format
        parts = input.split('.')
        type = None if len(parts) < 2 else '.'+parts[-1]
        match type:
            case '.json':
                # Load and parse JSON
                content = fromJSON(content)
            case '.yaml':
                # Parse the input file as yaml
                content = fromYAML(content)
            case '.csv':
                # Parse the input as CSV content. If only one row, treat as object
                content = fromCSV(content, collapse=True)
            case _:
                # Fallback: Prase the input and assume its either JSON or YAML
                content = fromYAML(content)

        return content


class Encoder:
    def __init__(self, mime_type, file_types=[], encode=toTEXT):
        self.mime = mime_type
        self.ext = file_types
        self.encode = encode


DEFAULT_ENCODERS = [
    Encoder("text/plain", [".txt"], toTEXT),
    Encoder("text/html", [".htm", ".html", ".htmx"], toHTML),
    Encoder("text/csv", [".csv"], toCSV),
    Encoder("application/json", [".json"], toJSON),
    Encoder("application/yaml", [".yaml"], toYAML),
]
