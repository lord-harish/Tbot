from google import genai
from google.genai import types
import base64
from pathlib import Path
import mimetypes
from utils.logger import get_logger
import config
from analysis.economic_calendar import EconomicCalendar

logger = get_logger(__name__)

class GeminiAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
    
    def encode_image_to_base64(self, image_path):
        """Convert image to base64"""
        try:
            with open(image_path, 'rb') as image_file:
                return base64.standard_b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image: {e}")
            return None
    
    def analyze_chart(self, image_path, pair, timeframe, calendar_context=None, image_features=None):
        """Analyze forex chart using Gemini with technical and macro context."""
        try:
            # Read image file
            image_file = Path(image_path)
            if not image_file.exists():
                logger.error(f"Image file not found: {image_path}")
                return None
            
            # Upload image to Gemini
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Prepare the analysis prompt
            prompt = self._create_analysis_prompt(
                pair=pair,
                timeframe=timeframe,
                calendar_context=calendar_context,
                image_features=image_features
            )
            mime_type = mimetypes.guess_type(image_path)[0] or 'image/png'
            
            # Call Gemini API with vision capabilities
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=[
                    types.Part.from_bytes(
                        data=image_data,
                        mime_type=mime_type
                    ),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    top_p=0.8,
                    top_k=32,
                )
            )
            
            if response.text:
                analysis_result = {
                    'raw_analysis': response.text,
                    'pair': pair,
                    'timeframe': timeframe,
                    'image_path': image_path
                }
                logger.info(f"Chart analysis completed for {pair} {timeframe}")
                return analysis_result
            else:
                logger.error("No response from Gemini API")
                raise RuntimeError("No response from Gemini API")
                
        except Exception as e:
            logger.error(f"Error analyzing chart: {e}")
            raise
    
    def _create_analysis_prompt(self, pair, timeframe, calendar_context=None, image_features=None):
        """Create a higher-level, evidence-driven analysis prompt."""
        calendar_text = self._format_calendar_context(calendar_context)
        image_feature_text = self._format_image_features(image_features)

        prompt = f"""
You are an institutional-grade forex analyst. Analyze this uploaded {pair} chart on the {timeframe} timeframe.

Goal: produce a higher-level trading forecast that combines visible price action, market structure, liquidity, risk management, and relevant economic-calendar event risk.

Accuracy rules:
- Base every claim on visible chart evidence or the supplied calendar context.
- If the screenshot does not show enough price scale/detail, say so and lower confidence.
- Do not force a trade. Use NO_TRADE when event risk, unclear structure, or poor risk/reward makes the setup weak.
- Treat news events as volatility/risk context, not guaranteed direction.
- Confidence above 80% requires strong multi-factor alignment and a clear invalidation level.

Local image feature scan:
{image_feature_text}

Economic calendar context for this pair:
{calendar_text}

Provide these sections:

1. MARKET REGIME
- Trend state: uptrend/downtrend/range/transition
- Volatility state: quiet/normal/expanding/news-sensitive
- Session or event-risk notes if visible or calendar-driven

2. MULTI-FACTOR TECHNICAL CASE
- Market structure: HH/HL, LH/LL, BOS, CHoCH, range boundaries
- Liquidity: equal highs/lows, stop zones, sweep/rejection areas
- Supply/demand: strongest zones and whether price already mitigated them
- Candle evidence: rejection, continuation, exhaustion, displacement
- Momentum quality: impulse vs corrective movement

3. ECONOMIC EVENT IMPACT
- List the relevant events that matter most for {pair}
- Explain whether upcoming/recent events increase breakout risk, fakeout risk, or favor waiting
- Give a volatility risk level: LOW/MEDIUM/HIGH

4. HIGHER-LEVEL PREDICTION
- Primary scenario for the next few candles and next few hours
- Alternative scenario and what would trigger it
- Expected path, not just direction

5. TRADE PLAN
- Bias: BUY/SELL/WAIT
- Entry zone
- Stop/invalidation level
- Take-profit targets
- Minimum risk/reward estimate
- Conditions that cancel the trade

6. QUALITY CONTROL
- Evidence score from 0-100
- Trade quality score from 0-100
- Main uncertainty

End with this exact machine-readable block:
FINAL VERDICT
DIRECTION: [UP/DOWN/CONSOLIDATION/NO_TRADE]
CONFIDENCE: [0-100]%
BIAS: [BUY/SELL/WAIT]
TRADE_QUALITY_SCORE: [0-100]
VOLATILITY_RISK: [LOW/MEDIUM/HIGH]
PRIMARY_TARGET: [price level or N/A]
INVALIDATION_LEVEL: [price level or N/A]
"""
        return prompt

    def _format_calendar_context(self, calendar_context):
        if not calendar_context:
            return "No economic calendar context was supplied."

        if isinstance(calendar_context, str):
            return calendar_context

        events = calendar_context.get('events', [])
        if not events:
            return calendar_context.get('summary', 'No relevant economic events found.')

        lines = [calendar_context.get('summary', 'Relevant economic events:')]
        for event in events:
            values = []
            for key in ('actual', 'forecast', 'previous'):
                if event.get(key):
                    values.append(f"{key}: {event[key]}")
            values_text = f" ({'; '.join(values)})" if values else ""
            time_text = event.get('time_utc')
            if hasattr(time_text, 'astimezone'):
                time_text = EconomicCalendar.format_event_time(time_text)

            lines.append(
                f"- {time_text} | {event.get('currency', 'N/A')} | "
                f"{event.get('impact', 'Unknown').upper()} | "
                f"{event.get('title', 'Untitled event')}{values_text}"
            )

        return '\n'.join(lines)

    def _format_image_features(self, image_features):
        if not image_features:
            return "No local image feature scan was available."

        props = image_features.get('image_properties', {})
        return (
            f"Detected {image_features.get('lines_detected', 0)} major line candidates, "
            f"{image_features.get('contours_count', 0)} contour/candle candidates, "
            f"edge density count {image_features.get('edge_count', 0)}, "
            f"image size {props.get('width', 'unknown')}x{props.get('height', 'unknown')}."
        )
    
    def parse_analysis_response(self, raw_analysis):
        """Parse Gemini response and extract structured data"""
        try:
            # This would parse the raw text response from Gemini
            # In production, you might want to structure this better
            result = {
                'raw_text': raw_analysis,
                'direction': self._extract_direction(raw_analysis),
                'confidence': self._extract_confidence(raw_analysis),
                'bias': self._extract_label(raw_analysis, 'BIAS', default='WAIT'),
                'trade_quality_score': self._extract_number(raw_analysis, 'TRADE_QUALITY_SCORE'),
                'volatility_risk': self._extract_label(raw_analysis, 'VOLATILITY_RISK', default='UNKNOWN'),
                'primary_target': self._extract_label(raw_analysis, 'PRIMARY_TARGET', default='N/A'),
                'invalidation_level': self._extract_label(raw_analysis, 'INVALIDATION_LEVEL', default='N/A'),
                'targets': self._extract_targets(raw_analysis),
                'support_levels': self._extract_levels(raw_analysis, 'SUPPORT'),
                'resistance_levels': self._extract_levels(raw_analysis, 'RESISTANCE'),
            }
            return result
        except Exception as e:
            logger.error(f"Error parsing analysis: {e}")
            return None
    
    def _extract_direction(self, text):
        """Extract predicted direction"""
        text_upper = text.upper()
        if 'DIRECTION: UP' in text_upper or 'BULLISH' in text_upper:
            return 'UP'
        elif 'DIRECTION: DOWN' in text_upper or 'BEARISH' in text_upper:
            return 'DOWN'
        elif 'DIRECTION: NO_TRADE' in text_upper or 'BIAS: WAIT' in text_upper:
            return 'NO_TRADE'
        else:
            return 'CONSOLIDATION'
    
    def _extract_confidence(self, text):
        """Extract confidence percentage"""
        import re
        matches = re.findall(r'CONFIDENCE[:\s]+(\d+)%', text.upper())
        if matches:
            return int(matches[0])
        return 0

    def _extract_number(self, text, label):
        import re
        matches = re.findall(rf'{label}[:\s]+(\d+)', text.upper())
        if matches:
            return int(matches[0])
        return 0

    def _extract_label(self, text, label, default=''):
        import re
        matches = re.findall(rf'{label}[:\s]+([^\n\r]+)', text.upper())
        if matches:
            return matches[-1].strip()
        return default
    
    def _extract_targets(self, text):
        """Extract price targets"""
        import re
        targets = re.findall(r'\d+\.\d+', text)
        return list(set(targets))[:5]  # Return unique targets, max 5
    
    def _extract_levels(self, text, level_type):
        """Extract support or resistance levels"""
        import re
        pattern = rf'{level_type}[:\s]+.*?(\d+\.\d+)'
        matches = re.findall(pattern, text.upper())
        return list(set(matches))
