# Python-Unit-Testing

# Software Testing Systems (SST) Project

**Chosen Theme:** T1 Unit Testing in Python

## Team
Created by Teodora-Ioana Popa - teodora-ioana.popa@s.unibuc.ro

## 1. Application Description

The project implements a small **shopping-cart calculator** in Python (`shopping_cart.py`). The main class is **`ShoppingCart`**. Its public method **`calculate(items)`** accepts a **list of product name strings** (e.g. `['banana', 'banana', 'mar', 'mar', 'mar']`). Products are aggregated by name, validated against a fixed **catalog** (`banana`, `mar`, `portocala`, `strugure`) with unit prices in RON. **Invalid product names** or **quantities above 10 per product** raise **`ValueError`**.

**Business rules (promotions):**

- **Bananas:** if quantity ≥ 3, a **10%** discount applies to that line.
- **Apples (`mar`):** for every **3** apples, the **third** is **free** (repeats for every full group of three).
- **Oranges:** if the cart contains both **oranges and grapes**, a **5%** discount applies to the orange line.

The method returns a **tuple**: the **final total** (rounded to two decimals) and a **list of line items**. Each line is a **`LineItem`** named tuple: **(item, quantity, unit price, total discount in RON for that line)**. The implementation uses explicit branching (`if` / `elif` / `else`), compound conditions, and loops over the aggregated products.

## 2. Environment Configuration

* **Hardware Configuration:** [e.g., CPU, RAM]
* **Software Configuration:** [e.g., OS, Python version]
* **Virtual Machine:** [Yes/No, and details if applicable]
* **Tool Versions:** [e.g., pytest version X, mutmut version Y]

## 3. Testing Strategies

### 3.1 Functional testing (black-box)

File: **`test_shopping_cart_functional.py`** — class **`TestShoppingCartFunctional`** (`unittest.TestCase`).
Tests are derived exclusively from the specification (prices, promotion rules, validation rules), without reading the source code.

```bash
python -m unittest test_shopping_cart_functional.py -v
```

#### Equivalence class partitioning

One representative input per class; each block in the test file carries a comment with the class name.

| # | Equivalence class | Representative input | Expected outcome | Actual outcome | Interpretation |
|---|-------------------|----------------------|------------------|----------------|----------------|
| 1 | Empty cart | `[]` | Total **0.00** RON, no lines | total=0.0, lines=[] ✓ | No products → no charge. |
| 2 | Valid, no promotion | `["strugure"]` | Total **5.00** RON, discount **0** | total=5.0, discount=0.0 ✓ | Qty 1, no rule applies (1 × 5.00). |
| 3 | Valid, promotion active | `["banana", "banana", "banana"]` | Total **4.05** RON, discount **0.45** | total=4.05, discount=0.45 ✓ | −10% on 3 × 1.50 = 4.50 → 4.05. |
| 4 | Mixed cart | `["mar","mar","mar","strugure"]` | Total **9.00** RON, mar discount **2.00** | total=9.0, mar_discount=2.0 ✓ | 3rd apple free (4.00) + grapes (5.00). |
| 5a | Invalid product name | `["kiwi"]` | `ValueError` | ValueError raised ✓ | Not in catalog → rejected. |
| 5b | Quantity over limit | `["banana"] * 11` | `ValueError` | ValueError raised ✓ | 11 > MAX_QUANTITY (10) → rejected. |


#### Boundary value analysis

Values at, below, and above each threshold that triggers a promotion or validation rule.

