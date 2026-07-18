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
