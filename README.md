# Centro de Control SOStenible

Tablero de seguimiento de los proyectos de Promotora Proyectos SOStenibles.
Lee las tareas desde ClickUp (lista **Seguimiento SOStenible**) y las muestra como
mapa de proyectos + tablero kanban.

- `index.html` — el tablero (lee `data.json`).
- `data.json` — foto de las tareas de ClickUp.
- `generate.py` — regenera `data.json` leyendo la API de ClickUp.
- `.github/workflows/refresh.yml` — cada 6 h actualiza `data.json` solo.

## Para que se actualice solo (un paso manual)

La GitHub Action necesita un token de ClickUp para leer tus tareas.

1. En ClickUp: foto de perfil (abajo izq.) → **Settings** → **Apps** → **API Token** → **Generate** / **Copy**.
2. En este repo de GitHub: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
3. Name: `CLICKUP_TOKEN` · Secret: pega el token → **Add secret**.

Listo. La Action corre cada 6 horas (o a mano en la pestaña **Actions → Run workflow**).

El tablero queda publicado por **GitHub Pages** y se puede apuntar a
`seguimiento.sostenible.me` con un registro CNAME.
