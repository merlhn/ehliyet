#!/usr/bin/env python3
"""
ehliyet.digital MCP Server

Ehliyet sinavi (Turkiye surucu belgesi) hazirlik verilerini
AI ajanlarina sunan Model Context Protocol sunucusu.
"""
import json
import random
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

DATA_DIR = Path(__file__).resolve().parent / "data"

# ---------------------------------------------------------------------------
# Veri yukleme
# ---------------------------------------------------------------------------

def load_json(name: str) -> Any:
    path = DATA_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))

questions: list[dict] = load_json("questions.json")
quick_facts: list[dict] = load_json("quick-facts.json")
lesson_summaries: list[dict] = load_json("lesson-summaries.json")

question_index: dict[str, dict] = {q["id"]: q for q in questions}

# ---------------------------------------------------------------------------
# Bolum eslestirme
# ---------------------------------------------------------------------------

SECTION_MAP = {
    "ilk_yardim": "İlk Yardım",
    "trafik_ve_cevre": "Trafik ve Çevre",
    "arac_teknigi": "Araç Tekniği",
    "trafik_adabi": "Trafik Adabı",
    "all": None,
}

SECTION_ENUM = list(SECTION_MAP.keys())

def resolve_section(key: str) -> str | None:
    return SECTION_MAP.get(key)

def filter_by_section(items: list[dict], section_key: str, field: str = "section") -> list[dict]:
    section = resolve_section(section_key)
    if section is None:
        return items
    return [item for item in items if item[field] == section]

# ---------------------------------------------------------------------------
# Yardimci fonksiyonlar
# ---------------------------------------------------------------------------

def format_question(q: dict, num: int | None = None) -> str:
    prefix = f"Soru {num}. " if num else ""
    lines = [
        f"{prefix}[{q['id']}] ({q['exam']} / {q['section']})",
        "",
        q["stem"],
        "",
    ]
    for opt in q["options"]:
        lines.append(f"  {opt}")
    lines.append("")
    lines.append(f"Dogru cevap: {q['correct_letter']}) {q['correct_text']}")
    if q["has_image"]:
        lines.append("(Bu soruda gorsel/video vardir; metin aciklamasi soru icinde verilmistir.)")
    return "\n".join(lines)


def handle_practice_questions(args: dict) -> str:
    section = args.get("section", "all")
    count = min(args.get("count", 5), 50)
    pool = filter_by_section(questions, section)
    if not pool:
        return f"'{section}' bolumu icin soru bulunamadi."
    selected = random.sample(pool, min(count, len(pool)))
    parts = [f"# Pratik Sorular ({len(selected)} soru)\n"]
    for i, q in enumerate(selected, 1):
        parts.append(format_question(q, i))
        parts.append("---")
    return "\n".join(parts)


def handle_quick_facts(args: dict) -> str:
    section = args.get("section", "all")
    facts = filter_by_section(quick_facts, section)
    if not facts:
        return f"'{section}' bolumu icin hap bilgi bulunamadi."
    parts = [f"# Hap Bilgiler ({len(facts)} bilgi)\n"]
    current_section = ""
    for i, f in enumerate(facts, 1):
        if f["section"] != current_section:
            current_section = f["section"]
            parts.append(f"\n## {current_section}\n")
        parts.append(f"{i}. {f['fact']}")
    return "\n".join(parts)


def handle_mock_exam(args: dict) -> str:
    distribution = {
        "İlk Yardım": 12,
        "Trafik ve Çevre": 23,
        "Araç Tekniği": 9,
        "Trafik Adabı": 6,
    }
    exam_questions = []
    for section_name, count in distribution.items():
        pool = [q for q in questions if q["section"] == section_name]
        selected = random.sample(pool, min(count, len(pool)))
        exam_questions.extend(selected)
    random.shuffle(exam_questions)

    parts = [
        "# Deneme Sinavi (50 soru)",
        "Dagitim: 12 Ilk Yardim, 23 Trafik ve Cevre, 9 Arac Teknigi, 6 Trafik Adabi",
        "Gecme baraj: 70 puan (her soru 2 puan, en az 35 dogru)",
        "",
    ]
    for i, q in enumerate(exam_questions, 1):
        parts.append(format_question(q, i))
        parts.append("---")
    parts.append("\n# Cevap Anahtari\n")
    for i, q in enumerate(exam_questions, 1):
        parts.append(f"{i:2d}. {q['correct_letter']}  ({q['id']})")
    return "\n".join(parts)


