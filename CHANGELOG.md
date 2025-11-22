# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-11-22

### Fixed
- Unit tests now properly match actual implementation
- Fixed `is_valid_image_size()` tests to use PIL Image objects
- Fixed `extract_confidence_score()` tests to match regex-based extraction
- Fixed `extract_description()` tests to match actual parsing logic
- All tests now pass (12 passed, 1 skipped)

## [0.1.0] - 2025-11-22

### Added
- First release of crawl4logo
- Logo extraction from company websites
- Support for multiple search strategies
- Comprehensive test coverage
