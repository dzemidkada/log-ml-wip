class EligibleProfilingTools:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if EligibleProfilingTools.__instance is None:
            EligibleProfilingTools.__instance = object.__new__(cls)
            EligibleProfilingTools.__instance.views = dict()

        return EligibleProfilingTools.__instance

    @classmethod
    def register_view(cls, view):
        EligibleProfilingTools().views.update({
            view.VIEW_ID: view})
        return view
