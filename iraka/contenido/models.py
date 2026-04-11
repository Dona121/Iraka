from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField


class ModeloConFechas(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    actualizado_en = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    class Meta:
        abstract = True


class ConfiguracionSitio(ModeloConFechas):
    nombre_hotel = models.CharField(max_length=150, verbose_name="Nombre del hotel")
    eslogan = models.CharField(max_length=255, blank=True, verbose_name="Eslogan")
    url_logo = models.URLField(blank=True, verbose_name="URL del logo")
    url_favicon = models.URLField(blank=True, verbose_name="URL del favicon")
    color_primario = models.CharField(max_length=20, blank=True, verbose_name="Color primario")
    color_secundario = models.CharField(max_length=20, blank=True, verbose_name="Color secundario")
    color_acento = models.CharField(max_length=20, blank=True, verbose_name="Color de acento")
    idioma_predeterminado = models.CharField(max_length=10, default="es", verbose_name="Idioma predeterminado")
    meta_titulo = models.CharField(max_length=255, blank=True, verbose_name="Meta título")
    meta_descripcion = models.TextField(blank=True, verbose_name="Meta descripción")

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuraciones del sitio"

    def __str__(self):
        return self.nombre_hotel


class SeccionHero(ModeloConFechas):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    subtitulo = models.TextField(blank=True, verbose_name="Subtítulo")
    url_video = models.URLField(blank=True, verbose_name="URL del video")
    url_video_movil = models.URLField(blank=True, verbose_name="URL del video móvil")
    url_poster = models.URLField(blank=True, verbose_name="URL del poster")
    texto_boton_primario = models.CharField(max_length=100, blank=True, verbose_name="Texto del botón primario")
    url_boton_primario = models.CharField(max_length=255, blank=True, verbose_name="URL del botón primario")
    texto_boton_secundario = models.CharField(max_length=100, blank=True, verbose_name="Texto del botón secundario")
    url_boton_secundario = models.CharField(max_length=255, blank=True, verbose_name="URL del botón secundario")
    esta_activo = models.BooleanField(default=True, verbose_name="Está activo")

    class Meta:
        verbose_name = "Sección hero"
        verbose_name_plural = "Secciones hero"

    def __str__(self):
        return self.titulo


class SeccionAcercaDe(ModeloConFechas):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    subtitulo = models.CharField(max_length=255, blank=True, verbose_name="Subtítulo")
    descripcion = models.TextField(verbose_name="Descripción")
    historia = models.TextField(blank=True, verbose_name="Historia")
    mision = models.TextField(blank=True, verbose_name="Misión")
    vision = models.TextField(blank=True, verbose_name="Visión")
    url_imagen_principal = models.URLField(blank=True, verbose_name="URL de la imagen principal")
    url_imagen_secundaria = models.URLField(blank=True, verbose_name="URL de la imagen secundaria")
    esta_activo = models.BooleanField(default=True, verbose_name="Está activo")

    class Meta:
        verbose_name = "Sección acerca de"
        verbose_name_plural = "Secciones acerca de"

    def __str__(self):
        return self.titulo


class Amenidad(ModeloConFechas):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    icono = models.CharField(max_length=100, blank=True, verbose_name="Ícono")
    descripcion = models.CharField(max_length=255, blank=True, verbose_name="Descripción")
    esta_activo = models.BooleanField(default=True, verbose_name="Está activo")

    class Meta:
        verbose_name = "Amenidad"
        verbose_name_plural = "Amenidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Habitacion(ModeloConFechas):
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    slug = models.SlugField(max_length=180, unique=True, verbose_name="Slug")
    descripcion_corta = models.TextField(blank=True, verbose_name="Descripción corta")
    descripcion_completa = models.TextField(blank=True, verbose_name="Descripción completa")
    capacidad = models.PositiveIntegerField(null=True, blank=True, verbose_name="Capacidad")
    tipo_cama = models.CharField(max_length=100, blank=True, verbose_name="Tipo de cama")
    tamano_m2 = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Tamaño en m²")
    tipo_vista = models.CharField(max_length=100, blank=True, verbose_name="Tipo de vista")
    precio_referencia = MoneyField(max_digits=10, decimal_places=2,default_currency="COL" ,null=True, blank=True, verbose_name="Precio de referencia")
    es_destacada = models.BooleanField(default=False, verbose_name="Es destacada")
    esta_activo = models.BooleanField(default=True, verbose_name="Está activo")
    orden_mostrar = models.IntegerField(default=0, verbose_name="Orden de visualización")
    amenidades = models.ManyToManyField(Amenidad, through="HabitacionAmenidad", related_name="habitaciones", blank=True, verbose_name="Amenidades")

    class Meta:
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
        ordering = ["orden_mostrar", "nombre"]

    def __str__(self):
        return self.nombre
    
    @property
    def imagen_portada(self):
        return self.imagenes.filter(es_portada=True).order_by("orden_mostrar", "id").first() or self.imagenes.order_by("orden_mostrar", "id").first()


class ImagenHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, related_name="imagenes", verbose_name="Habitación")
    url_imagen = models.URLField(verbose_name="URL de la imagen")
    texto_alternativo = models.CharField(max_length=255, blank=True, verbose_name="Texto alternativo")
    es_portada = models.BooleanField(default=False, verbose_name="Es portada")
    orden_mostrar = models.IntegerField(default=0, verbose_name="Orden de visualización")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    class Meta:
        verbose_name = "Imagen de habitación"
        verbose_name_plural = "Imágenes de habitaciones"
        ordering = ["orden_mostrar", "id"]

    def __str__(self):
        return f"Imagen de {self.habitacion.nombre}"


