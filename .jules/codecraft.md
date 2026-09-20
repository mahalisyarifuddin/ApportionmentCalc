## 2025-02-24 - Fix missing value update on Ctrl+Enter
**Mode:** Medic
**Learning:** In browser environments, triggering a programmatic save action via keyboard shortcuts (like Ctrl+Enter) does not automatically commit changes from the currently focused input because the `change` event is only fired upon losing focus. JSDOM behaves similarly, but doesn't auto-fire the change event synchronously on blur like real browsers do.
**Action:** When implementing global keyboard shortcuts that trigger saving or calculation, use `document.activeElement?.blur()` immediately prior to the core logic execution to ensure the active input successfully commits its value to the internal state.

## 2025-02-24 - Fix number parsing logic in UI inputs
**Mode:** Medic
**Learning:** The `parseInt` function incorrectly parses floating-point values from `<input type="number">` fields and silently truncates scientific notation (`parseInt("1e5")` evaluates to `1`).
**Action:** Always prefer `Math.round(+value)` for correctly coercing string inputs into rounded numeric values without breaking decimal or scientific notations.

## 2025-02-24 - Fix CSV delimiter detection ignoring quotes
**Mode:** Medic
**Learning:** The previous implementation of the CSV parser in `ApportionmentCalc.html` detected delimiters blindly counting splitting characters on the first line `['\t',';',','].reduce((a,b)=>l[0].split(a).length>l[0].split(b).length?a:b)`. This failed if a quoted column contains a comma, because commas inside strings would artificially inflate the split count for `,`, making it think `,` is the delimiter instead of `\t` or `;`.
**Action:** Use a regex-aware split that ignores delimiters inside quotes for delimiter detection just like the actual parsing logic does.

## 2025-02-24 - Optimize Sainte-Laguë allocation algorithm inner loop
**Mode:** Bolt
**Learning:** In tight inner execution paths (such as calculating the max quotient for each seat iteratively in Sainte-Laguë), using higher-order functions like `Array.prototype.reduce()` mapped to a closure IIFE introduces significant execution overhead and garbage collection pauses compared to standard native loops.
**Action:** When working in hot execution paths that run thousands of times synchronously, convert abstraction-heavy iterators (`reduce`, `map`, `filter`) into clean inline `for` loops to drastically improve performance (achieved up to ~3.45x speedup for high seat counts).

## 2025-02-24 - Fix CSV parser number identification throwing error for empty values
**Mode:** Medic
**Learning:** In the CSV parser, `c=>/^\d+$/.test(c?.replace(/[.,]/g,'').trim())` was used. While the optional chaining (`c?.replace(...)`) protects against `replace` being called on undefined/null, if it *does* evaluate to undefined, calling `.trim()` on it immediately throws a `TypeError`. This can happen with malformed rows. Additionally, it fails to identify space-separated numbers (e.g. `10 000`) because `.trim()` only targets leading/trailing spaces.
**Action:** Move whitespace removal into the regex replace itself: `c?.replace(/[.,\s]/g,'')`. This eliminates the `.trim()` call, safely evaluates to undefined if `c` is null/undefined (causing `.test(undefined)` to safely return `false`), and correctly strips internal spaces.

## 2025-02-24 - Enhance tabular scannability and Excel export compatibility
**Mode:** Palette
**Learning:** In tables displaying vote shares, dynamic decimal lengths (e.g., `10%` vs `12.50%`) break vertical alignment, making it harder to scan figures. Additionally, exporting CSVs with special characters (like "Sainte-Laguë") without a Byte Order Mark (\uFEFF) causes mangled encoding in Microsoft Excel, especially in locales where Excel uses semicolon delimiters instead of commas.
**Action:** Use `minimumFractionDigits` in `Intl.NumberFormat` to force uniform decimal widths for percentages. Always prepend `\uFEFF` to the Blob payload when creating a text/csv file export to ensure correct UTF-8 parsing in Excel. Use CSS opacity rules (like `.neutral { opacity: 0.4; }`) to de-emphasize zero differences, making true variations stand out.
## 2026-09-05 - ApportionmentCalc Refactoring
**Mode:** Razor
**Learning:** The `this.data` object generated in `computeAllocation` already caches values like `total`, which can be leveraged in subsequent methods like `copy` and `export` to avoid redundant O(N) traversal loops over the results array.
**Action:** When working on standalone HTML apps with centralized state mutations, check the main computation functions first to see if necessary aggregates are already available in the output object before manually recalculating them.

## 2026-09-06 - Validating Inline JavaScript Syntax
**Mode:** Razor
**Learning:** `node -c` (Syntax Check) fails when run directly against `.html` files (`ERR_UNKNOWN_FILE_EXTENSION`).
**Action:** To verify JavaScript syntax of inline `<script>` blocks within HTML files, extract the contents to temporary files in the `verification/` directory and run `node -c` on them.
