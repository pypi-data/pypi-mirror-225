import click
import os
import jinja2
import re
import json

# open templates/index.html, relative to the module
with open(os.path.join(os.path.dirname(__file__), "templates/index.html"), 'r') as f:
    template = f.read()

env = jinja2.Environment()
template = env.from_string(template)

@click.command()
@click.argument('path', default=".")
def main(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    title = None
    description = None
    author = None

    functions = {}

    for i, l in enumerate(lines):
        if l.startswith("## title"):
            title = l.split(":")[1].strip()
        elif l.startswith("## description"):
            # keep reading until next line starts with title:, :author:, or no #
            description = [l.split(":")[1].strip()]
            for j, l2 in enumerate(lines[i+1:]):
                if l2.startswith("## title") or l2.startswith("## author") or not l2.startswith("##"):
                    break

                description.append(l2.strip().replace("## ", ""))

            description = "<br>".join(description)
        elif l.startswith("## author"):
            author = ":".join(l.split(":")[1:]).strip()

            # search for http(s)://domain.com 
            author_link = re.search(r"http(s)?://[^\s]+", author)

            if author_link:
                author_link = author_link.group()
                author = author.replace(author_link, '')
                author = f'<a href="{author_link}">{author}</a>'

        if l.strip().startswith("Make"):
            function_name = l.split("Make")[1].split("[")[0].strip()

            # search next lines for docs
            docs = []
            for _, l2 in enumerate(lines[i+1:]):
                if not l2.strip().startswith("##"):
                    break

                docs.append(l2.strip())

            functions[function_name] = "\n".join(docs).replace("## ", "")
    
    # render template
    code = "".join([l for l in lines if not l.startswith("##") and not l == "\n"]).strip()

    result = template.render(
        title=title,
        description=description,
        author=author,
        functions=functions,
        code=code
    )

    cells = {
        "cells": [
            {
                "type": "code",
                "data": lines,
            }
        ]
    }

    path = os.path.splitext(path)[0] + "-docs"
        
    if not os.path.exists(path):
        os.makedirs(path)
        
    with open(os.path.join(path, "index.html"), 'w') as f:
        f.write(result)

    with open(os.path.join(path, "index.vicnb"), 'w') as f:
        f.write(json.dumps(cells))

    with open(os.path.join(path, "index.vic"), 'w') as f:
        f.write("".join(lines))

    with open(os.path.join(path, "styles.css"), 'w') as f:
        styles = os.path.join(os.path.dirname(__file__), "templates/styles.css")
        f.write(
            open(styles, 'r').read()
        )

    print(f"✨ Documentation is saved to {path}/index.html ✨")

if __name__ == '__main__':
    main()