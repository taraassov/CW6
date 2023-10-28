from django.views.generic import ListView, DetailView

from blogpost.models import Blogpost


class BlogpostListView(ListView):
    model = Blogpost

    extra_context = {
        'title': 'Наш блог!'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogpostDetailView(DetailView):
    model = Blogpost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