| Scenario | Input | Expected total (RON) | Actual total (RON) | Interpretation |
|----------|-------|----------------------|--------------------|----------------|
| Bananas — below threshold | 2 | **3.00** | 3.0, discount=0.0 ✓ | −10% needs ≥ 3; no discount. |
| Bananas — on threshold | 3 | **4.05** | 4.05, discount=0.45 ✓ | −10% activates: 4.50 − 0.45. |
| Bananas — above threshold | 4 | **5.40** | 5.4, discount=0.6 ✓ | Discount still applies: 6.00 − 0.60. |
| Apples — below "3rd free" | 2 | **4.00** | 4.0, discount=0.0 ✓ | 2 × 2.00, no free unit (2 // 3 = 0). |
| Apples — on threshold | 3 | **4.00** | 4.0, discount=2.0 ✓ | 1 free apple: pay for 2 × 2.00. |
| Apples — above threshold | 4 | **6.00** | 6.0, discount=2.0 ✓ | 1 free in first trio, 3 paid overall. |
| Oranges, no grapes | 1× `portocala` | **3.00** | 3.0, discount=0.0 ✓ | Combo rule inactive without grapes. |
| Oranges + grapes | `portocala` + `strugure` | **7.85** | 7.85, portocala_discount=0.15 ✓ | −5% on oranges (2.85) + 5.00 grapes. |
| Max quantity — valid | 10× `banana` | **13.50** | 13.5 ✓ | 10 = MAX_QUANTITY, accepted. |
| Max quantity — over limit | 11× `banana` | `ValueError` | ValueError raised ✓ | 11 > MAX_QUANTITY, rejected. |

> **Screenshot to show test results:**
> <img width="1092" height="940" alt="image" src="https://github.com/user-attachments/assets/3e0ee633-0969-4631-baae-3585e6eac73d" />
> <img width="1104" height="970" alt="image" src="https://github.com/user-attachments/assets/5b9cbfbd-0bf4-450c-b4f3-784b0c1fd968" />
> <img width="1098" height="963" alt="image" src="https://github.com/user-attachments/assets/9e40b0d4-f02d-42b1-93ff-df296bfe175f" />





> **Diagram to insert here (recommended):** draw a number line for the banana/apple thresholds (mark 2 / 3 / 4 and 10 / 11 with labels "no discount", "discount ON", "limit OK", "limit FAIL"). Use [diagrams.net](https://app.diagrams.net/) or similar. This one diagram covers both the equivalence classes and the boundary analysis visually and is useful for the slides.

### 3.2 White-box testing

Goal: execute each instruction at least once (Statement Coverage) and execute each decision on both outcomes True/False (Decision/Branch Coverage).

#### Minimal test data for 100% Statement + 100% Branch (ShoppingCart)

| ID | Input | Expected | Main branches covered |
|----|-------|----------|-----------------------|
| TC1_EMPTY_CART | `[]` | total=0.0, lines=[] | `calculate`: for-loop not entered; `_count_items`: empty input; `_validate`: no iteration |
| TC2_VALID_MIXED_PROMOS | `["mar", "banana", "banana", "banana", "portocala", "strugure"]` | total=15.9 | `product == "mar"` (True/False), banana promo decision (True/False), orange+grape decision (True/False), `else` with discount_rate=0.0 |
| TC3_UNKNOWN_PRODUCT | `["kiwi"]` | `ValueError` | `_validate`: `product not in CATALOG` -> True |
| TC4_OVER_MAX_QUANTITY | `["banana"] * 11` | `ValueError` | `_validate`: `qty > MAX_QUANTITY` -> True |

Why this set is minimal:

- One valid empty-cart case is needed for the path where the main loop is skipped.
- One valid non-empty mixed case is needed to traverse all promotion-related branches.
- Two separate invalid cases are needed because unknown product and over-limit quantity are different error branches.

#### MC/DC for compound decision

Consider decision form `if A or (B and C)`.

For ShoppingCart, this structure appears in the orange promotion check:

- `A`: `product == "portocala"`
- `B`: `has_portocala`
- `C`: `has_strugure`
- Decision: `A and (B and C)`

To document MC/DC independently of domain semantics, the generic test set for `A or (B and C)` is:

| Test | A | B | C | D = A or (B and C) |
|------|---|---|---|--------------------|
| MCDC_T1 | 0 | 1 | 1 | 1 |
| MCDC_T2 | 0 | 0 | 1 | 0 |
| MCDC_T3 | 0 | 1 | 0 | 0 |
| MCDC_T4 | 1 | 1 | 0 | 1 |

Independence pairs (no masking):

- A influences decision: `MCDC_T3` vs `MCDC_T4` (B,C fixed to 1,0)
- B influences decision: `MCDC_T2` vs `MCDC_T1` (A,C fixed to 0,1)
- C influences decision: `MCDC_T3` vs `MCDC_T1` (A,B fixed to 0,1)

Masking avoidance rule:

- For B and C, keep A=0 so A cannot force decision to True.
- For A, keep `(B and C)=0` so decision depends only on A.

#### Complexitate ciclomatica si set de circuite independente

Pentru graful de control din `diagrams/CFG_calcul.drawio`, folosim formula McCabe:

`V(G) = e - n + 2`

Unde:

- `n = 13` noduri (B0..B10, incluzand nodurile intermediare B8a/B8b)
- `e = 16` muchii

Rezultat:

`V(G) = 16 - 13 + 2 = 5`

Deci numarul minim de trasee linear independente (basis paths) este 5.

Set de baza propus (P1..P5):

- `P1`: B0 -> B1(F) -> B10
- `P2`: B0 -> B1(T) -> B2 -> B3(T) -> B4 -> B9 -> B1(F) -> B10
- `P3`: B0 -> B1(T) -> B2 -> B3(F) -> B5(T) -> B6 -> B8 -> B9 -> B1(F) -> B10
- `P4`: B0 -> B1(T) -> B2 -> B3(F) -> B5(F) -> B7(T) -> B8a -> B8 -> B9 -> B1(F) -> B10
- `P5`: B0 -> B1(T) -> B2 -> B3(F) -> B5(F) -> B7(F) -> B8b -> B8 -> B9 -> B1(F) -> B10

Acest set garanteaza parcurgerea tuturor ramurilor relevante:

- iesirea din bucla (`B1`: True/False)
- decizia `product == "mar"` (True/False)
- decizia `banana >= 3` (True/False)
- decizia `portocala combo` (True/False)

### 3.3 Planned / further work

* **Mutation testing:** run `mutmut`, analyse the surviving mutants, write 2 extra tests to kill 2 non-equivalent survivors.

## 4. AI Tools Usage Report

*(Note: I will include prompts, responses, screenshots of auto-generated code execution, interpretations, and an explicit comparison between our own test suite and the auto-generated one.)*

## 5. Video Material and Presentation

* **Presentation Link (max 10 slides):** [Google Slides / Canva link]
* **Video Demo Link:** [YouTube / Microsoft Stream link showing app demo and test runs]

## 6. References

*(Note: We will use the required template for citing official documentation, scientific articles, books, and AI tools.)*
