import json
import os

import markdown2
from jinja2 import FileSystemLoader, Environment
from livereload import Server


OUTPUT_DIRNAME = "docs"


def load_text_from_file(filepath):
    with open(filepath) as text_file:
        text = text_file.read()
        return text


def make_site():
    json_config = json.loads(load_text_from_file("config.json"))
    articles = json_config["articles"]
    topics = json_config["topics"]
    topic_titles = {topic["slug"]: topic["title"] for topic in topics}

    environment = Environment(
        loader=FileSystemLoader("templates"), autoescape=True
    )
    article_template = environment.get_template("article.html")

    if not os.path.exists(OUTPUT_DIRNAME):
        os.mkdir(OUTPUT_DIRNAME)

    for article in articles:
        markdown_path = "articles/{}".format(article["source"])
        markdown_content = load_text_from_file(markdown_path)
        html_content = markdown2.markdown(markdown_content)
        filename, _ = os.path.splitext(os.path.basename(article["source"]))

        article["url"] = "{}.html".format(filename)
        topic_title = topic_titles.get(article["topic"])

        article_template_stream = article_template.stream(
            name=article["title"],
            topic=topic_title,
            topic_slug=article["topic"],
            content=html_content,
        )
        article_template_stream.dump(
            "{}/{}.html".format(OUTPUT_DIRNAME, filename)
        )

    for topic in topics:
        topic["articles"] = [
            article
            for article in articles
            if article["topic"] == topic["slug"]
        ]

    index_template = environment.get_template("index.html")
    index_template_stream = index_template.stream(topics=topics)
    index_template_stream.dump("{}/index.html".format(OUTPUT_DIRNAME))


if __name__ == "__main__":
    server = Server()
    server.watch("templates/*.html", make_site)
    server.serve(root=OUTPUT_DIRNAME)
