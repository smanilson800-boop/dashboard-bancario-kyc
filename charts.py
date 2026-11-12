from __future__ import annotations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import config as C

FONTE = "Inter, -apple-system, Segoe UI, sans-serif"

def _base(fig: go.Figure, altura: int = 340, margens=(8, 8, 8, 8), legenda: bool = False) -> go.Figure:
    fig.update_layout(template="plotly_white", height=altura, margin=dict(l=margens[0], r=margens[1], t=margens[2], b=margens[3]), font=dict(family=FONTE, size=12, color=C.CORES["texto"]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=legenda, legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(size=11), traceorder="normal"), hoverlabel=dict(bgcolor="#0E2A47", font=dict(color="#fff", family=FONTE, size=12), bordercolor="#0E2A47"), hovermode="closest", bargap=0.28)
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#DCE4ED", ticks="outside", tickcolor="#DCE4ED", tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="#EEF2F7", zeroline=False, showline=False, tickfont=dict(size=11))
    return fig

def donut(labels, valores, cores: dict | None = None, altura=320, centro: str = "", ordem: list | None = None) -> go.Figure:
    pares = dict(zip(list(labels), list(valores)))
    if ordem: chaves = [l for l in ordem if l in pares] + [l for l in pares if l not in ordem]
    else: chaves = list(pares)
    labels, valores = chaves, [pares[l] for l in chaves]
    lista_cores = [cores.get(l, C.CORES["azul"]) for l in labels] if cores else C.SEQ_AZUIS
    fig = go.Figure(go.Pie(labels=list(labels), values=list(valores), hole=0.62, marker=dict(colors=lista_cores, line=dict(color="#fff", width=2)), textinfo="percent", textposition="inside", insidetextfont=dict(size=12, color="#fff", family=FONTE), hovertemplate="<b>%{label}</b><br>%{value} clientes<br>%{percent}<extra></extra>", sort=False, direction="clockwise"))
    if centro: fig.add_annotation(text=centro, x=0.5, y=0.5, showarrow=False, font=dict(size=17, family=FONTE, color=C.CORES["texto"]))
    _base(fig, altura, legenda=True)
    fig.update_layout(legend=dict(orientation="v", x=1.0, y=0.5, yanchor="middle", xanchor="left"))
    return fig

def barras_h(df: pd.DataFrame, cat: str, val: str, cor: str = C.CORES["azul"], altura=340, texto=None, escala_cor: dict | None = None, fmt: str = ",.0f", titulo_x: str = "") -> go.Figure:
    d = df.sort_values(val, ascending=True)
    cores = [escala_cor.get(c, cor) for c in d[cat]] if escala_cor else cor
    fig = go.Figure(go.Bar(x=d[val], y=d[cat].astype(str), orientation="h", marker=dict(color=cores, line=dict(width=0)), text=d[texto] if texto else d[val], texttemplate="%{text:" + fmt + "}", textposition="outside", textfont=dict(size=11, color="#5A6B7C"), cliponaxis=False, hovertemplate="<b>%{y}</b><br>%{x:" + fmt + "}<extra></extra>"))
    _base(fig, altura)
    fig.update_xaxes(title=titulo_x, showgrid=True, gridcolor="#EEF2F7", range=[0, float(d[val].max() or 1) * 1.18])
    fig.update_yaxes(title="", automargin=True)
    return fig

def barras_v(df: pd.DataFrame, cat: str, val: str, cor: str = C.CORES["azul"], altura=320, escala_cor: dict | None = None, fmt: str = ",.0f", ordem: list | None = None, titulo_y: str = "") -> go.Figure:
    d = df.copy()
    if ordem:
        d[cat] = pd.Categorical(d[cat], categories=ordem, ordered=True)
        d = d.sort_values(cat)
    cores = [escala_cor.get(str(c), cor) for c in d[cat]] if escala_cor else cor
    fig = go.Figure(go.Bar(x=d[cat].astype(str), y=d[val], marker=dict(color=cores, line=dict(width=0)), text=d[val], texttemplate="%{text:" + fmt + "}", textposition="outside", textfont=dict(size=11, color="#5A6B7C"), cliponaxis=False, hovertemplate="<b>%{x}</b><br>%{y:" + fmt + "}<extra></extra>"))
    _base(fig, altura)
    fig.update_yaxes(title=titulo_y, range=[0, float(d[val].max() or 1) * 1.18])
    fig.update_xaxes(title="")
    return fig

def barras_empilhadas(df: pd.DataFrame, cat: str, val: str, grupo: str, cores: dict, ordem_grupo: list | None = None, altura=360, percent: bool = False, ordem_cat: list | None = None) -> go.Figure:
    fig = go.Figure()
    grupos = ordem_grupo or sorted(df[grupo].unique())
    categorias = ordem_cat or list(df[cat].unique())
    for g in grupos:
        sub = df[df[grupo] == g].set_index(cat).reindex(categorias).fillna(0).reset_index()
        fig.add_trace(go.Bar(x=sub[cat].astype(str), y=sub[val], name=str(g), marker=dict(color=cores.get(str(g), C.CORES["azul"]), line=dict(width=0)), hovertemplate="<b>%{x}</b><br>" + str(g) + ": %{y:,.1f}" + ("%" if percent else "") + "<extra></extra>"))
    _base(fig, altura, legenda=True)
    fig.update_layout(barmode="stack", bargap=0.35)
    fig.update_yaxes(title="%" if percent else "Clientes", ticksuffix="%" if percent else "", range=[0, 100] if percent else None)
    fig.update_xaxes(title="")
    return fig

