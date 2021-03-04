class EligibleDataProfilers:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if EligibleDataProfilers.__instance is None:
            EligibleDataProfilers.__instance = object.__new__(cls)
            EligibleDataProfilers.__instance.profilers = dict()

        return EligibleDataProfilers.__instance

    @classmethod
    def register_profiler(cls, profiler):
        EligibleDataProfilers().profilers.update({
            profiler.PROFILER_ID: profiler})
        return profiler
