class VimInterface(object):

    def __init__(self, vim=None, *a, **k):
        super(VimInterface, self).__init__(*a, **k)
        self._vim = vim

    @property
    def current_contents(self):
        return reduce(lambda s1, s2: s1 + '\n' + s2, self._vim.current.buffer[:])
    @current_contents.setter
    def current_contents(self, new_content):
        current_buffer = self._vim.current.buffer
        del current_buffer[:]
        for index, line in enumerate(new_content.split('\n')):
            if index < len(current_buffer):
                current_buffer[index] = line
            else:
                current_buffer.append(line)

    @property
    def cursor_position(self):
        # Vim counts rows 1-based, but columns 0-based, we unify this
        position = self._vim.current.window.cursor
        return (position[0] - 1, position[1])
