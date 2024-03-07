from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from django.utils import timezone


from leagues.models import *

faker = Faker(["es_CA", "es_ES"])


class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga, created = Lliga.objects.get_or_create(nom=titol_lliga)
        if not created:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return

        print("Creem la nova lliga: {}".format(titol_lliga))

        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0, len(prefixos) - 1)]
            if prefix:
                prefix += " "
            nom = prefix + ciutat
            equip = Equip.objects.create(nom=nom, lliga=lliga, fundacio=faker.date_between(start_date='-100y', end_date='-10y'))

            print("Creem jugadors de l'equip " + nom)
            for j in range(25):
                nom = faker.first_name()
                edat = randint(18, 37)
                jugador = Jugador.objects.create(nom=nom, equip=equip, edat=edat)

        print("Creem partits de la lliga")
        equips = list(lliga.equip_set.all())
        for local in equips:
            for visitant in equips:
                if local != visitant:
                    partit = Partit.objects.create(local=local, visitant=visitant, lliga=lliga)
                    partit.local = local
                    partit.visitant = visitant
                    partit.save()
                    
                    gols_local = randint(0,7)
                    gols_visitant = randint(0,6)
                    for i in range(0,gols_local):
                        jugador = partit.local.jugador_set.all()[randint(0,24)]
                        gol = Event(
                            tipus=Event.EventType.GOL,
                            jugador=jugador,
                            equip=partit.local,
                            partit=partit,
                            temps=timezone.now()
                        )
                        gol.save()
                        partit.event_set.add(gol)
                    for i in range(0,gols_visitant):
                        jugador = partit.visitant.jugador_set.all()[randint(0,24)]
                        gol = Event(
                            tipus=Event.EventType.GOL,
                            jugador=jugador,
                            equip=partit.visitant,
                            partit=partit,
                            temps=timezone.now()
                        )
                        gol.save()
                        partit.event_set.add(gol)