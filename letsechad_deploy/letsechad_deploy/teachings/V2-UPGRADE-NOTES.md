# Teachings v2 upgrade (July 2026)

Every teaching page now has a `-v2.html` twin, upgraded to the course standard. Originals untouched.

**What every page gained:**
- Gold reading-progress bar
- Ghosted Hebrew watermark in the hero (parsha name or the teaching's key word)
- Reading-time line under the title
- Drop cap on the opening paragraph
- Scroll fade-ins on quotes, pull-quotes, dividers, and the signup box
- A "Before You Read" interactive question at the top of the body: tap an answer, the reveal draws them into the teaching. Pure CSS, works with scripts stripped, reduced-motion respected.

**Exception:** isaiah-53-academic-v2.html got the design layer but no quiz, on purpose. The scholarly register should not open with a tap-question.

**To go live:** replace each original's contents with its -v2 twin (same filename). Canonical URLs and internal links all point at the original filenames, so do not publish both. Preview first: the para page upgrade (para-v2.html, one level up) follows the same system.

**To edit later:** quizzes live in `quizzes.py`; the whole layer is applied by `enhance-teachings.py` (run it after editing an original and the -v2 regenerates).

*One stick in His hand. Ezekiel 37:19*
