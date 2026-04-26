## 2024-04-25 - Fix CSV/TSV Parser Regex and BOM Issues
**Mode:** Medic
**Learning:** The custom functional CSV/TSV parser incorrectly parsed TSV files because it constructed a `new RegExp("\\" + s)` where `s` is `\t`, which yielded `/\	/` (a literal tab instead of `\t`). It also failed if the file had a UTF-8 BOM (`\uFEFF`) at the beginning, as the BOM wasn't removed before regex matching the column headers.
**Action:** When building custom CSV parsers that use RegExp splitting dynamically, explicitly strip the BOM using `.replace(/^\uFEFF/,'')` at the beginning. Also, when dynamically constructing a regex that might contain escape sequences (like tabs), ensure `\t` is correctly formatted in the regex string via ternary or escaping (e.g., `new RegExp(s === '\t' ? '\\t...' : ...)`).
