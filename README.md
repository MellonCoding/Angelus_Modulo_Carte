# Pescata Demo — Client Draft

**Status:** DRAFT v3 — all rules confirmed with creator, ready to build
**Deadline:** Tomorrow
**Scope:** Minimal functional demo, no visual polish pass
**Source:** MOIST RPG manual (Cap. II) adapted per creator's verbal correction — manual's Lettura/majority-side/suit-court-effects system is **not** used here.

---

## 1. Confirmed Game Loop

1. **User** (single role — no separate player/master split) chooses:
   - **N** — how many cards to draw
   - **Seme** (suit) for the reading: Bastoni, Spade, Denari, or Coppe
2. App draws N cards from the deck, face-down, places them, then reveals them.
   - **If the deck has fewer than N cards left**, the reading uses only the remaining cards (draws less than N, no error/block). Once the deck is empty, it is **rebuilt fresh** (full deck, all 78 cards, reshuffled) so the game can continue with the next Pescata. When this happens, the app shows the user the message **"Il deck è finito"** — nothing else changes, the reading proceeds normally with whatever was drawn.
3. Each revealed card shows the **upright / upside-down** orientation it was already assigned at the deck's last shuffle (see §2 — orientation is not randomized at draw or reveal time).
4. Each card has a **point value** (see §3 — Scoring).
5. Any drawn card **matching the chosen Seme** has its points **doubled**.
   - Major Arcana never match a Seme (they have none) — always normal value, never doubled.
6. App sums:
   - **Upright total**
   - **Upside-down total**
7. User is asked: **"Do you want to cheat?"**
   - If yes → user flips orientation of chosen card(s).
   - Flipping a card **moves its already-calculated point value** (doubled or not) to the other total — the value itself doesn't change, only which pool it's counted in.
8. Whichever total is **higher** wins the Pescata.
9. Cards belonging to the **losing** total are returned to the **middle of the deck**.
10. Cards belonging to the **winning** total are **discarded** — removed from the active deck for the rest of the demo (not returned, not tracked separately).

---

## 2. Base Components

### `Card`
- `name` (str)
- `seme` (enum: Bastoni / Spade / Denari / Coppe / None) — `None` for Major Arcana
- `base_value` (int)
- `is_upside_down` (bool) — assigned randomly on deck creation / shuffle, **not** at draw or reveal time. Drawing and revealing a card just shows the orientation it already has.

### `Deck`
- `cards` (list of `Card`)
- Methods (planned):
  - `shuffle()` → re-randomizes `is_upside_down` for every card in the deck, in addition to reordering. Deck creation counts as an implicit shuffle.
  - `draw(n)` → returns up to N cards, removing them from the deck (orientation already set, untouched by this). If fewer than N remain, returns only what's left — does not error or block.
  - `return_to_middle(cards)` → reinserts given cards near the middle of the deck, **keeping their current orientation** until the next shuffle
  - `discard(cards)` → permanently removes given cards from the active deck for the rest of the demo (no separate discard pile tracked)
  - `is_empty()` → returns True if no cards remain
  - `rebuild()` → creates a fresh full 78-card deck (ignoring anything previously discarded) and shuffles it — called automatically once the deck is empty, so the game can keep going

### `Pescata` (the reading/round itself)
- `drawn_cards` (list of `Card`, with orientation set)
- `chosen_seme` (enum)
- `upright_total` / `upside_down_total` (int, computed)
- Methods (planned):
  - `reveal()` → randomizes orientation for each drawn card
  - `calculate_totals()` → applies seme-doubling, sums per orientation
  - `cheat(cards_to_flip)` → flips orientation of **individually selected** cards (user picks which ones), recalculates totals (doubling preserved, just moved to other pool)
  - `resolve()` → determines winning total; losing cards go back to `Deck.return_to_middle()`, winning cards go to `Deck.discard()`

---

## 3. Scoring Rules (confirmed)

**Minor Arcana (Bastoni / Spade / Denari / Coppe):**
- Numbered cards → face value
- Ace → 11
- Court cards (Re, Regina, Cavaliere, Fante) → 5 flat

**Major Arcana (no Seme, never doubled):**
- Value 0–10 → face value as-is
- Value 11+ → **digit sum** (e.g. La Luna = 17 → 1+7 = 8)

**Seme match doubling:**
- If a Minor Arcana card's suit == the reading's chosen Seme → its computed value (from rules above) is **doubled** before being added to its orientation's total.

---

## 4. Confirmed Answers Log (for traceability)

| Question | Answer |
|---|---|
| Who can cheat? | The single "user" role (creator's "master" = the app user, not a separate role) |
| Is draw count player-chosen? | Yes, for this demo (full Lettura table is a later feature, not needed now) |
| Is orientation randomized? | Yes, per card, on deck shuffle (not at draw/reveal) — persists until next shuffle |
| Scoring basis | Upright total vs upside-down total, not "majority side" from the manual |
| Seme doubling | Confirmed — chosen Seme doubles matching Minor Arcana card values |
| Major Arcana + Seme | Major Arcana have no Seme, never doubled |
| Major Arcana value calc | Digit-sum rule for 11+ retained from manual |
| Cheat effect | Flips orientation only; value (incl. doubling) carries over unchanged to new pool |
| Cheat scope | Individually selected — user picks which specific cards to flip |
| Losing cards | Returned to middle of deck |
| Winning cards | Discarded — removed from active deck for rest of demo |
| Deck runs out mid-reading | Reading uses only remaining cards (draws less than N); deck rebuilds fresh (full 78, reshuffled) once empty so play continues; app shows user the message **"Il deck è finito"** — nothing else special happens |

---

## 5. UI Requirements for Demo (functional-first)

- [ ] Input: N (number of cards to draw)
- [ ] Input: Seme selection (Bastoni / Spade / Denari / Coppe)
- [ ] Display: drawn cards, each with name, orientation, computed value (post-doubling if applicable)
- [ ] Display: upright total vs upside-down total
- [ ] Prompt: "Cheat?" — with **per-card checkboxes/selection** so the user can flip individual cards
- [ ] Display: final result — winning total, which cards return to the middle of the deck, which cards are discarded
- [ ] Message: **"Il deck è finito"** shown whenever the deck runs out mid-reading and gets rebuilt

No animation or card art required for this pass. Visual polish is an explicit second phase, not part of tomorrow's scope.

---

## 6. Suggested Build Order (tight timeline)

1. `Card` + `Deck` classes with draw/shuffle/return-to-middle logic — validate in console/print statements first.
2. Scoring logic: base values, digit-sum for Major Arcana, Seme-doubling — console-only, test against a few hand-picked draws to confirm math matches expectations.
3. Cheat logic: flip + recalculate, preserving doubled values correctly.
4. Once logic is confirmed correct end-to-end, layer on the UI (Tkinter — confirmed).

---

## 7. Not in scope for tomorrow

- Minor Arcana suit "Lettura table" draw-count-by-statistic (full manual system)
- Consulto mechanic (explicitly excluded per creator)
- Court card special effects (Re/Regina/Cavaliere/Fante triggers from manual) — not part of this simplified Pescata
- Balatro-style animation, particles, juice
- Persistent save state between sessions
- Multiplayer / multiple simultaneous users