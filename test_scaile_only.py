#!/usr/bin/env python3
"""Quick test for scaile.tech logo detection"""

import asyncio
import json
from datetime import datetime
from fede_crawl4ai import LogoCrawler

async def main():
    """Test scaile.tech logo detection"""
    print("=" * 80)
    print("CRAWL4LOGO - Quick Test for scaile.tech")
    print("=" * 80)

    # Initialize crawler
    api_key = "***REMOVED***"

    try:
        crawler = LogoCrawler(api_key=api_key)
        print("✅ Crawler initialized\n")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return

    # Crawl scaile.tech
    url = "https://scaile.tech"
    print(f"🔍 Crawling {url}...")

    try:
        results = await crawler.crawl_website(url)

        print(f"\n✅ Found {len(results)} logo(s)\n")
        print("=" * 80)
        print("TOP LOGO DETECTIONS")
        print("=" * 80)

        for i, result in enumerate(results[:5], 1):
            print(f"\n#{i} - Rank Score: {result.rank_score:.2f} | Confidence: {result.confidence:.2f}")
            print(f"Location: {'Header/Nav' if result.is_header else 'Main Content'}")
            print(f"Description: {result.description}")
            print(f"Image URL: {result.url[:100]}...")
            print("-" * 80)

        # Save results
        output = {
            "company": url,
            "timestamp": datetime.now().isoformat(),
            "total_logos": len(results),
            "top_logos": [
                {
                    "rank": i,
                    "image_url": r.url,
                    "confidence": round(r.confidence, 2),
                    "rank_score": round(r.rank_score, 2),
                    "description": r.description,
                    "is_header": r.is_header,
                }
                for i, r in enumerate(results[:10], 1)
            ]
        }

        with open("scaile_results.json", "w") as f:
            json.dump(output, f, indent=2)

        print(f"\n📄 Results saved to: scaile_results.json")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
