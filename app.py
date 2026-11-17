"""Lebanon SME charts: interactive Streamlit app (Plotly charts with hover tooltips).

Run locally:   pip install -r requirements.txt   then   streamlit run app.py
Show one chart only (for embedding):  ?chart=energy  or  ?chart=motives
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Colours: grey for context, one orange highlight (preattentive attribute)
INK, MUTED = "#111827", "#4B5563"
GREY, GREY_DARK = "#9CA3AF", "#6B7280"
RULE, ORANGE, ORANGE_SOFT, BAND = "#E5E7EB", "#C2410C", "#F8D9CC", "#FDEEE7"

st.set_page_config(page_title="Out of Power Charts", layout="centered")

energy = pd.read_csv("energy_cost_by_country.csv").sort_values("rank").head(9).reset_index(drop=True)
motives = pd.read_csv("motives_lebanon_vs_world.csv")
MEDIAN = float(energy["world_median_pct"].iloc[0])

LABELS = {"Pursue a passion or hobby": "Passion or hobby", "A new idea nobody was doing": "A new idea"}


def energy_chart():
    fig = go.Figure()
    n = len(energy)
    for i, r in energy.iterrows():
        lb = r["country"] == "Lebanon"
        v = r["share_a_lot_or_great_deal_pct"]
        fig.add_shape(type="line", x0=MEDIAN, x1=v, y0=i, y1=i,
                      line=dict(color=ORANGE_SOFT if lb else RULE, width=3), layer="below")
        fig.add_trace(go.Scatter(
            x=[v], y=[i], mode="markers+text", text=[f"{v:.0f}%"], textposition="middle right",
            textfont=dict(size=22 if lb else 16, color=ORANGE if lb else MUTED),
            marker=dict(size=22 if lb else 14, color=ORANGE if lb else GREY),
            customdata=[[r["country"], r["respondents"], r["approx_low_pct"], r["approx_high_pct"]]],
            hovertemplate="<b>%{customdata[0]}</b><br>%{x:.1f}% say energy costs hit them a lot or a great deal"
                          "<br>Range about %{customdata[2]:.0f} to %{customdata[3]:.0f}% · n=%{customdata[1]}<extra></extra>",
            showlegend=False))
        fig.add_annotation(x=0, xref="paper", y=i, yref="y", xanchor="right", xshift=-10, showarrow=False,
                           text=f"<b>{r['country']}</b>" if lb else r["country"],
                           font=dict(size=17, color=ORANGE if lb else INK))
    fig.add_vline(x=MEDIAN, line=dict(color=INK, width=2.5, dash="dash"))
    fig.add_annotation(x=MEDIAN, y=-1.0, yref="y", showarrow=False, text="<b>World median 39%</b>",
                       font=dict(size=17, color=INK))
    fig.update_xaxes(range=[0, 82], visible=False, fixedrange=True)
    fig.update_yaxes(range=[n - 0.4, -1.5], visible=False, fixedrange=True)
    fig.update_layout(height=520, margin=dict(l=190, r=20, t=10, b=10), plot_bgcolor="white",
                      paper_bgcolor="white", hoverlabel=dict(font_size=14))
    return fig


def motives_chart():
    """Gap chart: Lebanon minus world median, in percentage points (one encoding, orange = passion)."""
    d = motives.sort_values("gap_pts", ascending=False).reset_index(drop=True)
    n = len(d)
    fig = go.Figure()
    for i, r in d.iterrows():
        ps = r["is_passion"] == "Passion"
        g = float(r["gap_pts"])
        txt = f"{g:+.0f} pts".replace("-", "\u2212")
        fig.add_trace(go.Bar(
            x=[g], y=[i], orientation="h", width=0.62,
            marker=dict(color=ORANGE if ps else GREY),
            text=[f"<b>{txt}</b>" if ps else txt], textposition="outside", cliponaxis=False,
            textfont=dict(size=18 if ps else 16, color=ORANGE if ps else MUTED),
            customdata=[[r["motive"], r["lebanon_pct"], r["world_median_pct"], r["lebanon_rank"],
                         r["countries_ranked"], r["approx_low_pct"], r["approx_high_pct"],
                         r["respondents_lebanon"]]],
            hovertemplate="<b>%{customdata[0]}</b><br>Lebanon %{customdata[1]:.1f}% vs world median %{customdata[2]:.1f}%"
                          "<br>Rank %{customdata[3]} of %{customdata[4]} countries"
                          "<br>Lebanon range about %{customdata[5]:.0f} to %{customdata[6]:.0f}% \u00b7 n=%{customdata[7]}<extra></extra>",
            showlegend=False))
        fig.add_annotation(x=0, xref="paper", y=i, yref="y", xanchor="right", xshift=-10, showarrow=False,
                           text=f"<b>{LABELS.get(r['motive'], r['motive'])}</b>" if ps else LABELS.get(r["motive"], r["motive"]),
                           font=dict(size=17, color=ORANGE if ps else INK))
    fig.add_vline(x=0, line=dict(color=INK, width=2))
    fig.add_annotation(x=0, y=-0.95, yref="y", showarrow=False, text="<b>World median</b>", font=dict(size=16, color=INK))
    fig.add_annotation(x=-1, y=-0.95, yref="y", xanchor="right", showarrow=False,
                       text="Lebanon lower \u2190", font=dict(size=15, color=MUTED))
    fig.add_annotation(x=1, y=-0.95, yref="y", xanchor="left", showarrow=False,
                       text="\u2192 Lebanon higher", font=dict(size=15, color=MUTED))
    fig.update_xaxes(range=[-19, 13], visible=False, fixedrange=True)
    fig.update_yaxes(range=[n - 0.4, -1.5], visible=False, fixedrange=True)
    fig.update_layout(height=520, margin=dict(l=200, r=20, t=10, b=10), plot_bgcolor="white",
                      paper_bgcolor="white", bargap=0.3, hoverlabel=dict(font_size=14))
    return fig


which = st.query_params.get("chart", "both")

if which in ("both", "energy"):
    st.subheader("Lebanese business owners feel energy costs harder than almost anyone")
    st.caption('Share saying energy costs affected their business "a lot" or "a great deal", top 9 of 90 countries')
    st.plotly_chart(energy_chart(), use_container_width=True, config={"displayModeBar": False})
    st.caption("Source: Meta / OECD / World Bank Future of Business Survey, SME leaders. Survey-weighted shares; "
               "countries with at least 50 responses. Lebanon n=81. Hover a row for the approximate 95% range.")

if which in ("both", "motives"):
    st.subheader("Passion is not why Lebanese owners say they started: it ranks 88th of 94")
    st.caption("Lebanon's share naming each reason among their top three, minus the world median, in percentage points")
    st.plotly_chart(motives_chart(), use_container_width=True, config={"displayModeBar": False})
    st.caption("Source: Meta / OECD / World Bank Future of Business Survey, SME leaders. Lebanon n=124; "
               "owners chose up to three reasons. Hover a row for rank and range.")
