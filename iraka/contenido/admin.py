from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin as UnfoldModelAdmin, StackedInline, TabularInline

from .models import (
    Amenidad,
    ConfiguracionSitio,
    EnlaceReserva,
    Experiencia,
    Habitacion,
    HabitacionAmenidad,
    ImagenExperiencia,
    ImagenHabitacion,
    InformacionContacto,
    SeccionAcercaDe,
    SeccionHero,
)


class ImagenHabitacionInline(TabularInline):
    model = ImagenHabitacion
    extra = 1
    fields = ["url_imagen", "vista_previa", "texto_alternativo", "es_portada", "orden_mostrar"]
    readonly_fields = ["vista_previa"]

    def vista_previa(self, obj):
        if obj and obj.url_imagen:
            return format_html(
                '<img src="{}" alt="Imagen habitación" style="max-height: 120px; max-width: 220px; object-fit: cover; border-radius: 8px;" />',
                obj.url_imagen,
            )
        return "Sin imagen"

    vista_previa.short_description = "Vista previa"
    tab = True

class HabitacionAmenidadInline(TabularInline):
    model = HabitacionAmenidad
    extra = 1
    autocomplete_fields = ["amenidad"]
    tab = True


class ImagenExperienciaInline(StackedInline):
    model = ImagenExperiencia
    extra = 1
    fields = ["url_imagen", "vista_previa", "texto_alternativo", "orden_mostrar"]
    readonly_fields = ["vista_previa"]

    def vista_previa(self, obj):
        if obj and obj.url_imagen:
            return format_html(
                '<img src="{}" alt="Imagen experiencia" style="max-height: 120px; max-width: 220px; object-fit: cover; border-radius: 8px;" />',
                obj.url_imagen,
            )
        return "Sin imagen"

    vista_previa.short_description = "Vista previa"


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(UnfoldModelAdmin):
    list_display = ["nombre_hotel", "vista_previa_logo", "idioma_predeterminado", "creado_en", "actualizado_en"]
    search_fields = ["nombre_hotel", "eslogan", "meta_titulo"]
    fieldsets = (
        ("Información general", {"fields": ("nombre_hotel", "eslogan", "idioma_predeterminado")}),
        ("Identidad visual", {"fields": ("url_logo", "vista_previa_logo", "url_favicon", "color_primario", "color_secundario", "color_acento")}),
        ("SEO", {"fields": ("meta_titulo", "meta_descripcion")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["vista_previa_logo", "creado_en", "actualizado_en"]

    def vista_previa_logo(self, obj):
        if obj and obj.url_logo:
            return format_html(
                '<img src="{}" alt="Logo" style="max-height: 80px; max-width: 200px; object-fit: contain; border-radius: 8px;" />',
                obj.url_logo,
            )
        return "Sin logo"

    vista_previa_logo.short_description = "Vista previa del logo"


@admin.register(SeccionHero)
class SeccionHeroAdmin(UnfoldModelAdmin):
    list_display = ["titulo", "vista_previa_poster", "esta_activo", "creado_en", "actualizado_en"]
    list_filter = ["esta_activo"]
    search_fields = ["titulo", "subtitulo"]
    list_editable = ["esta_activo"]
    fieldsets = (
        ("Contenido", {"fields": ("titulo", "subtitulo", "esta_activo")}),
        ("Media", {"fields": ("url_video", "url_video_movil", "url_poster", "vista_previa_poster")}),
        ("Botón primario", {"fields": ("texto_boton_primario", "url_boton_primario")}),
        ("Botón secundario", {"fields": ("texto_boton_secundario", "url_boton_secundario")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["vista_previa_poster", "creado_en", "actualizado_en"]

    def vista_previa_poster(self, obj):
        if obj and obj.url_poster:
            return format_html(
                '<img src="{}" alt="Poster hero" style="max-height: 140px; max-width: 260px; object-fit: cover; border-radius: 8px;" />',
                obj.url_poster,
            )
        return "Sin poster"

    vista_previa_poster.short_description = "Vista previa del poster"


@admin.register(SeccionAcercaDe)
class SeccionAcercaDeAdmin(UnfoldModelAdmin):
    list_display = ["titulo", "esta_activo", "creado_en", "actualizado_en"]
    list_filter = ["esta_activo"]
    search_fields = ["titulo", "subtitulo", "descripcion"]
    list_editable = ["esta_activo"]
    fieldsets = (
        ("Contenido", {"fields": ("titulo", "subtitulo", "descripcion", "historia", "mision", "vision", "esta_activo")}),
        ("Imágenes", {"fields": ("url_imagen_principal", "vista_previa_imagen_principal", "url_imagen_secundaria", "vista_previa_imagen_secundaria")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["vista_previa_imagen_principal", "vista_previa_imagen_secundaria", "creado_en", "actualizado_en"]

    def vista_previa_imagen_principal(self, obj):
        if obj and obj.url_imagen_principal:
            return format_html(
                '<img src="{}" alt="Imagen principal" style="max-height: 120px; max-width: 220px; object-fit: cover; border-radius: 8px;" />',
                obj.url_imagen_principal,
            )
        return "Sin imagen"

    vista_previa_imagen_principal.short_description = "Vista previa imagen principal"

    def vista_previa_imagen_secundaria(self, obj):
        if obj and obj.url_imagen_secundaria:
            return format_html(
                '<img src="{}" alt="Imagen secundaria" style="max-height: 120px; max-width: 220px; object-fit: cover; border-radius: 8px;" />',
                obj.url_imagen_secundaria,
            )
        return "Sin imagen"

    vista_previa_imagen_secundaria.short_description = "Vista previa imagen secundaria"


@admin.register(Amenidad)
class AmenidadAdmin(UnfoldModelAdmin):
    list_display = ["nombre", "icono", "esta_activo", "creado_en", "actualizado_en"]
    list_filter = ["esta_activo"]
    search_fields = ["nombre", "descripcion", "icono"]
    list_editable = ["esta_activo"]
    fieldsets = (
        ("Información", {"fields": ("nombre", "icono", "descripcion", "esta_activo")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["creado_en", "actualizado_en"]



@admin.register(Habitacion)
class HabitacionAdmin(UnfoldModelAdmin):
    list_display = ["nombre", "capacidad", "tipo_cama", "es_destacada", "esta_activo", "orden_mostrar", "creado_en"]
    list_filter = ["es_destacada", "esta_activo"]
    search_fields = ["nombre", "slug", "descripcion_corta", "descripcion_completa", "tipo_cama", "tipo_vista"]
    list_editable = ["es_destacada", "esta_activo", "orden_mostrar"]
    prepopulated_fields = {"slug": ("nombre",)}
    inlines = [ImagenHabitacionInline, HabitacionAmenidadInline]
    fieldsets = (
        ("Información principal", {"fields": ("nombre", "slug", "descripcion_corta", "descripcion_completa")}),
        ("Detalles", {"fields": ("capacidad", "tipo_cama", "tamano_m2", "tipo_vista", "precio_referencia")}),
        ("Publicación", {"fields": ("es_destacada", "esta_activo", "orden_mostrar")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["creado_en", "actualizado_en"]


@admin.register(ImagenHabitacion)
class ImagenHabitacionAdmin(UnfoldModelAdmin):
    list_display = ["habitacion", "vista_previa", "es_portada", "orden_mostrar", "creado_en"]
    list_filter = ["es_portada", "habitacion"]
    search_fields = ["habitacion__nombre", "texto_alternativo", "url_imagen"]
    list_editable = ["es_portada", "orden_mostrar"]
    autocomplete_fields = ["habitacion"]
    fieldsets = (
        ("Información", {"fields": ("habitacion", "url_imagen", "vista_previa", "texto_alternativo", "es_portada", "orden_mostrar")}),
        ("Fechas", {"fields": ("creado_en",)}),
    )
    readonly_fields = ["vista_previa", "creado_en"]

    def vista_previa(self, obj):
        if obj and obj.url_imagen:
            return format_html(
                '<img src="{}" alt="Imagen habitación" style="max-height: 120px; max-width: 220px; object-fit: cover; border-radius: 8px;" />',
                obj.url_imagen,
            )
        return "Sin imagen"

    vista_previa.short_description = "Vista previa"


@admin.register(HabitacionAmenidad)
class HabitacionAmenidadAdmin(UnfoldModelAdmin):
    list_display = ["habitacion", "amenidad", "creado_en"]
    list_filter = ["amenidad"]
    search_fields = ["habitacion__nombre", "amenidad__nombre"]
    autocomplete_fields = ["habitacion", "amenidad"]
    fieldsets = (
        ("Relación", {"fields": ("habitacion", "amenidad")}),
        ("Fechas", {"fields": ("creado_en",)}),
    )
    readonly_fields = ["creado_en"]


@admin.register(Experiencia)
class ExperienciaAdmin(UnfoldModelAdmin):
    list_display = ["titulo", "nombre_huesped", "fuente", "calificacion", "es_destacada", "esta_activo", "orden_mostrar", "creado_en"]
    list_filter = ["fuente", "es_destacada", "esta_activo"]
    search_fields = ["titulo", "nombre_huesped", "ubicacion_huesped", "comentario", "etiqueta_fuente"]
    list_editable = ["es_destacada", "esta_activo", "orden_mostrar"]
    inlines = [ImagenExperienciaInline]
    fieldsets = (
        ("Contenido", {"fields": ("titulo", "comentario", "nombre_huesped", "ubicacion_huesped")}),
        ("Fuente", {"fields": ("fuente", "etiqueta_fuente", "url_fuente", "calificacion", "fecha_experiencia")}),
        ("Publicación", {"fields": ("es_destacada", "esta_activo", "orden_mostrar")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["creado_en", "actualizado_en"]


@admin.register(ImagenExperiencia)
class ImagenExperienciaAdmin(UnfoldModelAdmin):
    list_display = ["experiencia", "vista_previa", "orden_mostrar", "creado_en"]
    list_filter = ["experiencia"]
    search_fields = ["experiencia__titulo", "experiencia__nombre_huesped", "texto_alternativo", "url_imagen"]
    list_editable = ["orden_mostrar"]
    autocomplete_fields = ["experiencia"]
    fieldsets = (
        ("Información", {"fields": ("experiencia", "url_imagen", "vista_previa", "texto_alternativo", "orden_mostrar")}),
        ("Fechas", {"fields": ("creado_en",)}),
    )
    readonly_fields = ["vista_previa", "creado_en"]

    def vista_previa(self, obj):
        if obj and obj.url_imagen:
            return format_html(
                '<img src="{}" alt="Imagen experiencia" style="max-height: 120px; max-width: 220px; object-fit: cover; border-radius: 8px;" />',
                obj.url_imagen,
            )
        return "Sin imagen"

    vista_previa.short_description = "Vista previa"


@admin.register(EnlaceReserva)
class EnlaceReservaAdmin(UnfoldModelAdmin):
    list_display = ["nombre_plataforma", "tipo_plataforma", "es_principal", "esta_activo", "orden_mostrar", "creado_en"]
    list_filter = ["tipo_plataforma", "es_principal", "esta_activo"]
    search_fields = ["nombre_plataforma", "descripcion", "texto_boton", "url"]
    list_editable = ["es_principal", "esta_activo", "orden_mostrar"]
    fieldsets = (
        ("Información", {"fields": ("nombre_plataforma", "tipo_plataforma", "url", "url_icono")}),
        ("Contenido", {"fields": ("descripcion", "texto_boton")}),
        ("Publicación", {"fields": ("es_principal", "esta_activo", "orden_mostrar")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["creado_en", "actualizado_en"]


@admin.register(InformacionContacto)
class InformacionContactoAdmin(UnfoldModelAdmin):
    list_display = ["correo_electronico", "telefono", "whatsapp", "ciudad", "pais", "creado_en", "actualizado_en"]
    search_fields = ["direccion", "barrio", "ciudad", "pais", "telefono", "whatsapp", "correo_electronico"]
    fieldsets = (
        ("Ubicación", {"fields": ("direccion", "barrio", "ciudad", "estado_region", "pais", "codigo_postal", "latitud", "longitud", "url_google_maps")}),
        ("Contacto", {"fields": ("telefono", "whatsapp", "correo_electronico")}),
        ("Horarios", {"fields": ("hora_check_in", "hora_check_out")}),
        ("Redes sociales", {"fields": ("url_facebook", "url_instagram", "url_youtube", "url_tiktok", "url_x")}),
        ("Fechas", {"fields": ("creado_en", "actualizado_en")}),
    )
    readonly_fields = ["creado_en", "actualizado_en"]