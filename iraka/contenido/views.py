from django.db.models import Avg, Count
from django.shortcuts import render

from .models import (
    ConfiguracionSitio,
    EnlaceReserva,
    Experiencia,
    Habitacion,
    InformacionContacto,
    SeccionAcercaDe,
    SeccionHero,
)


def inicio(request):
    configuracion = ConfiguracionSitio.objects.order_by("-id").first()
    hero = SeccionHero.objects.filter(esta_activo=True).order_by("-id").first()
    acerca_de = SeccionAcercaDe.objects.filter(esta_activo=True).order_by("-id").first()
    habitaciones = (
        Habitacion.objects.filter(esta_activo=True)
        .prefetch_related("imagenes", "amenidades")
        .order_by("orden_mostrar", "nombre")
    )
    experiencias = (
        Experiencia.objects.filter(esta_activo=True)
        .prefetch_related("imagenes")
        .order_by("orden_mostrar", "-creado_en")
    )
    enlaces_reserva = EnlaceReserva.objects.filter(esta_activo=True).order_by(
        "orden_mostrar",
        "nombre_plataforma",
    )
    contacto = InformacionContacto.objects.order_by("-id").first()

    # Credenciales — calculadas desde la BD
    stats_experiencias = Experiencia.objects.filter(
        esta_activo=True,
        calificacion__isnull=False,
    ).aggregate(
        promedio=Avg("calificacion"),
        total=Count("id"),
    )
    calificacion_promedio = stats_experiencias["promedio"]
    total_resenas = stats_experiencias["total"]
    total_habitaciones = Habitacion.objects.filter(esta_activo=True).count()

    context = {
        "configuracion": configuracion,
        "hero": hero,
        "acerca_de": acerca_de,
        "habitaciones": habitaciones,
        "experiencias": experiencias,
        "enlaces_reserva": enlaces_reserva,
        "contacto": contacto,
        # Credenciales
        "calificacion_promedio": round(calificacion_promedio, 1) if calificacion_promedio else None,
        "total_resenas": total_resenas,
        "total_habitaciones": total_habitaciones,
    }
    return render(request, "inicio.html", context)