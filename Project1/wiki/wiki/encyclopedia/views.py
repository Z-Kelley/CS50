from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from . import util
from .forms import EntryForm, NewEntryForm
import random
from django.db.models import Q
from .models import Entry, NewEntry
from django import forms
from markdown2 import Markdown


from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, entry):
    markdowner = Markdown()
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/DoesNotExist.html", {
            "title": entry
        })
    else:
    
        return render(request, "encyclopedia/entry.html",{
            "entry": markdowner.convert(util.get_entry(entry)),
            "title": entry
        })

def randomPage(request):
    markdowner = Markdown()
    entryList = util.list_entries()
    randomChoice = random.choice(entryList)
    random_page = util.get_entry(randomChoice)
    return render(request, "encyclopedia/entry.html",{
        "entry": markdowner.convert(util.get_entry(randomChoice)),
        "title": randomChoice
    })

def createNew (request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            if((util.get_entry(title) is None) or (form.cleaned_data["edit"] is True)):
                util.save_entry(title, description)
                return HttpResponseRedirect(reverse("title", kwargs={
                    "entry": title
                    }))
            else:
                return render(request, "encyclopedia/createnew.html", {
            "form": form,
            "existing": True,
            "entry": title
            })
        return render(request, "encyclopedia/createnew.html", {
        "form": form,
        "existing": False,
        })
    else:
        return render(request, "encyclopedia/createnew.html", {
    "form": NewEntryForm()
    })


def searchResults (request):
    query = request.GET.get('q', '')
    if (util.get_entry(query) is not None):
        return render(request, "encyclopedia/entry.html",{
        "entry": util.get_entry(query),
        "title": query
    })
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if query.upper() in entry.upper():
                subStringEntries.append(entry)
        return render(request, "encyclopedia/searchResults.html", {
        "entries": subStringEntries,
        "query": query,
        "search": True,
        "entry": util.get_entry(entry)
        })
    
def editPage (request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/DoesNotExist.html", {
            "title": entry
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["description"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/createnew.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "title": form.fields["title"].initial
            })
    
def saveEdit(request):
    markdowner = Markdown()
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        util.save_entry(title, description)
    return render(request, "encyclopedia/entry.html",{
        "entry": markdowner.convert(util.get_entry(title)),
        "title": title
    })

