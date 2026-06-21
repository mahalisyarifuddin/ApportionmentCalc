## 2025-02-24 - Fix missing value update on Ctrl+Enter
**Mode:** Medic
**Learning:** In browser environments, triggering a programmatic save action via keyboard shortcuts (like Ctrl+Enter) does not automatically commit changes from the currently focused input because the `change` event is only fired upon losing focus. JSDOM behaves similarly, but doesn't auto-fire the change event synchronously on blur like real browsers do.
**Action:** When implementing global keyboard shortcuts that trigger saving or calculation, use `document.activeElement?.blur()` immediately prior to the core logic execution to ensure the active input successfully commits its value to the internal state.

## 2025-02-24 - Fix number parsing logic in UI inputs
**Mode:** Medic
**Learning:** The `parseInt` function incorrectly parses floating-point values from `<input type="number">` fields and silently truncates scientific notation (`parseInt("1e5")` evaluates to `1`).
**Action:** Always prefer `Math.round(+value)` for correctly coercing string inputs into rounded numeric values without breaking decimal or scientific notations.
