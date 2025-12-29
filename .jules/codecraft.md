## 2024-05-22 - [Persistence Implementation]
**Mode:** Palette
**Learning:** When implementing `localStorage` persistence for lists with IDs, ensuring the `nextIndex` or ID counter is recalculated from the loaded data (e.g., `Math.max(...ids) + 1`) is critical to prevent ID collisions when new items are added subsequently.
**Action:** Always verify ID generation logic when restoring state from external storage.
