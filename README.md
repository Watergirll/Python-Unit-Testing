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
* **Equivalence Class Partitioning** 
* **Boundary Value Analysis**
* **Coverage:** Statement, decision, condition, and independent paths coverage.
* **Mutation Testing:** Analysis of the report created by the mutant generator, and additional tests to kill 2 surviving non-equivalent mutants.

*(Note: We will include code snippets, screenshots of test executions, results comparison in tabular format, interpretations, and diagrams made with dedicated tools like diagrams.net or Lucidchart.)*

## 4. AI Tools Usage Report 
*(Note: I will include prompts, responses, screenshots of auto-generated code execution, interpretations, and an explicit comparison between our own test suite and the auto-generated one.)*

## 5. Video Material and Presentation
* **Presentation Link (max 10 slides):** [Google Slides / Canva link] 
* **Video Demo Link:** [YouTube / Microsoft Stream link showing app demo and test runs]

## 6. References
*(Note: We will use the required template for citing official documentation, scientific articles, books, and AI tools.)*
