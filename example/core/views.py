from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from example.core.forms import ChainedForm, FarmFormset, ReferencesTestForm, ChainedForm2, MultipleTestForm
from example.core.models import ReferencesTest, MultipleTest


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


def detail(request, pk):
    obj = ReferencesTest.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReferencesTestForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("example-list"))
    else:
        if request.GET:
            form = ReferencesTestForm(initial=request.GET, instance=obj)
        else:
            form = ReferencesTestForm(instance=obj)

    return render_to_response('base.html', {'form': form}, context_instance=RequestContext(request))


def advanced(request, form_type = 1):
    FormClass = ChainedForm
    if form_type == 2:
        FormClass = ChainedForm2

    if request.method == 'POST':
        form = FormClass(request.POST)
    else:
        if request.GET:
            form = FormClass(initial=request.GET)
        else:
            form = FormClass()

    return render_to_response('advanced.html', {'form': form, 'form_name' : FormClass.__name__ }, context_instance=RequestContext(request))


def formset(request):

    if request.method == 'POST':
        formset = FarmFormset(request.POST)
    else:
        if request.GET:
            formset = FarmFormset(initial=request.GET)
        else:
            formset = FarmFormset()

    return render_to_response('formset.html', {'formset': formset}, context_instance=RequestContext(request))


def multiple(request):

    form = MultipleTestForm()
    if request.method == 'POST':
        print "RPD", request.raw_post_data
        form = MultipleTestForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("example-multiple-list"))
    return render_to_response('base.html', {'form': form}, context_instance=RequestContext(request))


def multiple_edit(request, pk):

    instance = MultipleTest.objects.get(pk=pk)
    form = MultipleTestForm(instance=instance)
    if request.method == 'POST':
        print "RPD", request.raw_post_data
        form = MultipleTestForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("example-multiple-list"))
    return render_to_response('base.html', {'form': form}, context_instance=RequestContext(request))


def multiple_list(request):
    rlist = MultipleTest.objects.all()
    return render_to_response('list.html', {'object_list': rlist}, context_instance=RequestContext(request))
