# CodeCraft Journal

## 2025-02-18 - Initialization
**Mode:** General
**Learning:** Initialized journal system.
**Action:** Use this file to record critical learnings as per instructions.

## 2026-01-13 - Hare Quota Threshold Logic
**Mode:** Medic
**Learning:** Calculating Hare Quota using total votes while simultaneously filtering parties by threshold leads to unallocated seats, as the quota becomes too high for the remaining eligible vote pool.
**Action:** When implementing apportionment with thresholds, ensure the quota basis aligns with the eligible party set (recalculate quota from passed votes).

## 2026-02-05 - Initialization Order Dependency
**Mode:** Medic
**Learning:** `ApportionmentCalc.lang()` calls `renderParties()`, requiring `this.parties` to be initialized beforehand. Adding logic that delays `this.parties` initialization (like loading state) can cause crashes if placed after `lang()`.
**Action:** Ensure `this.parties` is initialized (at least to an empty array) immediately in the constructor before calling any setup methods that might trigger rendering.
