from cement.core import controller, foundation


class OediController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = ''

    @controller.expose(hide=False)
    def default(self):
        print "Hello world"


class Oedi(foundation.CementApp):
    class Meta:
        label = 'Oedi'
        base_controller = OediController
