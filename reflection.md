# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game launched and looked normal, but quickly revealed several serious issues during play.

**Bug 1 — Hints were backwards**
When I guessed a number that was too high, the hint said "Go HIGHER!" with an upward arrow. I expected it to say "Go LOWER!" to help me narrow in on the secret. Instead the hint actively pointed me in the wrong direction, making the game feel unwinnable.

**Bug 2 — The game became unwinnable on even-numbered attempts**
On my second guess (and every even-numbered attempt after), even typing the exact correct number would not register as a win. I expected a correct guess to always win. The bug was that the code was converting the secret number to a string on even attempts, so `50 == "50"` evaluated to `False` in Python.

**Bug 3 — Score was always 10 points lower than expected**
When I won on my first attempt, I expected to score 90 points (100 - 10×1). Instead I received 80 points. The formula used `attempt_number + 1` instead of `attempt_number`, silently penalizing every win by an extra 10 points.

**Bug 4 — Hard mode was easier than Normal mode**
Hard mode had a number range of 1–50, while Normal mode used 1–100. I expected Hard to be harder (a larger range). Hard mode gave me fewer guesses *and* a smaller range, which actually made it easier to find the number.

**Bug 5 — "New Game" ignored the selected difficulty**
After clicking New Game while playing on Easy difficulty, the secret number was chosen from 1–100 instead of 1–20. I expected the new game to respect my difficulty selection. The code had `random.randint(1, 100)` hardcoded instead of using the difficulty range variables.

---

## 2. How did you use AI as a teammate?

I used Claude Code as my primary AI tool throughout this project. I shared the full codebase with it using the `#file:app.py` context and described the strange behavior I was seeing during play.

One example of a correct suggestion: Claude Code identified the secret-number type conversion bug, where the code cast the secret to a string on even-numbered attempts (`str(st.session_state.secret)`). It explained that `50 == "50"` evaluates to `False` in Python, which is why correct guesses failed every other attempt. I verified this by opening the Developer Debug Info panel, noting the secret was an integer, then watching my correct guess on attempt 2 fail — exactly as predicted.

One example of a misleading suggestion: Claude Code also flagged the `TypeError` fallback branch inside `check_guess()` (lines 41–47) as still having backwards hints and suggested fixing those too. In practice, once the upstream string conversion was removed, that branch can never be reached — so the suggestion was technically accurate but unnecessary. I verified by tracing through the call path and confirming the `TypeError` block is dead code after the fix.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed by reproducing the exact failure condition before the fix and confirming it no longer happened after. For each fix I had a specific test in mind rather than just "does it feel right."

For the even-attempt bug, I opened the Developer Debug Info panel to read the secret number, then deliberately typed that exact number on attempt 2. Before the fix, the game said "Too Low" or "Too High" even though my guess matched. After removing the string conversion, the game correctly showed "Correct!" and launched the balloon animation on attempt.

Claude Code helped me understand *why* the test had to happen on attempt 2 specifically — it explained that Python's `%` operator made the bug deterministic (even attempts → string, odd attempts → int), so I knew exactly which attempt to target rather than guessing randomly.

---

## 4. What did you learn about Streamlit and state?

Every time you interact with a Streamlit app — clicking a button, typing in a box, changing a dropdown — the entire Python script reruns from top to bottom. Think of it like refreshing a webpage, except the script executes again completely. Without session state, every variable would reset to its starting value on each rerun, so your score and attempt count would disappear the moment you clicked anything.

`st.session_state` is a dictionary that survives across reruns. It's like a notepad that Streamlit holds onto between script executions. You store values in it (like `st.session_state.score = 0`) and read them back on the next rerun, which is how the game remembers your progress. This is also why the secret-number bug was so subtle — the type conversion happened during a rerun, not at startup, and only on specific attempt counts stored in session state.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse: always look for a built-in debug panel or expose hidden state before trying to guess at a bug. The "Developer Debug Info" expander in this app let me see the secret number, attempt count, and score in real time. That made bugs like the wrong range on New Game immediately obvious. I could just click New Game on Easy and watch the secret jump to 73, confirming the hardcoded range without any guesswork.

Next time I work with AI on a coding task, I would run the app and collect specific observed behavior *before* asking AI to explain the code. This time I described what I saw while playing and AI pinpointed the causes quickly — but I think if I had asked "what could go wrong?" without that context first, the answers would have been much more generic and harder to act on.

This project changed how I think about AI-generated code: it can produce code that looks intentional and well-structured but contains subtle logic errors that only surface under specific conditions. Treating AI output as a first draft that needs active verification, not a finished product, is the right default.
