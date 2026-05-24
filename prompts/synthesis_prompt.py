from schemas.search import SearchResult
from jinja2 import Template

SYSTEM_PROMPT = """
    You are a helpful research assistant. Your task is to combine article summaries from various sources. Just use information within summaries that you have. Do NOT invent new information. If you are not sure about any information, say so.
    The output should be formated in JSON format as followed:
    {
        "title": "a str title for all articles summaries",
        "summary": "a summarization of all summaries across articles",
        "insights": list of 3 core insight of form [{"claim":"a key insight claim from one of the summaries", "source": "http link to source of the claim"}],
        "citations": [list of all the sources]
    }
"""

combine_template = """
    Combine the following article summaries:
    {% for article in articles %}
    {{ article }}
    {% endfor %}
"""

summary_template = """
    <article>
    <title> {{ title }} </title>
    <summary> {{ summary }} </summary>
    </article>
"""

summary_template = Template(summary_template)
combine_template = Template(combine_template)

def parse_summaries(summaries:list[SearchResult])->str:
    articles = []
    for s in summaries:
        article_summary = summary_template.render(title=s.title, 
                                                  summary=s.content,
                                                  url = s.url)
        articles.append(article_summary)
    prompt = combine_template.render(articles= articles)
    return prompt