import numpy as np
import cv2
from utils.logger import get_logger

logger = get_logger(__name__)

class TechnicalAnalyzer:
    """Perform additional technical analysis on chart images"""
    
    def __init__(self):
        pass
    
    def analyze_image_features(self, image_path):
        """Analyze image features for technical clues"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 100, 200)
            
            # Line detection (for support/resistance lines)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=100, maxLineGap=10)
            
            # Contour detection (for candlesticks)
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            analysis = {
                'edge_count': len(edges[edges > 0]),
                'lines_detected': len(lines) if lines is not None else 0,
                'contours_count': len(contours),
                'image_properties': {
                    'width': image.shape[1],
                    'height': image.shape[0],
                    'channels': image.shape[2] if len(image.shape) > 2 else 1
                }
            }
            
            logger.info(f"Image analysis complete: {analysis['lines_detected']} lines, {analysis['contours_count']} contours detected")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing image features: {e}")
            return None
    
    def detect_candle_patterns(self, close_prices, high_prices, low_prices, open_prices=None):
        """Detect candlestick patterns"""
        patterns_found = []
        
        if len(close_prices) < 2:
            return patterns_found
        
        # If no open prices provided, use close prices as approximation
        if open_prices is None:
            open_prices = close_prices
        
        try:
            # Get last few candles
            for i in range(len(close_prices) - 1, max(len(close_prices) - 10, 0), -1):
                # Pinbar (doesn't need open_prices)
                if self.is_pinbar(close_prices, high_prices, low_prices, i):
                    patterns_found.append('Pinbar')
                
                # Doji (doesn't need open_prices)
                if self.is_doji(close_prices, high_prices, low_prices, i):
                    patterns_found.append('Doji')
                
                # Hammer (doesn't need open_prices)
                if self.is_hammer(close_prices, high_prices, low_prices, i):
                    patterns_found.append('Hammer')
        
        except Exception as e:
            logger.error(f"Error detecting candle patterns: {e}")
        
        return list(set(patterns_found))  # Return unique patterns
    
    @staticmethod
    def is_pinbar(close, high, low, index):
        """Detect pinbar (rejection wick) pattern"""
        try:
            if index < 1:
                return False
            
            body_high = close[index]
            body_low = close[index]
            upper_wick = high[index] - body_high
            lower_wick = body_low - low[index]
            
            total_range = high[index] - low[index]
            if total_range == 0:
                return False
            
            # If wick is 2x+ the body size
            wick_ratio = max(upper_wick, lower_wick) / (abs(close[index] - close[index - 1]) + 1e-10)
            return wick_ratio > 2
        except:
            return False
    
    @staticmethod
    def is_doji(close, high, low, index):
        """Detect doji pattern (similar body is small)"""
        try:
            if index < 1:
                return False
            
            body_range = abs(close[index] - close[index - 1])
            total_range = high[index] - low[index]
            
            if total_range == 0:
                return False
            
            body_ratio = body_range / total_range
            return body_ratio < 0.1  # Very small body
        except:
            return False
    
    @staticmethod
    def is_hammer(close, high, low, index):
        """Detect hammer pattern"""
        try:
            if index < 1:
                return False
            
            body_low = low[index]
            body_high = high[index]
            body_size = abs(close[index] - close[index - 1])
            lower_wick = body_low - low[index]
            upper_wick = high[index] - body_high
            
            # Hammer: small body, long lower wick, small upper wick
            if body_size == 0:
                return False
            
            return lower_wick > body_size and upper_wick < body_size
        except:
            return False
    
    def calculate_support_resistance(self, prices, lookback=20):
        """Calculate support and resistance levels"""
        try:
            support_levels = []
            resistance_levels = []
            
            # Simple approach: find local minima and maxima
            for i in range(lookback, len(prices) - lookback):
                # Support: local minimum
                if prices[i] < prices[i-lookback:i].min() and prices[i] < prices[i+1:i+lookback+1].min():
                    support_levels.append(round(prices[i], 4))
                
                # Resistance: local maximum
                if prices[i] > prices[i-lookback:i].max() and prices[i] > prices[i+1:i+lookback+1].max():
                    resistance_levels.append(round(prices[i], 4))
            
            return {
                'support': list(set(support_levels)),  # Remove duplicates
                'resistance': list(set(resistance_levels))
            }
        except Exception as e:
            logger.error(f"Error calculating support/resistance: {e}")
            return {'support': [], 'resistance': []}
    
    def detect_supply_demand_zones(self, prices, high_prices, low_prices, lookback=50):
        """Detect supply and demand zones"""
        try:
            zones = {
                'supply': [],  # Zones where price rejected downward
                'demand': []   # Zones where price rejected upward
            }
            
            # Supply zone: area where price bounced down multiple times
            # Demand zone: area where price bounced up multiple times
            
            # This is a simplified version - in production, would analyze actual rejection patterns
            supply_peaks = []
            demand_troughs = []
            
            for i in range(lookback, len(prices) - lookback):
                # Potential supply zone
                if high_prices[i] > high_prices[i-lookback:i].max():
                    supply_peaks.append({
                        'level': round(high_prices[i], 4),
                        'strength': 1
                    })
                
                # Potential demand zone
                if low_prices[i] < low_prices[i-lookback:i].min():
                    demand_troughs.append({
                        'level': round(low_prices[i], 4),
                        'strength': 1
                    })
            
            zones['supply'] = supply_peaks[-5:] if supply_peaks else []
            zones['demand'] = demand_troughs[-5:] if demand_troughs else []
            
            return zones
        except Exception as e:
            logger.error(f"Error detecting supply/demand zones: {e}")
            return {'supply': [], 'demand': []}
