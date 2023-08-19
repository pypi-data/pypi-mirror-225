#! /usr/bin/python3
import argparse
import os.path
import sys

from .chart_processor import ChartProcessor


def validate_chart(chart):
    if os.path.exists("%s/values.yaml" % chart) and os.path.exists("%s/Chart.yaml" % chart):
        return True
    print("Path to chart %s is not valid" % chart)
    sys.exit(1)


def process_settings(args):
    outDir = args.output
    if not os.path.isdir(args.output):
        os.makedirs(args.output)

    chart = args.chart
    if not os.path.isdir(chart):
        os.path.dirname(chart)
    validate_chart(chart)

    return {
        "chart_dir": chart,
        "chart": "%s/Chart.yaml" % chart,
        "values": "%s/values.yaml" % chart,
        "output": os.path.abspath(outDir),
        "indent": args.indentation
    }


def run(args):
    settings = process_settings(args)
    processor = ChartProcessor(settings)
    processor.run()

def run_cli():
    parser = argparse.ArgumentParser(
        prog='helm-mkdocs',
        description='Generate MKDocs style Markdown from a helm chart.',
        epilog='')

    parser.add_argument("chart", help="The path to the chart folder.")
    parser.add_argument("-o", "--output", default="docs_out", help="The path to output the compiled docs.")
    parser.add_argument("-i", "--indentation", default=2, help="The depth of each indentation.")

    parse_args = parser.parse_args()
    run(parse_args)

if __name__ == '__main__':
    run_cli()
