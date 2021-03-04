import os
from pathlib import Path

import pandas as pd
import sweetviz as sv
from logml.commons.config import Config
from logml.eda_tools.report_generator import ReportGenerator
from logml.eda_tools.utils import EligibleDataProfilers
from pandas_profiling import ProfileReport
from papermill import PapermillExecutionError, execute_notebook


class BaseProfiler:
    """Interface for profiling utilities.

    Profiler takes a csv file and generates a html report with
    basic descriptive statistics.
    """

    PROFILING_ARTIFACT = 'report.html'

    def __init__(self, cfg: Config):
        self._cfg = cfg
        self.__parse_cfg()
        self.__create_destination_folder()

    def __create_destination_folder(self):
        os.makedirs(self._dst_folder, exist_ok=True)

    def __parse_cfg(self):
        """Retrieves required params from config."""
        self._filename = self._cfg[['global_params', 'dataset_path']]
        self._dst_folder = self._cfg[['global_params', 'destination_folder']]

        # Update temporary parameters.
        self._cfg.cfg['temp_params'] = dict(profiler_id=self.PROFILER_ID)

    def generate_profile(self):
        """Produces and saves the result profile in html form.

        NOTE: interface method should be implemented!
        """
        raise NotImplementedError('Please use one of the inherited classes.')


@EligibleDataProfilers.register_profiler
class PandasProfiler(BaseProfiler):
    """Basic wrapper around pandas_profiling library."""

    PROFILING_ARTIFACT = 'pandas_profiling_artifact.html'
    PROFILER_ID = 'pandas_profiler'

    def __init__(self, cfg: Config):
        super().__init__(cfg)

    def generate_profile(self):
        """Produces and saves the result profile in html form."""
        profile = ProfileReport(
            pd.read_csv(self._filename),
            title=f'{self._filename} profile',
            explorative=True)

        profile.to_file(
            os.path.join(self._dst_folder, self.PROFILING_ARTIFACT))


@EligibleDataProfilers.register_profiler
class SweetvizProfiler(BaseProfiler):
    """Basic wrapper around sweetviz library."""

    PROFILING_ARTIFACT = 'sweetviz_artifact.html'
    PROFILER_ID = 'sweetviz_profiler'

    def __init__(self, cfg: Config):
        super().__init__(cfg)

    def generate_profile(self):
        """Produces and saves the result profile in html form."""
        profile = sv.analyze(
            pd.read_csv(self._filename))

        profile.show_html(
            os.path.join(self._dst_folder, self.PROFILING_ARTIFACT),
            open_browser=False)


def get_profiling_report_base_nb_path():
    return 'src/logml/eda_tools/data_profiling_report_template.ipynb'


@EligibleDataProfilers.register_profiler
class LogMLProfiler(BaseProfiler):
    """Custom LogMl profiler."""

    PROFILING_ARTIFACT = 'logml_artifact'
    PROFILER_ID = 'logml_profiler'

    def __init__(self, cfg: Config):
        super().__init__(cfg)

    def generate_profile(self):
        """
        Generates & execute data profiling notebook and saves it together with
        its html version.
        """
        # Result notebook path.
        output_path = \
            Path(self._dst_folder) / f'{self.PROFILING_ARTIFACT}.ipynb'
        # Generate notebook.
        ReportGenerator(
            get_profiling_report_base_nb_path(), self._cfg
        ).generate().dump(output_path.as_posix())

        # Run notebook (rewrite generated template).
        execute_notebook(
            output_path.as_posix(), output_path.as_posix(),
            parameters=dict(CFG=self._cfg.cfg)),

        # Render html.
        jupyter_command = f'jupyter nbconvert {output_path} ' \
            '--to html_embed --template toc2 ' \
            '--TagRemovePreprocessor.remove_cell_tags \'invisible\' ' \
            '--TemplateExporter.exclude_input=True'
        os.system(jupyter_command)
