"""
ShoppingCart – calculează valoarea finală a unui coș de cumpărături.

Catalog de produse (preț unitar):
    banana  – 1.50 RON
    mar     – 2.00 RON
    portocala – 3.00 RON
    strugure  – 5.00 RON

Reguli de business (promoții):
    1. Banana:  dacă cantitate >= 3 → discount 10 % pe fiecare buc.
    2. Mar:     la fiecare 3 bucăți, a 3-a e gratuită (multipli de 3).
    3. Portocala + strugure în același coș → discount 5 % pe portocale.
    4. Cantitate maximă per produs: 10 buc. (>10 → ValueError).
    5. Produs inexistent → ValueError.
"""

from typing import NamedTuple


CATALOG: dict[str, float] = {
    "banana":    1.50,
    "mar":       2.00,
    "portocala": 3.00,
    "strugure":  5.00,
}

MAX_QUANTITY = 10


class LineItem(NamedTuple):
    item:     str
    quantity: int
    price:    float   # preț unitar de bază
    discount: float   # discount total aplicat liniei (RON)


class ShoppingCart:
    """Procesează o listă de produse și returnează totalul și detaliile liniilor."""

    def calculate(self, items: list[str]) -> tuple[float, list[LineItem]]:
        """
        Parametri
        ----------
        items : list[str]
            Lista de produse (string-uri); același produs poate apărea de mai
            multe ori.

        Returnează
        ----------
        tuple[float, list[LineItem]]
            (valoare_finala, [LineItem(item, cantitate, pret_unitar, discount_total)])

        Excepții
        ---------
        ValueError  – produs inexistent sau cantitate > MAX_QUANTITY.
        """
        counts = self._count_items(items)
        self._validate(counts)

        has_portocala = "portocala" in counts
        has_strugure  = "strugure"  in counts

        line_items: list[LineItem] = []
        total = 0.0

        for product, qty in counts.items():
            unit_price = CATALOG[product]
            gross = unit_price * qty

            if product == "mar":
                free_units = qty // 3
                discount = round(unit_price * free_units, 2)
                net = round(gross - discount, 2)
            else:
                if product == "banana" and qty >= 3:
                    discount_rate = 0.10
                elif product == "portocala" and (has_portocala and has_strugure):
                    discount_rate = 0.05
                else:
                    discount_rate = 0.0
                discount = round(gross * discount_rate, 2)
                net = round(gross - discount, 2)

            line_items.append(LineItem(product, qty, unit_price, discount))
            total += net

        total = round(total, 2)
        return total, line_items

    # ------------------------------------------------------------------
    # Metode ajutătoare private
    # ------------------------------------------------------------------

    def _count_items(self, items: list[str]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        return counts

    def _validate(self, counts: dict[str, int]) -> None:
        for product, qty in counts.items():
            if product not in CATALOG:
                raise ValueError(f"Produs inexistent în catalog: '{product}'")
            if qty > MAX_QUANTITY:
                raise ValueError(
                    f"Cantitate prea mare pentru '{product}': {qty} > {MAX_QUANTITY}"
                )
