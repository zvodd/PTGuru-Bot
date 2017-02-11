from jinja2 import Environment, DictLoader, select_autoescape
from flask import Flask

"""
mock server for unit testing with rss feeds
"""

app = Flask(__name__)

TEMPLATES = DictLoader({"base.xml" : r"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
{%- for item in items %}
    {% include "items.xml" with context -%}
{% endfor %}
</channel>
</rss>
""",
                    "items.xml": r"""
<item>
    <title>{{item['title']}}</title>
    <description>{{item['desc']}}</description>
    <link>{{item['link']}}</link>
    <pubDate>{{item['date']}}</pubDate>
</item>
"""})


J2ENV = Environment(
    loader=TEMPLATES,
    autoescape=select_autoescape(['html', 'xml'])
)


# global GLOBAL_ITEMS
GLOBAL_ITEMS = {}


@app.route('/feed/<id>')
def render_feed(id='DEFAULT'):
    # global GLOBAL_ITEMS
    res = J2ENV.get_template("base.xml").render(items=GLOBAL_ITEMS.get(id,GLOBAL_ITEMS['DEFAULT']))
    return(res)


@app.route('/set/<start>/<end>/<id>')
def set_feed(start,end,id):
    # global GLOBAL_ITEMS
    GLOBAL_ITEMS[id] = gen_items(int(start),int(end))
    return "updated feed"


def gen_items(start,end):
    items = []
    for i in range (start, end):
        item = dict([
            ("title", i),
            ("desc", i),
            ("link", i),
            ("date", i),
            ])
        items.append(item)
    return items



GLOBAL_ITEMS = {'DEFAULT':gen_items(0, 10)}

if __name__ == '__main__':
    import argparse
    parser= argparse.ArgumentParser()
    parser.add_argument('start', metavar='N', type=str, nargs='?', default=0)
    parser.add_argument('end', metavar='N', type=int, nargs='?', default=10)
    parser.add_argument('server', metavar='S', type=bool, nargs='?', default=True)
    parser.add_argument('host', metavar='H', type=str, nargs='?', default='127.0.0.1')
    parser.add_argument('port', metavar='P', type=str, nargs='?', default="5000")
    args = parser.parse_args()

    if not args.server:
        items = gen_items(args.start, args.end)
        res = J2ENV.get_template("base.xml").render(items=items)
        print (res)
    else:
        app.run(  host=args.host, port=int(args.port))