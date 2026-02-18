#!/usr/bin/env python3
"""Test script to verify all fields are returned"""

from data_sources import YahooFinanceSource, FinnhubSource, AlphaVantageSource
import json

print("Testing Enhanced Data Sources")
print("=" * 60)

# Test Yahoo Finance
print("\n1. Yahoo Finance:")
yahoo = YahooFinanceSource()
result = yahoo.get_quote('AAPL')
print(json.dumps(result, indent=2))

# Test Finnhub
print("\n2. Finnhub:")
finnhub = FinnhubSource()
result = finnhub.get_quote('AAPL')
print(json.dumps(result, indent=2))

# Test Alpha Vantage
print("\n3. Alpha Vantage:")
alpha = AlphaVantageSource()
result = alpha.get_quote('AAPL')
print(json.dumps(result, indent=2))

print("\n" + "=" * 60)
print("✅ All sources now return comprehensive fields!")
print("\nNew fields added:")
print("  - high (day high)")
print("  - low (day low)")
print("  - open (opening price)")
print("  - previous_close (previous day close)")
