from helm_mkdocs.generator import Generator
from helm_mkdocs.model.page import PageInput


class MKDocsGenerator(Generator):

    def __init__(self, settings):
        super().__init__(settings)

    def generate_page(self, item: PageInput, depth=0) -> str:
        body = self.generate_value(item.name, item.root_item)

        for page_item in item.values:
            page_value = item.values[page_item]
            if isinstance(page_value.value, dict):
                body += self.generate_page(PageInput(page_item, page_value), depth + 1)
            elif isinstance(page_value.value, list):
                body += self.generate_list(page_item, page_value, depth + 1)
            else:
                body += self.generate_value(page_item, page_value)

        return body

    def generate_chart_page(self, chart, pages):
        return """
# Chart: %s

%s
%s

# Sections

%s


---

%s chart version (%s) %s
        """ % (
            chart.name, self.chart_image(chart), chart.description, self.chart_sections(pages), chart.type,
            chart.version,
            self.chart_app(chart))

    def chart_app(self, chart):
        if chart.type == "application":
            appStr = "running application"
            if chart.appVersion:
                appStr += " version (%s)" % chart.appVersion
            return appStr
        return ""

    def chart_image(self, chart):
        if chart.icon:
            return "![%s](%s)" % (chart.name, chart.icon)
        return ""

    def chart_sections(self, pages):
        return "\n".join(
            ["## [%s](./%s.md) \n\n %s" % (page.name, page.name, self.format_comments(page.comments, page.line_comment))
             for page in pages])

    def format_comments(self, comments, line_comment):
        return "\n\t".join([self.trim_comment(comment) for comment in comments]) + self.trim_comment(line_comment)

    def trim_comment(self, comment):
        if comment.startswith("# --"):
            return comment[4:].strip()
        if comment.startswith("##"):
            return comment[2:].strip()
        return comment[1:].strip()

    def generate_list(self, item_name, item, depth):
        body = self.generate_value(item.name, item)

        for page_item in item.value:
            page_value = page_item
            if isinstance(page_value.value, dict):
                body += self.generate_page(PageInput(page_item, page_value), depth + 1)
            elif isinstance(page_value.value, list):
                body += self.generate_list(page_item, page_value, depth)
            else:
                body += self.generate_value(page_item, page_value)

        return body

    def generate_value(self, page_name, page_value):
        return """
%s %s

    %s

%s

Type: %s

Path: `%s`
        """ % ("#" * int(page_value.depth /2), page_value.name, self.format_comments(page_value.comments, page_value.line_comment), self.format_value(page_value.value),
               page_value.object_type, self.object_path(page_value))

    def format_value(self, value):
        if isinstance(value, dict) or isinstance(value, list):
            return ""
        if "\n" in str(value):
            return """
Default:
```
%s
```
            """ % value
        return "Default: `%s`" % value

    def object_path(self, page_item):
        path = ""
        item = page_item
        while item.parent is not None:
            path = str(item.name) + "." + path
            item = item.parent
        return path[:-1]

