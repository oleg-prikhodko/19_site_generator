import json
import os

import markdown2
from jinja2 import FileSystemLoader, Environment


def load_text_from_file(filepath):
    with open(filepath) as text_file:
        text = text_file.read()
        return text


if __name__ == "__main__":
    json_config = json.loads(load_text_from_file("config.json"))
    articles = json_config["articles"]

    for article in articles:
        md_path = "articles/{}".format(article["source"])
        article_name = article["title"]
        md_content = load_text_from_file(md_path)
        html_content = markdown2.markdown(md_content)

        environment = Environment(loader=FileSystemLoader("templates"))
        article_template = environment.get_template("article.html")
        article_template_stream = article_template.stream(
            name=article_name, content=html_content
        )
        filename, _ = os.path.splitext(os.path.basename(article["source"]))

        if not os.path.exists("output"):
            os.mkdir("output")
        article_template_stream.dump("output/{}.html".format(filename))

        article["url"] = "{}.html".format(filename)

    index_template = environment.get_template('index.html')
    index_template_stream = index_template.stream(articles=articles)
    index_template_stream.dump("output/index.html")
