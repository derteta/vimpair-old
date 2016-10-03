class VimInterface(object):

    def __init__(self, vim=None, *a, **k):
        super(VimInterface, self).__init__(*a, **k)
        self._vim = vim

    @property
    def current_contents(self):
        return reduce(lambda s1, s2: s1 + '\n' + s2, self._vim.current.buffer[:])
