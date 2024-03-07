from django.contrib import admin

from .models import *

# class PartitAdmin(admin.ModelAdmin):
#     list_display = ('local','visitant','gols_local','gols_visitant')

class EventInline(admin.TabularInline):
    model = Event
    fields = ["temps","tipus","jugador","equip"]
    ordering = ("temps",)
    extra= 0
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "equip":
            partit_id = request.resolver_match.kwargs.get('object_id')
            if partit_id:
                partit = Partit.objects.get(id=partit_id)
                equips_ids = [partit.local.id, partit.visitant.id]
                qs = Equip.objects.filter(id__in=equips_ids)
                kwargs["queryset"] = qs
        elif db_field.name == "jugador":
            partit_id = request.resolver_match.kwargs.get('object_id')
            if partit_id:
                partit = Partit.objects.get(id=partit_id)
                equips_ids = [partit.local.id, partit.visitant.id]
                qs = Jugador.objects.filter(equip__id__in=equips_ids)
                kwargs["queryset"] = qs
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class PartitAdmin(admin.ModelAdmin):
        # podem fer cerques en els models relacionats
        # (noms dels equips o títol de la lliga)
    search_fields = ["local__nom","visitant__nom","lliga__nom"]
        # el camp personalitzat ("resultats" o recompte de gols)
        # el mostrem com a "readonly_field"
    readonly_fields = ["resultat",]
    list_display = ["local","visitant","resultat","lliga","inici"]
    ordering = ("-inici",)
    inlines = [EventInline,]

    def resultat(self,obj):
        gols_local = obj.event_set.filter(
            tipus=Event.EventType.GOL,
            equip=obj.local).count()
        gols_visit = obj.event_set.filter(
   		    tipus=Event.EventType.GOL,
            equip=obj.visitant).count()
        return "{} - {}".format(gols_local,gols_visit)
     


admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)
admin.site.register(Partit, PartitAdmin)
admin.site.register(Event)
