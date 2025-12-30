## 2024-01-01 - [Accessibility Labels in Dynamic Lists]
**Mode:** Palette
**Learning:** In dynamic lists generated via `innerHTML`, repeated inputs (like "Party Name") lack unique accessible names, confusing screen reader users. Using the row index in `aria-label` (e.g., "Party Name 1") solves this without requiring complex state management.
**Action:** When generating lists of form controls, always append a unique identifier (index or ID) to the `aria-label` to provide context.
