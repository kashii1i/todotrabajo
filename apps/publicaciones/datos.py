"""Categorías iniciales: (nombre, slug, [(subcategoría, slug), ...])."""

CATEGORIAS = [
    ("Hogar y reparaciones", "hogar", [
        ("Gasfitería", "gasfiteria"), ("Electricidad", "electricidad"),
        ("Carpintería", "carpinteria"), ("Pintura", "pintura"),
        ("Cerrajería", "cerrajeria"), ("Construcción y albañilería", "construccion"),
    ]),
    ("Limpieza", "limpieza", [
        ("Limpieza de hogar", "limpieza-hogar"), ("Limpieza de oficinas", "limpieza-oficinas"),
        ("Limpieza post obra", "limpieza-post-obra"),
    ]),
    ("Jardinería", "jardineria", []),
    ("Mudanzas y fletes", "mudanzas-fletes", []),
    ("Tecnología", "tecnologia", [
        ("Reparación de computadores", "reparacion-computadores"),
        ("Desarrollo web y apps", "desarrollo-web"), ("Soporte técnico", "soporte-tecnico"),
    ]),
    ("Clases particulares", "clases", [
        ("Matemáticas y ciencias", "clases-matematicas"), ("Idiomas", "clases-idiomas"),
        ("Música", "clases-musica"),
    ]),
    ("Belleza y bienestar", "belleza", [
        ("Peluquería", "peluqueria"), ("Manicure y pedicure", "manicure"),
        ("Masajes", "masajes"),
    ]),
    ("Cuidado de personas", "cuidado", [
        ("Cuidado de niños", "cuidado-ninos"), ("Cuidado de adultos mayores", "cuidado-adultos-mayores"),
    ]),
    ("Mascotas", "mascotas", [
        ("Paseo de perros", "paseo-perros"), ("Peluquería canina", "peluqueria-canina"),
    ]),
    ("Eventos", "eventos", [
        ("Fotografía y video", "fotografia"), ("Banquetería", "banqueteria"),
        ("Música y DJ", "dj"),
    ]),
    ("Mecánica automotriz", "mecanica", []),
    ("Diseño y marketing", "diseno-marketing", []),
    ("Otros", "otros", []),
]
