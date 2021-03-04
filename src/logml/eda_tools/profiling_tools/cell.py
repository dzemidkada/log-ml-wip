import nbformat as nbf


class Cell:
    """
    Wrapper for code/markdown Jupyter cells.

    Code cell:
        'do something'
    Markdown cell:
        '#* Description'
    """

    def __init__(self, cfg: dict, nbf_version=4):
        self._cfg = cfg
        self._nbf_version = nbf_version

    def __call__(self):
        constructor = ('new_markdown_cell'
                       if self._cfg['cell_type'] == 'markdown' else
                       'new_code_cell'
                       )

        cell = getattr(nbf.versions[self._nbf_version], constructor)(
            self._cfg['content'])

        return cell
