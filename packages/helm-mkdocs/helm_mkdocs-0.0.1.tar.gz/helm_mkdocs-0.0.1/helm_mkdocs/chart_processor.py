import yaml

from helm_mkdocs.generator.mkdocs import MKDocsGenerator
from helm_mkdocs.model import Chart
from helm_mkdocs.model import PageInput
from helm_mkdocs.reader import read_yaml


def generate_pages(yaml) -> [PageInput]:
    page_input = PageInput("root", yaml)
    page_input.root_item.comments = ["Values that are defined in the root of the values file."]
    pages = [page_input]
    root_values = {}
    for key in yaml.value:
        value = yaml.value[key]
        if isinstance(value.value, dict):
            pages.append(PageInput(value.name, value))
        else:
            root_values[key] = value
    page_input.root_item.value = root_values
    return pages


class ChartProcessor:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        file = self.settings["values"]
        chart = self.load_chart()
        generator = MKDocsGenerator(self.settings)

        yaml = read_yaml(file)

        pages = generate_pages(yaml)

        for page in pages:
            new_page = generator.generate_page(page)
            self.write_page(new_page, page.name)

        page = generator.generate_chart_page(chart, pages)
        self.write_page(page, "index")

    def load_chart(self):
        chart_path = self.settings["chart"]
        with open(chart_path) as file:
            load = yaml.safe_load(file)
            return Chart(load)

    def write_page(self, page, name):
        md_ = self.settings["output"] + "/" + name + ".md"
        print("Writing page", name, "to", md_)
        with open(md_, "w") as f:
            f.write(page)
