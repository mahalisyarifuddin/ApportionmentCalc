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

## 2025-10-27 - [Reuse Localization Keys for Consistency]
**Mode:** Palette
**Learning:** When adding new UI elements that display standard concepts (like "Total Valid Votes"), check existing localization dictionaries first. Reusing keys (`totalVotes`, `thresholdVotes`) ensures consistency and avoids bloating the text object, even if the context is slightly different (e.g., input stats vs result stats).
**Action:** Always `grep` for potential existing string keys before adding new ones to the localization object.

## 2025-01-26 - [Avoid Integer Truncation in Threshold Displays]
**Mode:** Palette
**Learning:** Displaying calculated thresholds as integers (default `maximumFractionDigits: 0`) creates confusion when the actual threshold is fractional (e.g., 4.2 votes shown as 4). Users see their vote count equals the displayed threshold but still fail.
**Action:** Always specify `{ maximumFractionDigits: 2 }` (or higher) when formatting calculated boundary values like electoral thresholds to ensure transparency.

## 2025-10-27 - [Constructor Crash on Missing DOM Elements]
**Mode:** Medic
**Learning:** The `ApportionmentCalc.setup` method assigns event handlers by iterating over a predefined object (e.g., `copy: handler`) and setting `elements[id].onclick`. If the corresponding DOM element (e.g., `id="copy"`) is missing from the HTML, the `elements` Proxy returns `null`, causing `null.onclick` assignment to throw a `TypeError`. This halts the entire application initialization.
**Action:** When adding new UI handlers, ensure the HTML markup for the element exists *before* adding the handler to the logic. Alternatively, add null checks in the setup loop if optional elements are expected.

## 2025-05-21 - [Refactoring Inline Styles to CSS Classes]
**Mode:** Razor
**Learning:** In a single-file application with heavy DOM manipulation, inline styles in JavaScript template literals quickly become unreadable and hard to maintain. Refactoring them to utility classes with CSS variables (e.g., `style="--percentage:..."`) significantly improves code clarity and separation of concerns without adding build complexity.
**Action:** When working on legacy or single-file projects, prioritize extracting repeated inline styles into utility classes and use CSS variables for dynamic values.
