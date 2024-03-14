from django import *
from django.http import * 
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.shortcuts import render

from django import forms
from django.shortcuts import redirect
 

def index(request):
    return render(request,"index.html")


class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
 
def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })




def classificacio(request, lliga_id):
    lliga = get_object_or_404(Lliga, pk=lliga_id)
    equips = lliga.equip_set.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partit_set.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partit_set.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append( (punts,equip.nom) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga":lliga,
                })
    
# class LligaForm(forms.ModelForm):
#     class Meta:
#         model = Lliga
#         fields = ["nom"]
    
# def crearLliga(request):
#     form = LligaForm()
#     messageError  = ""
#     if request.method == "POST":
#         form = LligaForm(request.POST)
#         if form.is_valid():
#             nom_lliga = form.cleaned_data.get("nom")
#             if Lliga.objects.filter(nom=nom_lliga).exists():
#                 messageError = "El nom de la lliga ja existeix"
#             else:
#                 messageError = "La lliga " + nom_lliga + " s'ha creat correctament"
#                 form.save()
    
#     return render(request, "crearLliga.html", {"form": form, "message": messageError})


