# Coffee Lab — Contexto del Proyecto

## Qué es
App web local personal para gestionar una colección de cafés de especialidad.
Construida con Python/Flask + SQLite + HTML/CSS. Tema oscuro café.

## Cómo correrla
```bash
cd ~/Proyectos/experimentos/mi-primer-proyecto/coffee-lab
python3 app.py
# → http://localhost:5000
```
También hay un acceso directo en el Desktop: **Coffee Lab.app** (doble clic).

## Stack
- **Backend:** Python 3 + Flask
- **Base de datos:** SQLite (`coffeelab.db` — se crea automático, no está en el repo)
- **Frontend:** HTML/CSS/JS vanilla (sin frameworks)
- **Tema:** Dark warm coffee (#0f0c09 base, #c87540 accent)

## Estructura de archivos
```
coffee-lab/
├── app.py                  ← servidor Flask + todas las rutas CRUD
├── seed.py                 ← carga datos del coffee_project_context.md a la DB
├── coffee_project_context.md  ← documento maestro de cafés, recetas y equipo
├── .gitignore
├── static/
│   ├── style.css           ← tema completo: sidebar, cards, badges, tabla
│   └── script.js           ← toggle formulario agregar/cancelar
└── templates/
    ├── base.html           ← sidebar nav + flash messages
    ├── cafes.html          ← colección de cafés (cards)
    ├── recetas.html        ← recetas con parámetros
    ├── equipo.html         ← inventario brewers/grinders
    ├── sesiones.html       ← log de preparaciones (tabla)
    ├── learning.html       ← 10 recursos curados con links externos
    ├── edit_cafe.html
    ├── edit_receta.html
    ├── edit_equipo.html
    └── edit_sesion.html
```

## Base de datos — tablas
| Tabla | Campos clave |
|---|---|
| `cafes` | nombre, roaster, pais_origen, proceso, perfil_taza, fecha_compra, estado (en_stock/terminado), puntuacion |
| `recetas` | cafe_id (FK), metodo, dosis_cafe, agua_ml, temperatura, tiempo_total, notas |
| `equipo` | nombre, marca, tipo (brewer/grinder/otro), fecha_adquisicion, notas |
| `sesiones` | cafe_id (FK), metodo, fecha, notas, puntuacion |

## Datos cargados (via seed.py)
- **34 cafés** — abiertos, por abrir y terminados con proceso, país y puntuación
- **11 equipos** — V60 Mugen, Chemex, UFO, Aeropress, Epeios Essence, etc.
- **5 recetas** — Elida ASD maestra ★5, Ayla Bombe, Sadayana + 2 plantillas
- **32 sesiones** — recipe log completo mayo–junio 2026

Para re-cargar la DB desde cero:
```bash
python3 seed.py
```

## Métodos disponibles en formularios
V60 · Switch · Chemex · AeroPress · UFO-V2

## Repos en GitHub
- `mi-primer-proyecto` → https://github.com/dianixlt/mi-primer-proyecto (hola.py + dashboard ventas retail)
- `coffee_lab` → https://github.com/dianixlt/coffee_lab (esta app)

## Pendiente
- [ ] **Deployment:** hostear la app para acceso desde cualquier lugar
  - Opciones evaluadas: Railway (recomendado), PythonAnywhere (gratis), Fly.io
  - Blocker: SQLite necesita volumen persistente o migrar a PostgreSQL
  - Necesita: `requirements.txt`, `Procfile` (Gunicorn), ajustar ruta DB a relativa
- [ ] Agregar campo "método de brew" a la sección de cafés para ver qué método va mejor con cada café
- [ ] Sección de learning: verificar URLs de Onyx Coffee Lab y Scott Rao (pueden haber cambiado)

## SSH configurada
Llave SSH activa para GitHub: `SHA256:EMOFi0nyx/E81hD2mxIPLEjvprkGCBMpQb8J4siunMs`
Remote configurado como SSH en ambos repos.
