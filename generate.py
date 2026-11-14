#!/usr/bin/env python3
"""Regenera data.json leyendo la lista 'Seguimiento SOStenible' de ClickUp.
Lee el token y el list_id de variables de entorno:
  CLICKUP_TOKEN   (secreto del repo)
  CLICKUP_LIST_ID (por defecto la lista creada)
No contiene ningun secreto en el codigo.
"""
import os, json, datetime, urllib.request, urllib.error

TOKEN = os.environ["CLICKUP_TOKEN"]
LIST_ID = os.environ.get("CLICKUP_LIST_ID", "1600620000000490")
API = "https://api.clickup.com/api/v2"

META = {
 "promotora": ("Promotora Proyectos SOStenibles", "\U0001F310", "#1f8a4c"),
 "salud": ("Salud", "\U0001F4AA", "#e0557a"),
 "casa-aurora": ("Casa Aurora", "\U0001F3E1", "#c9890b"),
 "colombia-sostenible": ("Colombia SOStenible", "\U0001F1E8\U0001F1F4", "#2f6fb0"),
 "box": ("bOx", "\U0001F4E6", "#7a4fd0"),
 "edificio": ("Edificio Multifamiliar Casa Aurora", "\U0001F3E2", "#0f9d9f"),
}
ORDER = ["promotora", "salud", "casa-aurora", "colombia-sostenible", "box", "edificio"]
COL = {"to do": "porhacer", "planning": "porhacer", "in progress": "proceso",
       "at risk": "proceso", "update required": "proceso", "on hold": "proceso",
       "complete": "listo", "cancelled": "listo"}


def api_get(path):
    req = urllib.request.Request(API + path, headers={"Authorization": TOKEN})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_tasks():
    tasks, page = [], 0
    while True:
        data = api_get(f"/list/{LIST_ID}/task?include_closed=true&subtasks=true&page={page}")
        batch = data.get("tasks", [])
        tasks += batch
        if data.get("last_page") or not batch:
            break
        page += 1
    return tasks


def main():
    tasks = fetch_tasks()
    buckets = {s: [] for s in ORDER}
    for t in tasks:
        tags = [tg["name"] for tg in t.get("tags", [])]
        slug = next((s for s in ORDER if s in tags), None)
        if not slug:
            continue
        status = (t.get("status", {}) or {}).get("status", "to do")
        url = (t.get("text_content") or t.get("description") or "").strip()
        name = t["name"]
        home = name.endswith("sitio principal")
        buckets[slug].append({
            "name": "Sitio principal" if home else name,
            "status": status,
            "col": COL.get(status, "porhacer"),
            "url": url,
            "clickup": t.get("url", "https://app.clickup.com/t/" + t["id"]),
            "home": home,
        })

    frentes = []
    for slug in ORDER:
        nombre, emoji, color = META[slug]
        items = sorted(buckets[slug], key=lambda x: (not x["home"], x["name"]))
        home_url = next((i["url"] for i in items if i["home"]), "")
        frentes.append({"slug": slug, "nombre": nombre, "emoji": emoji,
                        "color": color, "home_url": home_url, "items": items})

    data = {
        "generated": datetime.date.today().isoformat(),
        "source": "ClickUp · Lista Seguimiento SOStenible",
        "list_url": f"https://app.clickup.com/3118654/v/l/li/{LIST_ID}",
        "frentes": frentes,
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    on = sum(1 for fr in frentes for i in fr["items"] if i["status"] == "complete")
    tot = sum(len(fr["items"]) for fr in frentes)
    print(f"data.json actualizado: {tot} modulos, {on} en linea")


if __name__ == "__main__":
    main()
