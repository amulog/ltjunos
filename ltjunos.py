#!/usr/bin/env python

import os
import re

import click


VARIABLE_REGEX = re.compile(
    r"^.*(?P<replace><variable>(?P<name>.*?)</variable>).*$"
)


class TemporaryFilePath:

    def __enter__(self):
        import tempfile
        fd, self._filepath = tempfile.mkstemp()
        os.close(fd)
        return self._filepath

    def __exit__(self, exc_type, exc_value, traceback):
        os.remove(self._filepath)


def _load_xlsx(filepath):

    with TemporaryFilePath() as csv_filepath:

        from xlsx2csv import Xlsx2csv
        Xlsx2csv(filepath, outputencoding="utf-8").convert(csv_filepath)

        import csv
        obj = {"contents": list()}
        with open(csv_filepath, "r") as f:
            reader = csv.reader(f)

            obj["title"] = reader.__next__()[0]
            columns = reader.__next__()

            for row in reader:
                item = {key: value for key, value in zip(columns, row)}
                obj["contents"].append(item)

    return obj


def generate_json(obj, output=None):
    import json
    if output is None:
        json.dumps(obj, indent=4)
    else:
        with open(output, "w") as f:
            json.dump(obj, f, indent=4)


def generate_amulog_template(obj, output=None):
    from amulog.lt_common import REPLACER_HEAD, REPLACER_TAIL
    from amulog.strutil import add_esc

    l_buf = []
    for item in obj["contents"]:
        mes = add_esc("{0}: {1}".format(item["NAME"], item["MESSAGE"]))

        while True:
            mo = VARIABLE_REGEX.match(mes)
            if mo:
                attr_name = mo.group("name")
                replacer = REPLACER_HEAD + attr_name.upper() + REPLACER_TAIL
                attr_start, attr_end = mo.span("replace")
                mes = mes[:attr_start] + replacer + mes[attr_end:]
            else:
                break

        l_buf.append(mes)

    if output is None:
        print("\n".join(l_buf))
    else:
        with open(output, "w") as f:
            f.write("\n".join(l_buf))


@click.command()
@click.argument("file")
@click.option("--output", "-o", default=None,
              help="output filename")
@click.option("--type", "-t", "format_type", default="json",
              help="output format type, one of [json, amulog-plain]")
def ltjunos(file, output, format_type):

    if format_type not in ("json", "amulog-plain"):
        click.BadParameter("invalid type")

    obj = _load_xlsx(file)

    if format_type == "json":
        generate_json(obj, output)
    elif format_type == "amulog-plain":
        generate_amulog_template(obj, output)
    else:
        raise ValueError


if __name__ == "__main__":
    ltjunos()