class HabitacionAmenidad(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE, verbose_name="Habitación")
    amenidad = models.ForeignKey(Amenidad, on_delete=models.CASCADE, verbose_name="Amenidad")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    class Meta:
        verbose_name = "Amenidad de habitación"
        verbose_name_plural = "Amenidades de habitaciones"
        constraints = [models.UniqueConstraint(fields=["habitacion", "amenidad"], name="unica_habitacion_amenidad")]

    def __str__(self):
        return f"{self.habitacion.nombre} - {self.amenidad.nombre}"


class Experiencia(ModeloConFechas):
    class OpcionesFuente(models.TextChoices):
        INSTAGRAM = "instagram", "Instagram"
        FACEBOOK = "facebook", "Facebook"
        GOOGLE = "google", "Google"
        BOOKING = "booking", "Booking"
        AIRBNB = "airbnb", "Airbnb"
        TRIPADVISOR = "tripadvisor", "Tripadvisor"
        DIRECTO = "direct", "Directo"
        OTRO = "other", "Otro"

    nombre_huesped = models.CharField(max_length=150, blank=True, verbose_name="Nombre del huésped")
    ubicacion_huesped = models.CharField(max_length=150, blank=True, verbose_name="Ubicación del huésped")
    fuente = models.CharField(max_length=20, choices=OpcionesFuente.choices, default=OpcionesFuente.DIRECTO, verbose_name="Fuente")
    etiqueta_fuente = models.CharField(max_length=100, blank=True, verbose_name="Etiqueta de la fuente")
    url_fuente = models.URLField(blank=True, verbose_name="URL de la fuente")
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Calificación")
    titulo = models.CharField(max_length=255, blank=True, verbose_name="Título")
    comentario = models.TextField(verbose_name="Comentario")
    fecha_experiencia = models.DateField(null=True, blank=True, verbose_name="Fecha de la experiencia")
    es_destacada = models.BooleanField(default=False, verbose_name="Es destacada")
    esta_activo = models.BooleanField(default=True, verbose_name="Está activo")
    orden_mostrar = models.IntegerField(default=0, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Experiencias"
        ordering = ["orden_mostrar", "-creado_en"]

    def __str__(self):
        return self.titulo or self.nombre_huesped or "Experiencia"


class ImagenExperiencia(models.Model):
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name="imagenes", verbose_name="Experiencia")
    url_imagen = models.URLField(verbose_name="URL de la imagen")
    texto_alternativo = models.CharField(max_length=255, blank=True, verbose_name="Texto alternativo")
    orden_mostrar = models.IntegerField(default=0, verbose_name="Orden de visualización")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    class Meta:
        verbose_name = "Imagen de experiencia"
        verbose_name_plural = "Imágenes de experiencias"
        ordering = ["orden_mostrar", "id"]

    def __str__(self):
        return f"Imagen de experiencia #{self.experiencia_id}"


