import json
import os

import markdown2
from jinja2 import FileSystemLoader, Environment
from livereload import Server


def load_text_from_file(filepath):
    with open(filepath) as text_file:
        text = text_file.read()
        return text


def make_site():
    json_config = json.loads(load_text_from_file("config.json"))
    articles = json_config["articles"]
    topics = json_config["topics"]
    topic_titles = {topic["slug"]: topic["title"] for topic in topics}

    for article in articles:
        md_path = "articles/{}".format(article["source"])
        md_content = load_text_from_file(md_path)
        html_content = markdown2.markdown(md_content)
        filename, _ = os.path.splitext(os.path.basename(article["source"]))

        article["url"] = "{}.html".format(filename)
        article["topic"] = topic_titles.get(article["topic"])

        environment = Environment(loader=FileSystemLoader("templates"))
        article_template = environment.get_template("article.html")
        article_template_stream = article_template.stream(
            name=article["title"], topic=article["topic"], content=html_content
        )

        if not os.path.exists("output"):
            os.mkdir("output")
        article_template_stream.dump("output/{}.html".format(filename))

    for topic in topics:
        topic["articles"] = [
            article
            for article in articles
            if article["topic"] == topic["title"]
        ]

    index_template = environment.get_template("index.html")
    index_template_stream = index_template.stream(topics=topics)
    index_template_stream.dump("output/index.html")


if __name__ == "__main__":
    server = Server()
    server.watch("templates/*.html", make_site)
    server.serve(root="output/")
