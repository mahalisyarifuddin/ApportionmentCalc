## 2025-02-24 - Fix missing value update on Ctrl+Enter
**Mode:** Medic
**Learning:** In browser environments, triggering a programmatic save action via keyboard shortcuts (like Ctrl+Enter) does not automatically commit changes from the currently focused input because the `change` event is only fired upon losing focus. JSDOM behaves similarly, but doesn't auto-fire the change event synchronously on blur like real browsers do.
**Action:** When implementing global keyboard shortcuts that trigger saving or calculation, use `document.activeElement?.blur()` immediately prior to the core logic execution to ensure the active input successfully commits its value to the internal state.
