import json

import markdown2
from jinja2 import FileSystemLoader, Environment, select_autoescape


def load_text_from_file(filepath):
    with open(filepath) as text_file:
        text = text_file.read()
        return text


if __name__ == "__main__":
    json_config = json.loads(load_text_from_file("config.json"))
    articles = json_config["articles"]
    md_path = "articles/{}".format(articles[0]["source"])
    article_name = articles[0]["title"]
    md_content = load_text_from_file(md_path)
    html_content = markdown2.markdown(md_content)
    # print(html_content)

    environment = Environment(
        loader=FileSystemLoader("templates")
    )
    template = environment.get_template("article.html")
    result = template.render(name=article_name, content=html_content)
    print(result)
