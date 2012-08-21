from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from example.core.forms import FruitForm, ChainedForm, FarmFormset, ReferencesTestForm
from example.core.models import ReferencesTest


def add(request):

    if request.method == 'POST':
        form = ReferencesTestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("example-list"))
    else:
        if request.GET:
            form = ReferencesTestForm(initial=request.GET)
        else:
            form = ReferencesTestForm()

    return render_to_response('base.html', {'form': form}, context_instance=RequestContext(request))


def list(request):

    rlist = ReferencesTest.objects.all()
    return render_to_response('list.html', {'object_list': rlist}, context_instance=RequestContext(request))



def advanced(request):

    if request.method == 'POST':
        form = ChainedForm(request.POST)
    else:
        if request.GET:
            form = ChainedForm(initial=request.GET)
        else:
            form = ChainedForm()

    return render_to_response('advanced.html', {'form': form}, context_instance=RequestContext(request))


def formset(request):

    if request.method == 'POST':
        formset = FarmFormset(request.POST)
    else:
        if request.GET:
            formset = FarmFormset(initial=request.GET)
        else:
            formset = FarmFormset()

    return render_to_response('formset.html', {'formset': formset}, context_instance=RequestContext(request))
