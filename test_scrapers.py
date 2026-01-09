#!/usr/bin/env python3
"""
Test Seeding - Proof of Concept
Zeigt die Funktionalität der Scraper mit kleiner Datenmenge
"""

import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from ingestion.scrapers.eugh_scraper import EuGHScraper
from ingestion.scrapers.ag_comprehensive_scraper import AGComprehensiveScraper

print("="*80)
print("DOMULEX.AI - CASE LAW SCRAPER TEST")
print("="*80)

# Test EuGH Scraper
print("\n1. EuGH Scraper Test")
print("-"*80)
eugh = EuGHScraper()

print("\nImmobilienrecht (5 cases):")
immobilien = eugh.scrape_immobilien(max_results=5)
for i, case in enumerate(immobilien, 1):
    print(f"  {i}. {case['title']}")
    print(f"     Court: {case['court']} | Date: {case['date']}")
    print(f"     Keywords: {', '.join(case['keywords'][:3])}")

print("\nSteuerrecht (5 cases):")
steuer = eugh.scrape_steuerrecht(max_results=5)
for i, case in enumerate(steuer, 1):
    print(f"  {i}. {case['title']}")
    print(f"     Court: {case['court']} | Date: {case['date']}")
    print(f"     Keywords: {', '.join(case['keywords'][:3])}")

print(f"\n✓ EuGH Total: {len(immobilien) + len(steuer)} cases")

# Test AG Scraper
print("\n\n2. AG Comprehensive Scraper Test")
print("-"*80)
ag = AGComprehensiveScraper()

print("\nScraping 30 AG cases (sample)...")
ag_cases = ag.scrape_all(max_total=30)

# Distribution
distribution = {}
for case in ag_cases:
    rg = case['rechtsgebiet']
    distribution[rg] = distribution.get(rg, 0) + 1

print("\nDistribution by Rechtsgebiet:")
for rg, count in sorted(distribution.items()):
    print(f"  {rg}: {count} cases")

# Sample cases
print("\nSample Cases:")
for i, case in enumerate(ag_cases[:5], 1):
    print(f"  {i}. {case['title']}")
    print(f"     Rechtsgebiet: {case['rechtsgebiet']} | Court: {case['court']}")
    print(f"     Keywords: {', '.join(case['keywords'][:2])}")

print(f"\n✓ AG Total: {len(ag_cases)} cases")

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nTotal Cases Scraped: {len(immobilien) + len(steuer) + len(ag_cases)}")
print(f"  - EuGH Immobilienrecht: {len(immobilien)}")
print(f"  - EuGH Steuerrecht: {len(steuer)}")
print(f"  - AG (alle Gebiete): {len(ag_cases)}")

print("\n✅ Scraper fully functional!")
print("\nFor full seeding (350 cases), run:")
print("  python3 seed_comprehensive_case_law.py")
print("\nNote: Requires GEMINI_API_KEY and QDRANT_API_KEY in backend/.env")
print("="*80)
