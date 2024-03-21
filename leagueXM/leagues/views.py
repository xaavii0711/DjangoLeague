from django import *
from django.http import * 
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse

from django import forms
from django.shortcuts import redirect

from .models import Equip
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    userstr = str(request.user)
    return HttpResponse("profile: "+userstr)

def index(request):
    return render(request,"index.html")

def edita_equip(request):
    return render(request, "edita_equip_ajax.html")


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
    

class CrearLiga(forms.ModelForm):
    class Meta:
        model = Lliga
        fields = ['nom']

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if Lliga.objects.filter(nom=nom).exists():
            raise forms.ValidationError("Ya existe una liga con este nombre.")
        return nom
    
def crear_lliga(request):
    if request.method == 'POST':
        form = CrearLiga(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crearLliga')
    else:
        form = CrearLiga()
    return render(request, 'crearLliga.html', {'form': form})

class CrearEquipo(forms.ModelForm):
    class Meta:
        model = Equip
        fields = ['nom', 'ciutat', 'fundacio', 'lliga']

    def clean_nom(self):
        nom = self.cleaned_data['nom']
        if Equip.objects.filter(nom=nom).exists():
            raise forms.ValidationError("Ya existe un equipo con este nombre.")
        return nom
    
def crear_equipo(request):
    if request.method == 'POST':
        form = CrearEquipo(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_equipo')
    else:
        form = CrearEquipo()
    return render(request, 'crearEquipo.html', {'form': form})


