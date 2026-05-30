## 2024-05-18 - CSV/TSV Parser Semicolon Support
**Mode:** Medic
**Learning:** The previous implementation hardcoded fallback behavior based merely on the length of commas vs tabs on the first line. By changing it to an array-reduce statement `['\t',';',','].reduce(...)`, we can support European semicolon-delimited CSV formats dynamically.
**Action:** Always test delimiter-detection code against an array of common delimiters when dealing with locale-specific string formatting.
