from datetime import datetime, timedelta, timezone

import requests

import config
from utils.logger import get_logger

logger = get_logger(__name__)


class EconomicCalendar:
    """Fetch and filter economic events relevant to a forex pair."""

    IST_TIMEZONE = timezone(timedelta(hours=5, minutes=30), name='IST')

    CURRENCY_COUNTRIES = {
        'USD': {'USD', 'US', 'United States'},
        'EUR': {'EUR', 'EU', 'Euro Zone', 'Eurozone'},
        'GBP': {'GBP', 'UK', 'United Kingdom'},
        'JPY': {'JPY', 'JP', 'Japan'},
        'CHF': {'CHF', 'CH', 'Switzerland'},
        'AUD': {'AUD', 'AU', 'Australia'},
        'NZD': {'NZD', 'NZ', 'New Zealand'},
        'CAD': {'CAD', 'CA', 'Canada'},
        'XAU': {'USD', 'US', 'United States'},
    }

    IMPACT_WEIGHT = {
        'high': 3,
        'medium': 2,
        'low': 1,
        'holiday': 0,
    }

    def __init__(self, url=None, timeout=None):
        self.url = url or config.ECONOMIC_CALENDAR_URL
        self.timeout = timeout or config.ECONOMIC_CALENDAR_TIMEOUT

    def get_events_for_pair(self, pair):
        if not config.ECONOMIC_CALENDAR_ENABLED:
            return {
                'enabled': False,
                'events': [],
                'summary': 'Economic calendar is disabled in configuration.',
                'source': self.url,
            }

        currencies = self._pair_currencies(pair)

        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            raw_events = response.json()
        except Exception as exc:
            logger.warning(f"Economic calendar fetch failed: {exc}")
            return {
                'enabled': True,
                'events': [],
                'summary': f'Live economic calendar unavailable: {exc}',
                'source': self.url,
            }

        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=config.ECONOMIC_CALENDAR_LOOKBACK_HOURS)
        end = now + timedelta(hours=config.ECONOMIC_CALENDAR_LOOKAHEAD_HOURS)

        events = []
        for event in raw_events:
            normalized = self._normalize_event(event)
            if not normalized:
                continue

            if normalized['time_utc'] < start or normalized['time_utc'] > end:
                continue

            if not self._is_relevant_event(normalized, currencies):
                continue

            events.append(normalized)

        events.sort(
            key=lambda item: (
                -self.IMPACT_WEIGHT.get(item['impact'].lower(), 0),
                abs((item['time_utc'] - now).total_seconds()),
            )
        )
        events = events[:config.ECONOMIC_CALENDAR_MAX_EVENTS]

        return {
            'enabled': True,
            'events': events,
            'summary': self._build_summary(pair, currencies, events),
            'source': self.url,
        }

    def format_for_prompt(self, calendar_context):
        events = calendar_context.get('events', [])
        if not events:
            return calendar_context.get('summary', 'No relevant economic events found.')

        lines = [
            calendar_context.get('summary', 'Relevant economic events:'),
            'Use these events as volatility and directional-risk context; do not invent actual/forecast values.',
        ]
        for event in events:
            values = []
            for key in ('actual', 'forecast', 'previous'):
                if event.get(key):
                    values.append(f"{key}: {event[key]}")

            value_text = f" ({'; '.join(values)})" if values else ''
            lines.append(
                f"- {self.format_event_time(event['time_utc'])} | "
                f"{event['currency']} | {event['impact'].upper()} | "
                f"{event['title']}{value_text}"
            )

        return '\n'.join(lines)

    def _pair_currencies(self, pair):
        pair = pair.upper().replace('/', '').replace('-', '')
        if pair.startswith('XAU'):
            return ['XAU', 'USD']
        if len(pair) >= 6:
            return [pair[:3], pair[3:6]]
        return [pair]

    def _normalize_event(self, event):
        event_time = self._parse_datetime(
            event.get('date') or event.get('datetime') or event.get('time')
        )
        if not event_time:
            return None

        impact = str(event.get('impact') or event.get('importance') or '').strip() or 'Unknown'
        currency = str(event.get('country') or event.get('currency') or '').strip()

        return {
            'title': str(event.get('title') or event.get('event') or 'Untitled event').strip(),
            'currency': currency,
            'impact': impact,
            'time_utc': event_time,
            'actual': self._clean_value(event.get('actual')),
            'forecast': self._clean_value(event.get('forecast')),
            'previous': self._clean_value(event.get('previous')),
        }

    def _parse_datetime(self, value):
        if not value:
            return None

        text = str(value).strip().replace('Z', '+00:00')
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%m-%d-%Y %H:%M'):
                try:
                    parsed = datetime.strptime(text, fmt)
                    break
                except ValueError:
                    parsed = None
            if parsed is None:
                return None

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    def _is_relevant_event(self, event, currencies):
        event_currency = event['currency']
        relevant_countries = set()
        for currency in currencies:
            relevant_countries.update(self.CURRENCY_COUNTRIES.get(currency, {currency}))

        return event_currency in relevant_countries

    def _build_summary(self, pair, currencies, events):
        if not events:
            return f'No relevant calendar events found for {pair} currencies: {", ".join(currencies)}.'

        high_count = sum(1 for event in events if event['impact'].lower() == 'high')
        medium_count = sum(1 for event in events if event['impact'].lower() == 'medium')
        return (
            f'Found {len(events)} relevant economic events for {pair} '
            f'({high_count} high impact, {medium_count} medium impact).'
        )

    @classmethod
    def format_event_time(cls, event_time):
        if not hasattr(event_time, 'astimezone'):
            return str(event_time)
        return event_time.astimezone(cls.IST_TIMEZONE).strftime('%Y-%m-%d %H:%M IST')

    @staticmethod
    def _clean_value(value):
        if value is None:
            return ''
        return str(value).strip()
