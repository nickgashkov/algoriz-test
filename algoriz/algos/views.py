from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView

from algoriz.algos.forms import AlgoForm
from algoriz.algos.models import Algo


class AlgoListView(ListView):
    model = Algo


class AlgoDetailView(DetailView):
    model = Algo


class AlgoCreateView(CreateView):
    model = Algo
    form_class = AlgoForm
