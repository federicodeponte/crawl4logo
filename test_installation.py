#!/usr/bin/env python3
"""Test script to verify crawl4logo installation"""

print("=" * 60)
print("Testing crawl4logo installation")
print("=" * 60)

# Test 1: Import the package
print("\n1. Testing package import...")
try:
    from fede_crawl4ai import LogoCrawler
    print("   ✅ Package imported successfully")
except ImportError as e:
    print(f"   ❌ Failed to import package: {e}")
    exit(1)

# Test 2: Check dependencies
print("\n2. Checking core dependencies...")
dependencies = [
    ("aiohttp", "aiohttp"),
    ("beautifulsoup4", "bs4"),
    ("Pillow", "PIL"),
    ("pydantic", "pydantic"),
    ("rich", "rich"),
    ("cairosvg", "cairosvg"),
    ("opencv-python", "cv2"),
    ("numpy", "numpy"),
]

all_deps_ok = True
for pkg_name, import_name in dependencies:
    try:
        __import__(import_name)
        print(f"   ✅ {pkg_name}")
    except ImportError:
        print(f"   ❌ {pkg_name} - not found")
        all_deps_ok = False

if not all_deps_ok:
    print("\n⚠️  Some dependencies are missing")
    exit(1)

# Test 3: Test LogoCrawler initialization (should fail without API key)
print("\n3. Testing LogoCrawler initialization...")
try:
    crawler = LogoCrawler(api_key=None)
    print("   ❌ Expected ValueError but initialization succeeded")
    exit(1)
except ValueError as e:
    if "API key is required" in str(e):
        print("   ✅ Correctly requires API key")
    else:
        print(f"   ❌ Unexpected error: {e}")
        exit(1)
except Exception as e:
    print(f"   ❌ Unexpected error: {e}")
    exit(1)

# Test 4: Test with dummy API key (just to verify initialization works)
print("\n4. Testing LogoCrawler initialization with dummy API key...")
try:
    crawler = LogoCrawler(api_key="dummy-key-for-testing-installation")
    print("   ✅ LogoCrawler initialized successfully")
    print(f"   - Min width: {crawler.min_width}")
    print(f"   - Min height: {crawler.min_height}")
    print(f"   - Cache enabled: {crawler.image_cache is not None}")
except Exception as e:
    print(f"   ❌ Failed to initialize: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✅ All installation tests passed!")
print("=" * 60)
print("\nNote: To use the crawler, you need a valid OpenAI API key.")
print("Get your key from: https://platform.openai.com/")
print("\nUsage:")
print("  crawler = LogoCrawler(api_key='your-openai-key')")
print("  results = await crawler.crawl_website('https://example.com')")
print("=" * 60)
