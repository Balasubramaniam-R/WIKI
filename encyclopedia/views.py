from django.shortcuts import render,redirect
from django.http import HttpResponse
from markdown2 import markdown
from django import forms
import re
from random import randint
from . import util

class NewForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': "Enter title", 'class': 'col-sm-6 mx-auto p-2'}
    ))
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': "Enter Markdown content", 'class': 'col-sm-9 mx-auto p-2'}
    ))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get(request, title):
    markdown_content=util.get_entry(title)
    html = ''
    if markdown_content:
       html=markdown(markdown_content)
    return render(request,'encyclopedia/entry.html', {'content': html, 'title': title})

def search(request):

    title=request.POST['q'].lower()
    entries=util.list_entries()
    for entry in entries:
        if entry.lower()==title:
          return redirect('encyclopedia:get',entry)
    # search start ...
    matched=[]
    for entry in entries:
        if re.search(title,entry.lower()):
            matched.append(entry)

    # search ends .
    message= ''
    if not matched: # No match found
          message = 'Could not find what you are looking for.'
          print(matched)
    
    return render(request,'encyclopedia/search.html', {'entries': matched, 'message': message})

def add(request):
    if request.method=="POST":
        message=""
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].lower()
            content = form.cleaned_data["content"]
            entries=set(entry.lower() for entry in util.list_entries())
            if title not in entries:
                if title[0].islower():
                     title = title.capitalize()
                util.save_entry(title,content)
                return redirect('encyclopedia:get',title)
            else:
                message = "A page with this title already exists!, please enter a unique title."
                form = NewForm() 
        else:
            form = NewForm()
        return render(request,'encyclopedia/add.html', {"form" : form, "message" : message})
    else:
        return render(request,'encyclopedia/add.html', {"form" : NewForm(), "message" : ""})

def edit(request):
    if request.method=="POST":
         form = NewForm(request.POST)
         if form.is_valid():
          title = form.cleaned_data["title"]
          content = form.cleaned_data["content"]
          if title[0].islower():
              title = title.capitalize()
          util.save_entry(title,content)
          return redirect('encyclopedia:get',title)
    title = request.GET["edit"]
    content=util.get_entry(title)
    form = NewForm(initial={'title':title,'content':content})
    return render(request,'encyclopedia/edit.html',{"form": form})

def random(request):
    entries = util.list_entries()
    idx=randint(0,len(entries))
    title = entries[idx-1]
    return redirect('encyclopedia:get',title)
        
