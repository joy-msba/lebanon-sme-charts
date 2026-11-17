# Lebanon SME charts

Interactive Streamlit app (Python, Plotly) for a data story on Lebanese small-business owners: **not out of passion, out of power**.

- **Chart 1:** why Lebanese owners started their business (share naming each reason among their top three).
- **Chart 2:** how much current energy costs have affected their business, Lebanon vs 90 countries.

**Data:** Meta / OECD / World Bank Future of Business Survey, SME leaders (aggregated country data). Lebanon n=124 (motives) and n=81 (energy costs).

**Run locally:**

```
pip install -r requirements.txt
streamlit run app.py
```

Add `?chart=motives` or `?chart=energy` to the app address to show one chart only.

Course project for MSBA 325 Data Visualization & Communication, AUB.
