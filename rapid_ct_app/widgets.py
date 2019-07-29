import json
from wtforms.widgets import Select, HTMLString

class ChosenSelect(Select):

    def __init__(self, multiple=False, renderer=None, options={}):
        super(ChosenSelect, self).__init__(multiple=multiple)
        self.renderer = renderer
        options.setdefault('width', '100%')
        self.options = options

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if kwargs.get("readonly"):
            kwargs['disabled'] = 'disabled'
        html = []
        # render the select
        if self.renderer:
            html.append(self.renderer(self, field, **kwargs))
        else:
            html.append(super(ChosenSelect, self).__call__(field, **kwargs))
        # attach the chosen initiation with options
        html.append(
            '<script>$("#%s").chosen(%s);</script>\n'
            % (kwargs['id'], json.dumps(self.options))
        )
        # return the HTML (as safe markup)
        return HTMLString('\n'.join(html))