class EnlaceReserva(ModeloConFechas):
    class OpcionesTipoPlataforma(models.TextChoices):
        BOOKING = "booking", "Booking"
        AIRBNB = "airbnb", "Airbnb"
        EXPEDIA = "expedia", "Expedia"
        TRIPADVISOR = "tripadvisor", "Tripadvisor"
        WHATSAPP = "whatsapp", "WhatsApp"
        TELEFONO = "phone", "Teléfono"
        CORREO = "email", "Correo"
        SITIO_WEB = "website", "Sitio web"
        OTRO = "other", "Otro"

    nombre_plataforma = models.CharField(max_length=100, verbose_name="Nombre de la plataforma")
    tipo_plataforma = models.CharField(max_length=20, choices=OpcionesTipoPlataforma.choices, default=OpcionesTipoPlataforma.OTRO, verbose_name="Tipo de plataforma")
    url = models.URLField(verbose_name="URL")
    url_icono = models.URLField(blank=True, verbose_name="URL del ícono")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    texto_boton = models.CharField(max_length=100, blank=True, verbose_name="Texto del botón")
    es_principal = models.BooleanField(default=False, verbose_name="Es principal")
    esta_activo = models.BooleanField(default=True, verbose_name="Está activo")
    orden_mostrar = models.IntegerField(default=0, verbose_name="Orden de visualización")

    class Meta:
        verbose_name = "Enlace de reserva"
        verbose_name_plural = "Enlaces de reserva"
        ordering = ["orden_mostrar", "nombre_plataforma"]

    def __str__(self):
        return self.nombre_plataforma


class InformacionContacto(ModeloConFechas):
    direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección")
    barrio = models.CharField(max_length=150, blank=True, verbose_name="Barrio")
    ciudad = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")
    estado_region = models.CharField(max_length=100, blank=True, verbose_name="Estado o región")
    pais = models.CharField(max_length=100, blank=True, verbose_name="País")
    codigo_postal = models.CharField(max_length=20, blank=True, verbose_name="Código postal")
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name="Latitud")
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name="Longitud")
    telefono = models.CharField(max_length=50, blank=True, verbose_name="Teléfono")
    whatsapp = models.CharField(max_length=50, blank=True, verbose_name="WhatsApp")
    correo_electronico = models.EmailField(blank=True, verbose_name="Correo electrónico")
    url_google_maps = models.URLField(blank=True, verbose_name="URL de Google Maps")
    hora_check_in = models.TimeField(null=True, blank=True, verbose_name="Hora de check-in")
    hora_check_out = models.TimeField(null=True, blank=True, verbose_name="Hora de check-out")
    url_facebook = models.URLField(blank=True, verbose_name="URL de Facebook")
    url_instagram = models.URLField(blank=True, verbose_name="URL de Instagram")
    url_youtube = models.URLField(blank=True, verbose_name="URL de YouTube")
    url_tiktok = models.URLField(blank=True, verbose_name="URL de TikTok")
    url_x = models.URLField(blank=True, verbose_name="URL de X")

    class Meta:
        verbose_name = "Información de contacto"
        verbose_name_plural = "Información de contacto"

    def __str__(self):
        return self.correo_electronico or self.telefono or "Información de contacto"