def handle_lesson_summary(args: dict) -> str:
    section = args.get("section", "all")
    topic = args.get("topic", "").lower().strip()
    pool = filter_by_section(lesson_summaries, section)
    if topic:
        pool = [
            ls for ls in pool
            if topic in ls["lesson"].lower() or topic in ls["url"].lower()
        ]
    if not pool:
        return f"Eslesen ders bulunamadi (bolum={section}, konu={topic})."
    parts = [f"# Ders Ozetleri ({len(pool)} ders)\n"]
    for ls in pool:
        parts.append(f"## {ls['lesson']} ({ls['section']})")
        parts.append(f"URL: https://ehliyet.digital{ls['url']}\n")
        for j, fact in enumerate(ls["facts"], 1):
            parts.append(f"  {j}. {fact}")
        parts.append("")
    return "\n".join(parts)


def handle_explain_answer(args: dict) -> str:
    qid = args.get("question_id", "").strip()
    q = question_index.get(qid)
    if not q:
        return f"'{qid}' ID'li soru bulunamadi. Ornek format: sinav1-q01"

    related_facts = [f["fact"] for f in quick_facts if f["section"] == q["section"]]
    related_lessons = [ls for ls in lesson_summaries if ls["section"] == q["section"]]

    stem_words = set(q["stem"].lower().split())
    scored_facts = []
    for fact in related_facts:
        overlap = len(stem_words & set(fact.lower().split()))
        if overlap >= 3:
            scored_facts.append((overlap, fact))
    scored_facts.sort(reverse=True)
    top_facts = [f for _, f in scored_facts[:3]]

    scored_lessons = []
    for ls in related_lessons:
        all_text = " ".join(ls["facts"]).lower()
        overlap = len(stem_words & set(all_text.split()))
        if overlap >= 3:
            scored_lessons.append((overlap, ls))
    scored_lessons.sort(reverse=True)
    top_lessons = [ls for _, ls in scored_lessons[:2]]

    parts = [
        f"# Soru Aciklamasi: {qid}",
        f"Sinav: {q['exam']} | Bolum: {q['section']}",
        "",
        "## Soru",
        q["stem"],
        "",
    ]
    for opt in q["options"]:
        marker = " <<< DOGRU" if opt.startswith(q["correct_letter"] + ")") else ""
        parts.append(f"  {opt}{marker}")
    parts.append(f"\n## Dogru Cevap: {q['correct_letter']}) {q['correct_text']}")
    if top_facts:
        parts.append("\n## Ilgili Hap Bilgiler")
        for fact in top_facts:
            parts.append(f"  - {fact}")
    if top_lessons:
        parts.append("\n## Ilgili Dersler")
        for ls in top_lessons:
            parts.append(f"  - {ls['lesson']}: https://ehliyet.digital{ls['url']}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Arac tanimlari
# ---------------------------------------------------------------------------

TOOLS = [
    types.Tool(
        name="get_practice_questions",
        description=(
            "Belirtilen bolumden rastgele ehliyet sinav sorulari dondurur. "
            "Her soru: soru metni, 4 secenegi, dogru cevabi ve soru kimligini icerir. "
            "Turkiye B sinifi surucu belgesi (ehliyet) sinavina hazirlik icin kullanilir."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "enum": SECTION_ENUM,
                    "description": (
                        "Soru bolumu: ilk_yardim, trafik_ve_cevre, arac_teknigi, "
                        "trafik_adabi veya all (tum bolumler)"
                    ),
                },
                "count": {
                    "type": "integer",
                    "description": "Dondurulecek soru sayisi (varsayilan: 5, maks: 50)",
                    "default": 5,
                },
            },
            "required": ["section"],
        },
    ),
    types.Tool(
        name="get_quick_facts",
        description=(
            "Belirtilen bolum icin hap bilgileri (kisa ozetler) dondurur. "
            "Bunlar sinavda en cok sorulan bilgilerin ozetleridir. "
            "Hizli tekrar ve son dakika calismasi icin idealdir."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "enum": SECTION_ENUM,
                    "description": (
                        "Bolum: ilk_yardim, trafik_ve_cevre, arac_teknigi, "
                        "trafik_adabi veya all"
                    ),
                },
            },
            "required": ["section"],
        },
    ),
    types.Tool(
        name="generate_mock_exam",
        description=(
            "50 soruluk tam bir deneme sinavi olusturur. "
            "Dagitim gercek MTSK sinaviyla aynidir: "
            "12 Ilk Yardim, 23 Trafik ve Cevre, 9 Arac Teknigi, 6 Trafik Adabi. "
            "Sorular rastgele secilir."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    types.Tool(
        name="get_lesson_summary",
        description=(
            "Belirli bir ders icin atomik bilgileri (sinavlik ozetler) dondurur. "
            "Her ders, konunun sinavda cikmasi muhtemel bilgilerini madde madde icerir. "
            "Konu parametresi ders adinin parcasi olabilir (ornegin 'kanamalar')."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "enum": SECTION_ENUM,
                    "description": "Bolum: ilk_yardim, trafik_ve_cevre, arac_teknigi, trafik_adabi veya all",
                },
                "topic": {
                    "type": "string",
                    "description": (
                        "Ders konusu (kismi eslesme desteklenir). "
                        "Ornek: 'kanamalar', 'hiz', 'fren', 'tasima'"
                    ),
                    "default": "",
                },
            },
            "required": ["section"],
        },
    ),
    types.Tool(
        name="explain_answer",
        description=(
            "Belirtilen soru ID'si icin dogru cevabi ve aciklamayi dondurur. "
            "Soru ID formati: sinav1-q01, sinav2-q15 vb."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "question_id": {
                    "type": "string",
                    "description": "Soru kimligi (ornek: sinav1-q01, sinav3-q42)",
                },
            },
            "required": ["question_id"],
        },
    ),
]

