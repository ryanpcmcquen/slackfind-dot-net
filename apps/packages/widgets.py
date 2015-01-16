from lib.widgets import MySelectMultiple

class RepositorySelectWidget(MySelectMultiple):

    def render(self, name, value, **kwargs):
        kwargs['template_name'] = 'packages/widgets/repository_select_widget.html'
        return super(RepositorySelectWidget, self).render(name, value, **kwargs)

