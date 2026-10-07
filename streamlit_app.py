from pathlib import Path
import os
import subprocess
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_ROOT / "venv" / "Scripts" / "python.exe"

if (
    os.name == "nt"
    and VENV_PYTHON.exists()
    and Path(sys.executable).resolve() != VENV_PYTHON.resolve()
):
    subprocess.run(
        [str(VENV_PYTHON), "-m", "streamlit", "run", str(Path(__file__).resolve()), *sys.argv[1:]],
        check=False,
    )
    sys.exit()

if __name__ == "__main__" and "streamlit" not in sys.modules:
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(Path(__file__).resolve()), *sys.argv[1:]],
        check=False,
    )
    sys.exit()

import streamlit as st

import config
from analysis.economic_calendar import EconomicCalendar
from analysis.gemini_analyzer import GeminiAnalyzer
from analysis.technical_analyzer import TechnicalAnalyzer
from database.db_manager import DatabaseManager


st.set_page_config(
    page_title="Tbot",
    layout="wide",
)


def inject_theme():
    st.markdown(
        """
        <style>
            :root {
                --bg: #050712;
                --panel: rgba(13, 18, 34, 0.84);
                --panel-strong: rgba(18, 26, 48, 0.94);
                --line: rgba(125, 245, 255, 0.20);
                --text: #edf7ff;
                --muted: #8fa5ba;
                --cyan: #63f7ff;
                --green: #7cff9b;
                --pink: #ff5fc8;
                --amber: #ffd166;
            }

            .stApp {
                color: var(--text);
                background:
                    radial-gradient(circle at 18% 12%, rgba(99, 247, 255, 0.18), transparent 27%),
                    radial-gradient(circle at 82% 6%, rgba(255, 95, 200, 0.14), transparent 26%),
                    linear-gradient(135deg, #050712 0%, #0a1020 42%, #07131b 72%, #050712 100%);
            }

            .stApp::before {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background-image:
                    radial-gradient(rgba(255,255,255,0.35) 1px, transparent 1px),
                    radial-gradient(rgba(99,247,255,0.22) 1px, transparent 1px);
                background-size: 64px 64px, 108px 108px;
                background-position: 0 0, 24px 38px;
                opacity: 0.26;
            }

            [data-testid="stSidebar"] {
                background: rgba(5, 9, 20, 0.92);
                border-right: 1px solid rgba(99, 247, 255, 0.16);
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            .block-container {
                padding-top: 2rem;
                max-width: 1180px;
            }

            .tbot-hero {
                border: 1px solid rgba(99, 247, 255, 0.22);
                border-radius: 8px;
                background:
                    linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(5, 11, 25, 0.78)),
                    repeating-linear-gradient(90deg, rgba(99,247,255,0.05) 0 1px, transparent 1px 90px);
                box-shadow: 0 24px 70px rgba(0, 0, 0, 0.36), inset 0 1px 0 rgba(255,255,255,0.06);
                padding: 28px;
                margin-bottom: 22px;
                position: relative;
                overflow: hidden;
            }

            .tbot-kicker {
                color: var(--cyan);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0;
                text-transform: uppercase;
                margin-bottom: 8px;
            }

            .tbot-title {
                color: var(--text);
                font-size: clamp(2.2rem, 6vw, 4.6rem);
                line-height: 0.95;
                font-weight: 800;
                letter-spacing: 0;
                margin: 0;
            }

            .tbot-subtitle {
                color: var(--muted);
                font-size: 1.02rem;
                max-width: 720px;
                margin-top: 12px;
            }

            .market-strip {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 10px;
                margin-top: 22px;
            }

            .market-chip {
                min-height: 72px;
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 8px;
                background: rgba(255,255,255,0.045);
                padding: 12px;
            }

            .chip-label {
                color: var(--muted);
                font-size: 0.72rem;
                text-transform: uppercase;
            }

            .chip-value {
                color: var(--text);
                font-size: 1.16rem;
                font-weight: 750;
                margin-top: 5px;
            }

            .panel {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: var(--panel);
                padding: 18px;
                box-shadow: 0 16px 48px rgba(0,0,0,0.25);
            }

            .signal-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 12px;
                margin: 18px 0;
            }

            .signal-card {
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 8px;
                background: var(--panel-strong);
                padding: 16px;
                min-height: 96px;
            }

            .signal-label {
                color: var(--muted);
                font-size: 0.72rem;
                text-transform: uppercase;
            }

            .signal-value {
                color: var(--text);
                font-size: 1.35rem;
                font-weight: 800;
                margin-top: 8px;
                overflow-wrap: anywhere;
            }

            .signal-value.buy,
            .signal-value.up {
                color: var(--green);
            }

            .signal-value.sell,
            .signal-value.down {
                color: #ff7a7a;
            }

            .signal-value.wait,
            .signal-value.no_trade,
            .signal-value.consolidation {
                color: var(--amber);
            }

            .stButton > button {
                width: 100%;
                border-radius: 8px;
                border: 1px solid rgba(124, 255, 155, 0.45);
                background: linear-gradient(135deg, #31f2b2, #32a7ff);
                color: #031018;
                font-weight: 800;
                min-height: 48px;
                box-shadow: 0 10px 34px rgba(49, 242, 178, 0.22);
            }

            .stButton > button:disabled {
                background: rgba(255,255,255,0.08);
                color: rgba(255,255,255,0.35);
                border-color: rgba(255,255,255,0.10);
                box-shadow: none;
            }

            [data-testid="stFileUploader"] section {
                border-radius: 8px;
                border: 1px dashed rgba(99, 247, 255, 0.35);
                background: rgba(10, 16, 32, 0.72);
            }

            [data-testid="stMetricValue"],
            [data-testid="stMarkdownContainer"] {
                color: var(--text);
            }

            div[data-testid="stDataFrame"] {
                border: 1px solid rgba(99, 247, 255, 0.16);
                border-radius: 8px;
                overflow: hidden;
            }

            @media (max-width: 800px) {
                .block-container {
                    padding: 1rem 0.85rem 2rem;
                }
                .tbot-hero {
                    padding: 20px;
                }
                .market-strip,
                .signal-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_uploaded_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        return tmp_file.name


def render_metric(label, value):
    st.metric(label, value if value not in (None, "") else "N/A")


def render_signal_card(label, value, tone=""):
    display_value = value if value not in (None, "") else "N/A"
    tone_class = str(tone or display_value).lower().replace(" ", "_")
    st.markdown(
        f"""
        <div class="signal-card">
            <div class="signal-label">{label}</div>
            <div class="signal-value {tone_class}">{display_value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_api_key():
    if config.GEMINI_API_KEY:
        return config.GEMINI_API_KEY

    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


inject_theme()

st.markdown(
    """
    <section class="tbot-hero">
        <div class="tbot-kicker">AI market intelligence</div>
        <h1 class="tbot-title">Tbot</h1>
        <div class="tbot-subtitle">
            Dark terminal for chart-image forecasting, event risk, and trade-quality signals.
        </div>
        <div class="market-strip">
            <div class="market-chip"><div class="chip-label">Mode</div><div class="chip-value">Vision AI</div></div>
            <div class="market-chip"><div class="chip-label">Markets</div><div class="chip-value">FX + XAU</div></div>
            <div class="market-chip"><div class="chip-label">Signal</div><div class="chip-value">Bias + Risk</div></div>
            <div class="market-chip"><div class="chip-label">Access</div><div class="chip-value">Mobile Ready</div></div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

api_key = get_api_key()
if not api_key:
    st.error(
        "GEMINI_API_KEY is missing. Add it in Streamlit app secrets when deployed, "
        "or in your local .env file."
    )
    st.stop()

with st.sidebar:
    st.header("Tbot")
    pair = st.selectbox("Pair", config.FOREX_PAIRS, index=0)
    timeframe = st.selectbox("Timeframe", config.TIMEFRAMES, index=5)
    include_calendar = st.toggle("Include economic calendar", value=config.ECONOMIC_CALENDAR_ENABLED)
    st.divider()
    st.caption("This tool is educational only and is not financial advice.")

st.markdown('<div class="panel">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Chart image", type=config.SUPPORTED_IMAGE_FORMATS, accept_multiple_files=False)

if uploaded_file:
    if uploaded_file.size > config.MAX_IMAGE_SIZE:
        st.error("Image is larger than the configured 10MB limit.")
        st.stop()

    st.image(uploaded_file, caption=f"{pair} chart", width="stretch")

analyze = st.button("Run Tbot Analysis", type="primary", disabled=uploaded_file is None)
st.markdown("</div>", unsafe_allow_html=True)

if analyze and uploaded_file:
    image_path = save_uploaded_file(uploaded_file)
    db = DatabaseManager(config.DB_PATH)
    technical_analyzer = TechnicalAnalyzer()
    gemini_analyzer = GeminiAnalyzer(api_key)

    with st.status("Analyzing chart...", expanded=True) as status:
        st.write("Scanning local image features")
        image_features = technical_analyzer.analyze_image_features(image_path)

        calendar_context = None
        if include_calendar:
            st.write("Fetching relevant economic calendar events")
            calendar_context = EconomicCalendar().get_events_for_pair(pair)

        st.write("Requesting Gemini analysis")
        try:
            analysis_result = gemini_analyzer.analyze_chart(
                image_path=image_path,
                pair=pair,
                timeframe=timeframe,
                calendar_context=calendar_context,
                image_features=image_features,
            )
        except Exception as exc:
            status.update(label="Analysis failed", state="error")
            st.error(f"AI Analysis could not complete: {exc}")
            st.info("Tip: Gemini servers may be experiencing temporary high demand or rate limits. Please try again in a few moments.")
            st.stop()

        parsed = gemini_analyzer.parse_analysis_response(analysis_result["raw_analysis"])

        st.write("Saving analysis history")
        db.save_analysis(
            pair=pair,
            timeframe=timeframe,
            image_path=uploaded_file.name,
            analysis_result=analysis_result["raw_analysis"],
            prediction=parsed.get("direction", "UNKNOWN") if parsed else "UNKNOWN",
            confidence=parsed.get("confidence", 0) if parsed else 0,
            patterns=[],
            support_levels=parsed.get("support_levels", []) if parsed else [],
            resistance_levels=parsed.get("resistance_levels", []) if parsed else [],
        )
        status.update(label="Analysis complete", state="complete")

    if parsed:
        st.markdown('<div class="signal-grid">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_signal_card("Direction", parsed.get("direction"))
        with col2:
            render_signal_card("Confidence", f"{parsed.get('confidence', 0)}%")
        with col3:
            render_signal_card("Bias", parsed.get("bias"))
        with col4:
            render_signal_card("Trade Quality", parsed.get("trade_quality_score"))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="signal-grid">', unsafe_allow_html=True)
        col5, col6, col7 = st.columns(3)
        with col5:
            render_signal_card("Volatility Risk", parsed.get("volatility_risk"))
        with col6:
            render_signal_card("Primary Target", parsed.get("primary_target"))
        with col7:
            render_signal_card("Invalidation", parsed.get("invalidation_level"))
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Tbot Analysis")
    st.markdown(analysis_result["raw_analysis"])

    if include_calendar and calendar_context:
        with st.expander("Economic calendar context"):
            st.write(calendar_context.get("summary", "No summary available."))
            for event in calendar_context.get("events", []):
                st.write(
                    f"{EconomicCalendar.format_event_time(event['time_utc'])} | "
                    f"{event['currency']} | {event['impact'].upper()} | {event['title']}"
                )

st.divider()
with st.expander("Recent analysis history"):
    try:
        db = DatabaseManager(config.DB_PATH)
        history = db.get_analysis_history(limit=10)
        if history:
            st.dataframe(
                [
                    {
                        "time": item["timestamp"],
                        "pair": item["pair"],
                        "timeframe": item["timeframe"],
                        "prediction": item["prediction"],
                        "confidence": item["confidence"],
                    }
                    for item in history
                ],
                width="stretch",
            )
        else:
            st.caption("No saved analyses yet.")
    except Exception as exc:
        st.caption(f"History unavailable: {exc}")
