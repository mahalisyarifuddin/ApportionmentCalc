
## 2025-02-18 - [Fix CSV Parsing for International Formats]
**Mode:** Medic
**Learning:** The CSV parsing logic used `replace(/[^\d.]/g, '')` which preserved dots, causing `1.000` (Indonesian thousand) to be parsed as `1`. Since the app uses integer votes (rounding in UI), robust parsing should strictly enforce integers by stripping all non-digits (`/\D/g`) to support all thousands separators.
**Action:** When implementing CSV parsers for international audiences, assume integer inputs unless decimals are explicitly required, and strip non-digit characters to handle `.` and `,` thousands separators correctly.

## 2024-05-23 - Shadowed Globals Create Confusion
**Mode:** Medic
**Learning:** The codebase shadowed the deprecated global `escape` function with a local variable of the same name. This led to initial misdiagnosis of a bug (assuming deprecated behavior) and could lead to silent failures if the local definition were removed.
**Action:** Avoid using standard global function names for local variables. Refactor them into class methods with distinct names (e.g., `escapeHtml`) to improve clarity and safety.

## 2025-10-26 - Safe Retrofit of Row Headers
**Mode:** Palette
**Learning:** Changing `<td>` to `<th>` for row headers to improve accessibility can break existing CSS that targets `th` elements (often used for column headers).
**Action:** Use `role="rowheader"` on `<td>` elements instead of changing the tag. This provides the same semantic value to assistive technology without risking style regressions in legacy codebases.
