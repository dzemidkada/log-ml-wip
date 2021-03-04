from logml.eda_tools.profiling_tools.utils import EligibleProfilingTools
from logml.eda_tools.profiling_tools.cell import Cell


@EligibleProfilingTools.register_view
class SummaryView:
    """
    Simple dataset summary workflow:
     - head/tail
     - simple descriptive statistics
     - numerical/categorical column lists
    """
    VIEW_ID = 'summary'

    def __init__(self, cfg: dict):
        self._cfg = cfg

    def get_cells(self):
        # Define required cells (configs).
        cell_cfgs = [
            dict(cell_type='markdown', content='# Summary'),
            dict(cell_type='markdown', content='### Head'),
            dict(cell_type='code', content='''
                display(df.head())
            '''),
            dict(cell_type='markdown', content='### Tail'),
            dict(cell_type='code', content='''
                display(df.tail())
            '''),
            dict(cell_type='markdown', content='### Summary statistics'),
            dict(cell_type='code', content='''
                display(df.describe())
            '''),
            dict(cell_type='markdown', content='### Numeric columns'),
            dict(cell_type='code', content='''
                sorted(list(df.select_dtypes(include=[np.number]).columns))
            '''),
            dict(cell_type='markdown',
                 content='### Non-numerical (e.g. categorical) columns'),
            dict(cell_type='code', content='''
                sorted(list(df.select_dtypes(include=[np.object]).columns))
            ''')
        ]
        # Generate actual Jupyter cells.
        return [
            Cell(cell_cfg)()
            for cell_cfg in cell_cfgs
        ]
