from cement.core import controller


class Merger(controller.CementBaseController):
    class Meta:
        label = "importer"

    @controller.expose(hide=False)
    def performers(self):
        pass