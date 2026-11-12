from __future__ import annotations
import inspect
from functools import lru_cache
import pandas as pd
import streamlit as st
import config as C

@lru_cache(maxsize=None)
def _aceita(func_name: str, param: str) -> bool:
    fn = getattr(st, func_name, None)
    if fn is None: return False
    try:
        return param in inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False

def largura(func_name: str) -> dict:
    if _aceita(func_name, "width"): return {"width": "stretch"}
    if _aceita(func_name, "use_container_width"): return {"use_container_width": True}
    return {}

def grafico(fig, chave: str | None = None, zoom: bool = False, **kw):
    st.plotly_chart(fig, key=chave, config={"displayModeBar": False, "displaylogo": False, "scrollZoom": zoom}, **largura("plotly_chart"), **kw)

def tabela(df: pd.DataFrame, altura: int | None = None, **kw):
    st.dataframe(df, height=altura, hide_index=True, **largura("dataframe"), **kw)

def descarregar(df: pd.DataFrame, nome: str, etiqueta: str, chave: str | None = None):
    st.download_button(etiqueta, data=df.to_csv(index=False).encode("utf-8-sig"), file_name=nome, mime="text/csv", key=chave, **largura("download_button"))

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {{ --navy: {C.CORES['navy']}; --teal: {C.CORES['teal']}; --texto: {C.CORES['texto']}; --borda: #DCE4ED; }}
html, body, [class*="css"] {{ font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif; }}
#MainMenu, footer {{ visibility: hidden; }}
.stApp {{ background: {C.CORES['fundo']}; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1500px; }}
section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, #0E2A47 0%, #123A5C 55%, #0E2A47 100%); border-right: 1px solid #0A2138; }}
section[data-testid="stSidebar"] * {{ color: #E8EFF7 !important; }}
section[data-testid="stSidebar"] .stMarkdown h1, section[data-testid="stSidebar"] .stMarkdown h2, section[data-testid="stSidebar"] .stMarkdown h3 {{ color: #FFFFFF !important; }}
section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,.14); }}
section[data-testid="stSidebar"] label {{ font-size: .78rem !important; font-weight: 600 !important; letter-spacing: .02em; text-transform: uppercase; opacity: .92; }}
section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea {{ color: #0E2A47 !important; background: #FFFFFF !important; }}
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{ background: rgba(255,255,255,.96) !important; border-color: rgba(255,255,255,.25) !important; }}
section[data-testid="stSidebar"] div[data-baseweb="select"] * {{ color: #0E2A47 !important; }}
section[data-testid="stSidebar"] span[data-baseweb="tag"] {{ background: {C.CORES['teal']} !important; }}
section[data-testid="stSidebar"] span[data-baseweb="tag"] * {{ color: #fff !important; }}
section[data-testid="stSidebar"] button {{ background: rgba(255,255,255,.10) !important; border: 1px solid rgba(255,255,255,.28) !important; color: #fff !important; font-weight: 600; }}
section[data-testid="stSidebar"] button:hover {{ background: {C.CORES['teal']} !important; border-color: {C.CORES['teal']} !important; }}
section[data-testid="stSidebar"] [data-testid="stExpander"] {{ background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.14); border-radius: 10px; }}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary, section[data-testid="stSidebar"] [data-testid="stExpanderDetails"], section[data-testid="stSidebar"] [data-testid="stExpander"] details {{ background: transparent !important; color: #E8EFF7 !important; }}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{ background: rgba(255,255,255,.10) !important; }}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary p {{ font-weight: 700 !important; font-size: .85rem !important; }}
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {{ color: #8FD9D9 !important; }}
section[data-testid="stSidebar"] [data-testid="stDateInput"] input {{ color: #0E2A47 !important; -webkit-text-fill-color: #0E2A47 !important; font-weight: 600 !important; }}
section[data-testid="stSidebar"] div[role="radiogroup"] label {{ text-transform: none !important; font-size: .9rem !important; letter-spacing: 0 !important; padding: .32rem .5rem; border-radius: 8px; width: 100%; }}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{ background: rgba(255,255,255,.10); }}
section[data-testid="stSidebar"] div[role="radiogroup"] label p {{ font-weight: 600 !important; }}
.cab {{ background: linear-gradient(115deg, {C.CORES['navy']} 0%, {C.CORES['navy_claro']} 60%, #17607F 100%); border-radius: 16px; padding: 1.35rem 1.6rem; color: #fff; margin-bottom: 1.1rem; box-shadow: 0 10px 26px rgba(14,42,71,.18); }}
.cab .marca {{ font-size: .7rem; letter-spacing: .18em; text-transform: uppercase; color: #8FD9D9; font-weight: 700; margin-bottom: .3rem; }}
.cab h1 {{ font-size: 1.65rem; font-weight: 800; margin: 0; color: #fff; letter-spacing: -.02em; }}
.cab p {{ margin: .35rem 0 0; color: #C7D8E8; font-size: .9rem; }}
.cab .chips {{ margin-top: .8rem; display: flex; flex-wrap: wrap; gap: .4rem; }}
.cab .chip {{ background: rgba(255,255,255,.13); border: 1px solid rgba(255,255,255,.20); padding: .22rem .6rem; border-radius: 999px; font-size: .74rem; color: #EAF3FA; font-weight: 600; }}
.kpi {{ background: #fff; border: 1px solid var(--borda); border-radius: 14px; padding: .95rem 1.05rem; height: 100%; box-shadow: 0 2px 8px rgba(16,40,66,.05); border-top: 3px solid var(--navy); }}
.kpi .rot {{ font-size: .685rem; text-transform: uppercase; letter-spacing: .07em; color: #6C7C8C; font-weight: 700; margin-bottom: .3rem; }}
.kpi .val {{ font-size: 1.72rem; font-weight: 800; color: var(--texto); line-height: 1.1; letter-spacing: -.03em; }}
.kpi .val small {{ font-size: .9rem; font-weight: 700; color: #6C7C8C; }}
.kpi .sub {{ font-size: .755rem; color: #7A8896; margin-top: .28rem; font-weight: 500; }}
.kpi .sub b {{ color: var(--texto); }}
.sec {{ display: flex; align-items: baseline; gap: .6rem; margin: 1.35rem 0 .55rem; }}
.sec .barra {{ width: 4px; height: 20px; background: {C.CORES['teal']}; border-radius: 3px; display: inline-block; position: relative; top: 3px; }}
.sec h3 {{ margin: 0; font-size: 1.06rem; font-weight: 700; color: var(--texto); letter-spacing: -.01em; }}
.sec span.desc {{ font-size: .8rem; color: #7A8896; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ background: #fff; border-radius: 14px; }}
.alerta {{ border-radius: 12px; padding: .8rem 1rem; font-size: .86rem; margin-bottom: .5rem; border-left: 4px solid; background: #fff; border: 1px solid var(--borda); }}
.alerta b {{ color: var(--texto); }}
.ficha-linha {{ display: flex; justify-content: space-between; gap: 1rem; padding: .42rem 0; border-bottom: 1px dashed #E4EAF1; font-size: .86rem; }}
.ficha-linha .k {{ color: #6C7C8C; font-weight: 600; }}
.ficha-linha .v {{ color: var(--texto); font-weight: 600; text-align: right; }}
.pill {{ display: inline-block; padding: .16rem .55rem; border-radius: 999px; font-size: .72rem; font-weight: 700; margin: .12rem .18rem .12rem 0; }}
button[data-baseweb="tab"] {{ font-weight: 600; font-size: .88rem; }}
div[data-baseweb="tab-highlight"] {{ background: {C.CORES['teal']}; }}
div[data-testid="stMetricValue"] {{ font-weight: 800; letter-spacing: -.02em; }}
</style>
"""

def injetar_css(): st.markdown(CSS, unsafe_allow_html=True)

def cabecalho(titulo: str, subtitulo: str, chips: list[str] | None = None):
    chips_html = "".join(f'<span class="chip">{c}</span>' for c in (chips or []))
    st.markdown(f'<div class="cab"><div class="marca">{C.BANCO_NOME}</div><h1>{titulo}</h1><p>{subtitulo}</p><div class="chips">{chips_html}</div></div>', unsafe_allow_html=True)

def secao(titulo: str, desc: str = ""):
    d = f'<span class="desc">{desc}</span>' if desc else ""
    st.markdown(f'<div class="sec"><span class="barra"></span><h3>{titulo}</h3>{d}</div>', unsafe_allow_html=True)

def kpi(rotulo: str, valor: str, sub: str = "", cor: str | None = None, altura: int = 0):
    cor = cor or C.CORES["navy"]
    st.markdown(f'<div class="kpi" style="border-top-color:{cor}"><div class="rot">{rotulo}</div><div class="val">{valor}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

def linha_kpis(cartoes: list[dict]):
    cols = st.columns(len(cartoes), gap="small")
    for col, c in zip(cols, cartoes):
        with col: kpi(**c)

def alerta(texto: str, cor: str, fundo: str = "#FFFFFF"):
    st.markdown(f'<div class="alerta" style="border-left-color:{cor};background:{fundo}">{texto}</div>', unsafe_allow_html=True)

def pill(texto: str, cor: str, fundo: str | None = None):
    fundo = fundo or f"{cor}1A"
    return f'<span class="pill" style="background:{fundo};color:{cor}">{texto}</span>'

def ficha(linhas: list[tuple[str, str]]):
    html = "".join(f'<div class="ficha-linha"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in linhas)
    st.markdown(html, unsafe_allow_html=True)

def vazio(msg: str = "Nenhum cliente corresponde aos filtros selecionados."): st.info(msg, icon="🔍")
def nota(texto: str): st.caption(texto)

def num(x) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)): return "—"
    return f"{x:,.0f}".replace(",", " ")

def dec(x, casas: int = 1) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)): return "—"
    return f"{x:,.{casas}f}".replace(",", " ").replace(".", ",")

def pct(x, casas: int = 1) -> str: return f"{dec(x, casas)}%"

def data_br(x) -> str:
    if x is None or pd.isna(x): return "—"
    return pd.Timestamp(x).strftime("%d/%m/%Y")
