#!/usr/bin/env python3
"""Test crawl4logo on multiple companies"""

import asyncio
import json
from datetime import datetime
from fede_crawl4ai import LogoCrawler

# List of companies to test
COMPANIES = [
    "https://scaile.tech",
    "https://anthropic.com",
    "https://stripe.com",
    "https://shopify.com",
    "https://airbnb.com",
    "https://spotify.com",
    "https://netflix.com",
    "https://notion.so",
    "https://figma.com",
    "https://vercel.com",
    "https://supabase.com",
]

async def test_single_company(crawler, url, index, total):
    """Test a single company website"""
    print(f"\n{'=' * 80}")
    print(f"[{index}/{total}] Testing: {url}")
    print('=' * 80)

    try:
        # Crawl the website
        results = await crawler.crawl_website(url)

        if not results:
            print(f"❌ No logos found for {url}")
            return {
                "url": url,
                "status": "no_logos_found",
                "logos": [],
                "error": None
            }

        # Process results
        print(f"\n✅ Found {len(results)} logo(s) for {url}")

        processed_results = []
        for i, result in enumerate(results[:3], 1):  # Show top 3
            logo_data = {
                "rank": i,
                "image_url": result.url,
                "confidence": round(result.confidence, 2),
                "rank_score": round(result.rank_score, 2),
                "description": result.description,
                "is_header": result.is_header,
                "page_url": result.page_url,
            }
            processed_results.append(logo_data)

            print(f"\n  Logo #{i}:")
            print(f"    Image URL: {result.url}")
            print(f"    Confidence: {result.confidence:.2f}")
            print(f"    Rank Score: {result.rank_score:.2f}")
            print(f"    Location: {'Header/Navigation' if result.is_header else 'Main Content'}")
            print(f"    Description: {result.description}")

        return {
            "url": url,
            "status": "success",
            "total_logos": len(results),
            "top_logos": processed_results,
            "error": None
        }

    except Exception as e:
        print(f"\n❌ Error crawling {url}: {str(e)}")
        return {
            "url": url,
            "status": "error",
            "logos": [],
            "error": str(e)
        }

async def main():
    """Main test function"""
    print("=" * 80)
    print("CRAWL4LOGO - Multi-Company Logo Detection Test")
    print("=" * 80)
    print(f"Testing {len(COMPANIES)} companies...")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Initialize crawler with API key
    api_key = "***REMOVED***"

    try:
        crawler = LogoCrawler(api_key=api_key)
        print("✅ Crawler initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize crawler: {e}")
        return

    # Test each company
    all_results = []
    for i, company_url in enumerate(COMPANIES, 1):
        result = await test_single_company(crawler, company_url, i, len(COMPANIES))
        all_results.append(result)

        # Small delay between requests to be respectful
        if i < len(COMPANIES):
            await asyncio.sleep(2)

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    successful = sum(1 for r in all_results if r["status"] == "success")
    failed = sum(1 for r in all_results if r["status"] == "error")
    no_logos = sum(1 for r in all_results if r["status"] == "no_logos_found")

    print(f"\nTotal companies tested: {len(COMPANIES)}")
    print(f"✅ Successful: {successful}")
    print(f"⚠️  No logos found: {no_logos}")
    print(f"❌ Failed: {failed}")

    # Show successful results
    if successful > 0:
        print("\n" + "-" * 80)
        print("SUCCESSFUL DETECTIONS:")
        print("-" * 80)
        for result in all_results:
            if result["status"] == "success" and result["top_logos"]:
                logo = result["top_logos"][0]  # Best match
                print(f"\n{result['url']}")
                print(f"  Best match: {logo['description']}")
                print(f"  Confidence: {logo['confidence']}")
                print(f"  Image: {logo['image_url'][:80]}...")

    # Save detailed results to JSON
    output_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_companies": len(COMPANIES),
            "summary": {
                "successful": successful,
                "no_logos": no_logos,
                "failed": failed
            },
            "results": all_results
        }, f, indent=2)

    print(f"\n📄 Detailed results saved to: {output_file}")
    print("\n" + "=" * 80)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