def heatmap(tab: pd.DataFrame, altura=340, percent=False, escala=None, titulo_z="") -> go.Figure:
    escala = escala or [[0, "#EAF1FA"], [0.5, "#5C93E8"], [1, "#0E2A47"]]
    z = tab.values
    fig = go.Figure(go.Heatmap(z=z, x=[str(c) for c in tab.columns], y=[str(i) for i in tab.index], colorscale=escala, xgap=3, ygap=3, text=[[f"{v:,.1f}%" if percent else f"{v:,.0f}" for v in linha] for linha in z], texttemplate="%{text}", textfont=dict(size=11, family=FONTE), colorbar=dict(thickness=10, len=0.85, outlinewidth=0, ticksuffix="%" if percent else "", title=titulo_z), hovertemplate="<b>%{y}</b> × <b>%{x}</b><br>%{text}<extra></extra>"))
    _base(fig, altura)
    fig.update_xaxes(side="top", showgrid=False, ticks="")
    fig.update_yaxes(autorange="reversed", showgrid=False, ticks="")
    return fig

def histograma(serie: pd.Series, cor: str = C.CORES["azul"], nbins: int = 28, altura=310, titulo_x="", media: float | None = None) -> go.Figure:
    fig = go.Figure(go.Histogram(x=serie.dropna(), nbinsx=nbins, marker=dict(color=cor, line=dict(color="#fff", width=1)), hovertemplate="Intervalo: %{x}<br>Clientes: %{y}<extra></extra>"))
    _base(fig, altura)
    if media is not None:
        fig.add_vline(x=media, line_width=2, line_dash="dot", line_color=C.CORES["teal"], annotation_text=f"média {media:,.1f}".replace(".", ","), annotation_position="top right", annotation_font=dict(size=11, color=C.CORES["teal"]))
    fig.update_xaxes(title=titulo_x)
    fig.update_yaxes(title="Clientes")
    return fig

def piramide(df: pd.DataFrame, altura=360) -> go.Figure:
    fig = go.Figure()
    ordem = C.LABELS_IDADE
    for sexo, cor, sinal in [("Masculino", C.CORES["azul"], -1), ("Feminino", C.CORES["teal"], 1)]:
        sub = df[df["Sexo"] == sexo].set_index("Segmento_Idade").reindex(ordem).fillna(0)
        vals = sub["n"] * sinal
        fig.add_trace(go.Bar(x=vals, y=ordem, orientation="h", name=sexo, marker=dict(color=cor, line=dict(width=0)), customdata=sub["n"].abs(), hovertemplate="<b>%{y}</b><br>" + sexo + ": %{customdata}<extra></extra>"))
    _base(fig, altura, legenda=True)
    fig.update_layout(barmode="relative", bargap=0.18)
    maxi = float(df["n"].max() or 1) * 1.15
    fig.update_xaxes(range=[-maxi, maxi], title="Clientes", tickvals=[-maxi * f for f in (0.75, 0.5, 0.25, 0)] + [maxi * f for f in (0.25, 0.5, 0.75)], ticktext=[str(int(maxi * f)) for f in (0.75, 0.5, 0.25, 0, 0.25, 0.5, 0.75)])
    fig.update_yaxes(title="")
    return fig

def mapa_mundi(df: pd.DataFrame, altura=430, escala=None, titulo_z="Clientes", fmt: str = ",.0f", rotulo: str = "clientes") -> go.Figure:
    escala = escala or [[0, "#DCE9F7"], [0.25, "#7FA8E8"], [0.6, "#2E6FDB"], [1, "#0E2A47"]]
    fig = go.Figure(go.Choropleth(locations=df["ISO3"], z=df["n"], text=df["Pais_PT"], colorscale=escala, marker_line_color="#FFFFFF", marker_line_width=0.5, colorbar=dict(thickness=11, len=0.72, outlinewidth=0, title=titulo_z, tickfont=dict(size=10)), hovertemplate="<b>%{text}</b><br>%{z:" + fmt + "} " + rotulo + "<extra></extra>", zmin=0))
    _base(fig, altura, margens=(0, 0, 0, 0))
    fig.update_geos(showframe=False, showcoastlines=True, coastlinecolor="#C6D3E0", showland=True, landcolor="#F2F5F9", showocean=True, oceancolor="#FBFDFF", showcountries=True, countrycolor="#DCE4ED", projection_type="natural earth", lataxis_range=[-58, 85], bgcolor="rgba(0,0,0,0)")
    return fig