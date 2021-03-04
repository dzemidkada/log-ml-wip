import logging

from logml.commons.config import Config
from logml.commons.logging_utils import prepare_logger
from logml.eda_tools.utils import EligibleDataProfilers


class ProfilersRunner:
    """Simple data profilers handler."""
    __logger = logging.getLogger('logml')
    __logger.propagate = False

    def __init__(self, cfg: Config):
        self._cfg = cfg

        if not self.__logger.hasHandlers():
            prepare_logger(self.__logger)

    def run(self):
        """
        Invokes required profilers according to 'profilers_to_run' cfg section.
        """
        self.__logger.info('Running required data profilers...')

        for profiler_id in self._cfg['profilers_to_run']:
            self.__logger.debug(f'Generate "{profiler_id}" EDA report')

            EligibleDataProfilers().profilers[profiler_id](
                self._cfg).generate_profile()
