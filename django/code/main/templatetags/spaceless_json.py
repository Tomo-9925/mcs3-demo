from django.template.base import Node
from django.template.library import Library
from django.utils import safestring

register = Library()

class SpacelessJsonNode(Node):
  def __init__(self, nodelist):
    self.nodelist = nodelist

  def render(self, context):
    import json, unicodedata
    content = self.nodelist.render(context).strip()
    content = unicodedata.normalize('NFKC', content)
    json_data = json.loads(content)
    return safestring.mark_safe(json.dumps(json_data, ensure_ascii=False))


@register.tag(name='spaceless_json')
def spaceless_json(parser, token):
  """
  Remove whitespace inside json-data.

  Example usage::

    <script type="application/id+json">
    {% spaceless_json %}
      {
        "foo":  "bar",

                "foo2":
                        "bar2"
      }
    {% endspaceless_json %}
    </script>

  This example returns this string::

      <script type="application/id+json">{"foo":"bar", "foo2":"bar2"}</script>
  """
  nodelist = parser.parse(('endspaceless_json',))
  parser.delete_first_token()
  return SpacelessJsonNode(nodelist)
