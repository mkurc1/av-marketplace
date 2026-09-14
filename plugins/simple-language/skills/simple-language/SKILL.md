---
name: simple-language
description: Use when writing any text a human will read — a reply, task summary, explanation, report, plan, spec, or README. Applies to short and technical answers too. Readers scan text before they read it, so the shape of the text matters as much as its content.
---

# Simple Language

## Overview

A correct answer the reader cannot scan is a bad answer.

Many readers scan text rather than read it line by line: people with dyslexia, non-native speakers, anyone reading on a phone or under time pressure. Dense text costs them the most. This skill defines the **shape** of text: the order of information, the length of a sentence, the words allowed. It does not lower the quality of the message. It does not decide tone or how much to say.

Write in the language the user writes in. The rules hold in every language.

## Reply Shape

Every reply has this order:

1. **First line = the answer.** A verdict, a status, or a number. Not context. Not what you did to get there.
2. **Details** as a list or a table.
3. **Caveats and next steps** last, in their own block.

A reply longer than one screen gets `##` headings. One topic per heading.

## Sentence Rules

| Rule | Instead of | Write |
|---|---|---|
| One sentence = one idea, up to ~15 words | "Since the portfolio never sells, the valuation never recovers, so the drawdown condition keeps the mode active longer than intended." | "The portfolio never sells. The valuation never recovers. Defensive mode stays active longer than intended." |
| Definition as its own sentence, not a parenthesis | "Win rate (the share of profitable trades) says nothing about profitability." | "Win rate says nothing about profitability. Win rate is the share of profitable trades." |
| Positive statement, not double negation | "It is not impossible that this fails." | "This may fail." |
| Active voice | "Selling was paused by the breaker." | "The breaker pauses selling." |
| The concrete name, not a pronoun | "That file does not handle it." | "`targets.py` does not handle it." |
| Numbers as digits | "four thousand eight hundred" | "4800" |
| One word for one thing | "breaker", then "fuse", then "the mechanism" | always "breaker" |

## Words

The message stays simple. No jargon, no invented words.

- **No invented words.** Do not coin verbs or blend languages: "bumps the row", "triggers the flow", "dispatches". Say what happens: "updates the row", "starts", "sends a message", "walks up the tree by `parent_id`".
- **No undefined jargon.** If a technical term is necessary, define it in one sentence at first use. Then use only that one term.
- **The code name, not a descriptive shorthand.** Instead of "the ancestor bump" write "the update of `updated_at` on watched comments higher in the tree". A field or method name in backticks is unambiguous. A shorthand is not.
- **Check in your head:** would someone outside this conversation understand the word without asking? If not, replace it with a plain word or a name from the code.
- The same rules apply to logs, plans, documentation, and test names. Jargon in a log comes back months later and nobody understands it.

## Lists

- A list item is **one short sentence** or a fragment. Not a compound sentence with an arrow in the middle.
- If an item needs a reason, split it: short item, then an indented line starting with "because".
- One list type per section. Bulleted **or** numbered, not both mixed.
- Numbered only when order matters.
- 3-7 items. More than that: split into sections.

## Emphasis

- **Bold on 1-2 words** that carry the meaning: the verdict, the number, the name. Not on a whole sentence.
- At most one bold per paragraph or list item. When everything is bold, nothing stands out.
- File names, functions, and values in `backticks`. They give the eye an anchor.
- A prose paragraph is at most 3 lines. Longer: turn it into a list.

## Documents

Plans, specs, reports, and READMEs written by the agent follow the same shape. A document is a long reply.

- **First paragraph = the outcome.** What the document decides, or what the reader will have after following it. Before any heading.
- **Decision before justification.** State the choice in one sentence. Then the reasons, as a list.
- **One topic per section.** A section that needs a second topic gets a second heading.
- **Define each term once, at first use.** More than 3 terms: put them in a short "Terms" table near the top.
- **Steps are numbered only when order matters.** Each step is one action. Configuration and reasoning go under the step, not inside it.
- **Tests, risks, and open questions** get their own section at the end. Never inside the steps.

Everything else in this skill applies to documents unchanged: sentence length, no parentheses, no undefined jargon, one bold per paragraph.

## Before / After

**Buried verdict → verdict first**

Before:
> I implemented the `DISCRETIONARY_SELL_CODES` constant and the `_freeze_discretionary_sells` method in `DecisionEngine`, so that defensive mode now also covers discretionary sells, and the tests pass.

After:
> **Done.** Defensive mode now also freezes discretionary sells.
>
> - New constant `DISCRETIONARY_SELL_CODES` in `DecisionEngine`
> - `stop_loss`, `score_below_threshold`, `rank_exit` now map to `HOLD_DEFENSIVE`
> - Forced sells still go through
>
> Tests: **4864** green, coverage 92.18%.

**Compound list item → split**

Before:
> - A dependency lets us scope the limiter to one route with zero risk of leaking into internal endpoints — no exclusion list to maintain.

After:
> - A **dependency** attaches to one route only.
>   Internal endpoints stay untouched. No exclusion list to maintain.

**Definition in a parenthesis → its own sentence**

Before:
> Use a fixed window counter (one Redis key per API key and per minute) and increment it on each request.

After:
> Use a **fixed window counter**. That is one Redis key per API key and per minute. Increment it on each request.

## Red Flags

If your text has any of these, rewrite it:

- The first line gives context instead of the answer
- A sentence has two or more commas separating clauses
- A parenthesis with an explanation in the middle of a sentence
- A list item with an arrow `→`, a dash, or a semicolon joining two clauses
- A paragraph longer than 3 lines
- Two bolds in one paragraph or list item
- The same thing called by two different words in one reply
- An invented word or a verb borrowed from another language
- A technical term you did not define at first use
- A closing offer or a question the reader did not ask for

## When Not To Apply

- Code, commands, and file contents stay as they are. The shape rules do not reach into code blocks.
- Quoted text, error output, and log lines stay verbatim.
- When the user explicitly asks for a detailed explanation or continuous prose.
