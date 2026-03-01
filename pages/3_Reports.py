import streamlit as st
from utils import load_data
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO


if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("You must login to access this page.")
    st.stop()
st.set_page_config(layout="wide")

st.image("breathesmartug.png", width=320)

st.title("📄 Monthly Impact Report")

df = load_data()

month = datetime.now().strftime("%B %Y")

st.markdown(f"## BreatheSmart UG Report – {month}")

total = len(df)
high = df[df["Risk"] >=11].shape[0]
moderate = df[(df["Risk"] >= 6) & (df["Risk"] < 11)].shape[0]
low = df[df["Risk"] < 6].shape[0]

st.write(f"Total Screenings: {total}")
st.write(f"High Risk Cases: {high}")
st.write(f"Moderate Risk Cases: {moderate}")
st.write(f"Low Risk Cases: {low}")


def generate_pdf_report():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    try:
        logo = Image("new_breathsmart.png", width=140, height=60)
        elements.append(logo)
        elements.append(Spacer(1, 10))
    except Exception:
        pass
    month = datetime.now().strftime("%B %Y")
    elements.append(Paragraph(
        f"<b>BreatheSmart UGANDA Impact Report– {month}</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))
    df = load_data()
    total = len(df)
    high = df[df["Risk"] >= 11].shape[0]
    moderate = df[(df["Risk"] >= 6) & (df["Risk"] < 11)].shape[0]
    low = df[df["Risk"] < 6].shape[0]
    table_data = [
        ["Cases", "Numbers"],
        ["High Risk", high],
        ["Moderate Risk", moderate],
        ["Low Risk", low],
        ["Total Screenings", total],
    ]

    table = Table(table_data, colWidths=[170, 120])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(
        f"<b>Screenings Per Division</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 12))

    LL = len(df[(df["Division"] == "Rubaga") & (df["Risk"] < 6)])
    # LM = len(df[(df["Division"] == "Lubaga") & (df["Risk"] >= 5)])
    LM = df[
        (df["Division"] == "Rubaga") &
        (df["Risk"].between(6, 11, inclusive="left"))
        ].shape[0]
    LH = len(df[(df["Division"] == "Rubaga") & (df["Risk"] >= 11)])

    CL = len(df[(df["Division"] == "Central") & (df["Risk"] < 6)])
    # CM = len(df[(df["Division"] == "Central") & (df["Risk"] >= 5)])
    CM = df[
        (df["Division"] == "Central") &
        (df["Risk"].between(6, 11, inclusive="left"))
        ].shape[0]
    CH = len(df[(df["Division"] == "Central") & (df["Risk"] >= 11)])

    NL = len(df[(df["Division"] == "Nakawa") & (df["Risk"] < 6)])
    # NM = len(df[(df["Division"] == "Nakawa") & (df["Risk"] >= 5)])
    NM = df[
        (df["Division"] == "Nakawa") &
        (df["Risk"].between(6, 11, inclusive="left"))
        ].shape[0]
    NH = len(df[(df["Division"] == "Nakawa") & (df["Risk"] >= 11)])

    ML = len(df[(df["Division"] == "Makindye") & (df["Risk"] < 6)])
    # MM = len(df[(df["Division"] == "Makindye") & (df["Risk"] >= 5)])
    MM = df[
        (df["Division"] == "Makindye") &
        (df["Risk"].between(6, 11, inclusive="left"))
        ].shape[0]
    MH = len(df[(df["Division"] == "Makindye") & (df["Risk"] >= 11)])

    KL = len(df[(df["Division"] == "Kawempe") & (df["Risk"] < 6)])
    # KM = len(df[(df["Division"] == "Kawempe") & (df["Risk"] >= 5)])
    KM = df[
        (df["Division"] == "Kawempe") &
        (df["Risk"].between(6, 11, inclusive="left"))
        ].shape[0]
    KH = len(df[(df["Division"] == "Kawempe") & (df["Risk"] >= 11)])

    CT = CL + CM + CH
    KT = KL + KM + KH
    LT = LL + LM + LH
    NT = NL + NM + NH
    MT = ML + MM + MH

    table2_data = [
        ["Division", "High", "Moderate", "Low", "Total"],
        ["Central", CH, CM, CL, CT],
        ["Nakawa", NH, NM, NL, NT],
        ["Rubaga", LH, LM, LL, LT],
        ["Makindye", MH, MM, ML, MT],
        ["Kawempe", KH, KM, KL, KT],
    ]

    table2 = Table(table2_data, colWidths=[120, 100, 100, 100, 100])
    table2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table2)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        f"<b>This report is made from user's data, while keeping personal information anonymous.</b>",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        f"<b>Reviewed and Approved By:________________________________</b>",
        styles["Normal"]
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer

st.download_button(
        "📥 Download PDF Report",
        data=generate_pdf_report(),
        file_name="BreatheSmart_UG_Monthly_Report.pdf",
        mime="application/pdf",
        key="download-pdf",
        use_container_width=True
        # st.success("PDF Report Downloaded Successfully.")
    )
