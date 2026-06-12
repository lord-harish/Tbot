from pathlib import Path
import tempfile

import streamlit as st

import config
from analysis.economic_calendar import EconomicCalendar
from analysis.gemini_analyzer import GeminiAnalyzer
from analysis.technical_analyzer import TechnicalAnalyzer
from database.db_manager import DatabaseManager


st.set_page_config(
    page_title="Forex AI Chart Analyzer",
    layout="wide",
)


def save_uploaded_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        return tmp_file.name


def render_metric(label, value):
    st.metric(label, value if value not in (None, "") else "N/A")


def get_api_key():
    if config.GEMINI_API_KEY:
        return config.GEMINI_API_KEY

    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


st.title("Forex AI Chart Analyzer")
st.caption("Upload a chart, select the market, and get a Gemini-powered trading analysis.")

api_key = get_api_key()
if not api_key:
    st.error(
        "GEMINI_API_KEY is missing. Add it in Streamlit app secrets when deployed, "
        "or in your local .env file."
    )
    st.stop()

with st.sidebar:
    st.header("Chart Setup")
    pair = st.selectbox("Pair", config.FOREX_PAIRS, index=0)
    timeframe = st.selectbox("Timeframe", config.TIMEFRAMES, index=5)
    include_calendar = st.toggle("Include economic calendar", value=config.ECONOMIC_CALENDAR_ENABLED)
    st.divider()
    st.caption("This tool is educational only and is not financial advice.")

uploaded_file = st.file_uploader(
    "Upload chart image",
    type=config.SUPPORTED_IMAGE_FORMATS,
    accept_multiple_files=False,
)

if uploaded_file:
    if uploaded_file.size > config.MAX_IMAGE_SIZE:
        st.error("Image is larger than the configured 10MB limit.")
        st.stop()

    st.image(uploaded_file, caption=f"{pair} chart", use_container_width=True)

analyze = st.button("Analyze Chart", type="primary", disabled=uploaded_file is None)

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
        analysis_result = gemini_analyzer.analyze_chart(
            image_path=image_path,
            pair=pair,
            timeframe=timeframe,
            calendar_context=calendar_context,
            image_features=image_features,
        )

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
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_metric("Direction", parsed.get("direction"))
        with col2:
            render_metric("Confidence", f"{parsed.get('confidence', 0)}%")
        with col3:
            render_metric("Bias", parsed.get("bias"))
        with col4:
            render_metric("Trade Quality", parsed.get("trade_quality_score"))

        col5, col6, col7 = st.columns(3)
        with col5:
            render_metric("Volatility Risk", parsed.get("volatility_risk"))
        with col6:
            render_metric("Primary Target", parsed.get("primary_target"))
        with col7:
            render_metric("Invalidation", parsed.get("invalidation_level"))

    st.subheader("Full Analysis")
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
                use_container_width=True,
            )
        else:
            st.caption("No saved analyses yet.")
    except Exception as exc:
        st.caption(f"History unavailable: {exc}")
