import yaml
from pathlib import Path
from neuronautics.utils.helpers import file_path

LAYOUT_FILE = file_path('layout.yml')

class Layout:
    def __init__(self):
        self.layouts = self.load()

    def __getstate__(self):
        return dict()

    def __setstate__(self, state):
        pass

    def save(self):
        with open(LAYOUT_FILE, 'w') as stream:
            yaml.dump(self.layouts, stream)

    def load(self):
        if Path(LAYOUT_FILE).exists():
            with open(LAYOUT_FILE, 'r') as stream:
                data = yaml.full_load(stream)
                if not data:
                    return list()
                return data
        else:
            return list()

    def names(self):
        return sorted([layout.get('name') for layout in self.layouts])

    def new(self, name, cols, rows):
        self.layouts.append({'name': name,
                             'rows': rows, 'cols': cols,
                             'layout': self.default_config(cols, rows),
                             'current': False})
        self.save()

    def _get(self, name):
        for layout in self.layouts:
            if layout.get('name') == name:
                return layout

    def update(self, name, cell_values):
        layout = self._get(name)
        layout['layout'] = cell_values
        self.save()

    def get_layout(self, name):
        layout = self._get(name)
        return layout.get('layout')

    def get_shape(self, name):
        layout = self._get(name)
        return int(layout['cols']), int(layout['rows'])

    @classmethod
    def int_to_abc(cls, n):
        result = ""
        while n > 0:
            n, rem = divmod(n - 1, 26)
            result = chr(65 + rem) + result
        return result

    def default_config(self, cols, rows):
        cell_values = [[f"{self.int_to_abc(c+1)}{r+1}" for c in range(cols)] for r in range(rows)]
        return cell_values

    def column_headers(self, cols):
        return [self.int_to_abc(c+1) for c in range(cols)]

    def row_headers(self, rows):
        return [str(r+1) for r in range(rows)]

    def delete(self, name):
        for ix, layout in enumerate(self.layouts):
            if layout.get('name') == name:
                self.layouts.pop(ix)
                self.save()
                return True
        return False

    def set_current_layout(self, name):
        for layout in self.layouts:
            layout['current'] = layout.get('name') == name
        self.save()

    def is_current_layout(self, name):
        return self._get(name).get('current', False)

    def current(self):
        for layout in self.layouts:
            if layout.get('current', False):
                return layout.get('layout')

