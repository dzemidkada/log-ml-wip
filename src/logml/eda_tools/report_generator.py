import nbformat as nbf
from logml.commons.config import Config
from logml.eda_tools.profiling_tools.utils import EligibleProfilingTools


class ReportGenerator:

    def __init__(self, template_nb_path: str, cfg: Config, nbf_version=4):
        self.__template_nb_path = template_nb_path
        self.__cfg = cfg
        self.__nbf_version = nbf_version


    def generate(self):
        # Read template notebook
        self.__result_nb = nbf.read(
            self.__template_nb_path, as_version=self.__nbf_version)

        # Generate required views
        profiler_id = self.__cfg[['temp_params', 'profiler_id']]
        views = self.__cfg[[f'{profiler_id}_config', 'views']]
        for view_cfg in views:
            view_id = view_cfg['id']

            cells_to_add = (
                EligibleProfilingTools().views[view_id](view_cfg)
                .get_cells()
            )

            self.__result_nb['cells'].extend(cells_to_add)

        return self

    def dump(self, output_nb_path: str):
        nbf.write(self.__result_nb, output_nb_path)