TOOL_HANDLERS = {
    "get_practice_questions": handle_practice_questions,
    "get_quick_facts": handle_quick_facts,
    "generate_mock_exam": handle_mock_exam,
    "get_lesson_summary": handle_lesson_summary,
    "explain_answer": handle_explain_answer,
}


# ---------------------------------------------------------------------------
# MCP handler fonksiyonlari
# ---------------------------------------------------------------------------

async def on_list_tools(ctx, params) -> types.ListToolsResult:
    return types.ListToolsResult(tools=TOOLS)


async def on_call_tool(ctx, params: types.CallToolRequestParams) -> types.CallToolResult:
    handler = TOOL_HANDLERS.get(params.name)
    if handler is None:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Bilinmeyen arac: {params.name}")],
            isError=True,
        )
    arguments = params.arguments or {}
    result = handler(arguments)
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=result)]
    )


# ---------------------------------------------------------------------------
# Server olustur ve calistir
# ---------------------------------------------------------------------------

app = Server(
    "ehliyet-digital",
    version="1.0.0",
    instructions=(
        "Turkiye B sinifi surucu belgesi (ehliyet) sinavina hazirlik MCP sunucusu. "
        "200 soru, 76 hap bilgi ve 43 ders ozeti icerir. "
        "Sorular 4 bolume ayrilir: Ilk Yardim, Trafik ve Cevre, Arac Teknigi, Trafik Adabi."
    ),
    on_list_tools=on_list_tools,
    on_call_tool=on_call_tool,
)


async def main_stdio():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


async def main_http(host="0.0.0.0", port=8080):
    """HTTP/SSE transport — remote agent'lar icin."""
    try:
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route, Mount
        import uvicorn

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await app.run(streams[0], streams[1], app.create_initialization_options())

        starlette_app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ]
        )
        config = uvicorn.Config(starlette_app, host=host, port=port)
        server = uvicorn.Server(config)
        print(f"MCP SSE sunucusu baslatildi: http://{host}:{port}/sse")
        await server.serve()
    except ImportError:
        print("HTTP transport icin ek bagimliliklar gerekli:")
        print("  pip install 'mcp[sse]' starlette uvicorn")
        raise


if __name__ == "__main__":
    import asyncio
    import os
    import sys
    if "--http" in sys.argv:
        port = int(os.environ.get("PORT", "8080"))
        for i, arg in enumerate(sys.argv):
            if arg == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
        asyncio.run(main_http(port=port))
    else:
        asyncio.run(main_stdio())
