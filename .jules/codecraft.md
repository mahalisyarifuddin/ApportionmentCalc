
## 2025-02-18 - [Fix CSV Parsing for International Formats]
**Mode:** Medic
**Learning:** The CSV parsing logic used `replace(/[^\d.]/g, '')` which preserved dots, causing `1.000` (Indonesian thousand) to be parsed as `1`. Since the app uses integer votes (rounding in UI), robust parsing should strictly enforce integers by stripping all non-digits (`/\D/g`) to support all thousands separators.
**Action:** When implementing CSV parsers for international audiences, assume integer inputs unless decimals are explicitly required, and strip non-digit characters to handle `.` and `,` thousands separators correctly.
