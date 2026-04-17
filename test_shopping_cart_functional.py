"""
Testare Funcțională (Blackbox) – TestShoppingCartFunctional
============================================================
Modulul testează clasa ShoppingCart exclusiv pe baza specificațiilor
(reguli de business), fără a inspecta codul sursă.

Reguli de business relevante:
    banana  – 1.50 RON/buc;  qty >= 3  → -10% pe linie
    mar     – 2.00 RON/buc;  fiecare al 3-lea gratuit (qty // 3 gratuite)
    portocala – 3.00 RON/buc; portocala + strugure în coș → -5% pe portocale
    strugure  – 5.00 RON/buc; fără promoție proprie
    Limită: qty > 10 per produs → ValueError
    Produs inexistent → ValueError
"""

import unittest

from shopping_cart import ShoppingCart


class TestShoppingCartFunctional(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    # ==================================================================
    # 1. PARTIȚIONARE ÎN CLASE DE ECHIVALENȚĂ
    # ==================================================================

    def test_equivalence_partitioning(self):

        # ------------------------------------------------------------------
        # Clasa 1 – Coș gol
        # Intrări invalide: lista goală nu conține niciun produs.
        # Ne așteptăm la total 0 și lista de linii vidă.
        # ------------------------------------------------------------------
        total, lines = self.cart.calculate([])
        self.assertEqual(total, 0.0)
        self.assertEqual(lines, [])

        # ------------------------------------------------------------------
        # Clasa 2 – Coș valid fără promoție
        # Un singur produs (strugure), cantitate 1 – nu se încadrează
        # în nicio regulă de discount.
        # 1 × 5.00 = 5.00 RON, discount = 0.
        # ------------------------------------------------------------------
        total, lines = self.cart.calculate(["strugure"])
        self.assertEqual(total, 5.00)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].discount, 0.0)

        # ------------------------------------------------------------------
        # Clasa 3 – Coș valid cu promoție activă
        # 3 banane → promoția -10% se activează.
        # 3 × 1.50 = 4.50; discount = 0.45; net = 4.05 RON.
        # ------------------------------------------------------------------
        total, lines = self.cart.calculate(["banana", "banana", "banana"])
        self.assertEqual(total, 4.05)
        line_banana = lines[0]
        self.assertEqual(line_banana.discount, 0.45)

        # ------------------------------------------------------------------
        # Clasa 4 – Coș mixt (produse cu și fără promoție)
        # 3 mere (al 3-lea gratuit) + 1 strugure (fără promoție).
        # Mere: 3 × 2.00 = 6.00; 1 gratuit → discount 2.00; net 4.00.
        # Strugure: 1 × 5.00 = 5.00; discount 0.
        # Total = 9.00 RON.
        # ------------------------------------------------------------------
        total, lines = self.cart.calculate(
            ["mar", "mar", "mar", "strugure"]
        )
        self.assertEqual(total, 9.00)
        line_mar = next(l for l in lines if l.item == "mar")
        self.assertEqual(line_mar.discount, 2.00)

        # ------------------------------------------------------------------
        # Clasa 5a – Produs inexistent în catalog
        # "kiwi" nu există → se așteaptă ValueError.
        # ------------------------------------------------------------------
        with self.assertRaises(ValueError):
            self.cart.calculate(["kiwi"])

        # ------------------------------------------------------------------
        # Clasa 5b – Cantitate depășește limita maximă (> 10)
        # 11 banane → se așteaptă ValueError.
        # ------------------------------------------------------------------
        with self.assertRaises(ValueError):
            self.cart.calculate(["banana"] * 11)

    # ==================================================================
    # 2. ANALIZA VALORILOR DE FRONTIERĂ
    # ==================================================================

    def test_boundary_value_analysis(self):

        # ---- Promoția "banana" (prag: qty = 3) -------------------------

        # Sub graniță: 2 banane – discount 0.
        # 2 × 1.50 = 3.00 RON.
        total, lines = self.cart.calculate(["banana", "banana"])
        self.assertEqual(total, 3.00)
        self.assertEqual(lines[0].discount, 0.0)

        # Pe graniță: exact 3 banane – promoția -10% se activează.
        # 3 × 1.50 = 4.50; discount 0.45; net 4.05 RON.
        total, lines = self.cart.calculate(["banana"] * 3)
        self.assertEqual(total, 4.05)
        self.assertEqual(lines[0].discount, 0.45)

        # Peste graniță: 4 banane – promoția rămâne activă.
        # 4 × 1.50 = 6.00; discount 0.60; net 5.40 RON.
        total, lines = self.cart.calculate(["banana"] * 4)
        self.assertEqual(total, 5.40)
        self.assertEqual(lines[0].discount, 0.60)

        # ---- Promoția "mar" (al 3-lea gratuit, prag: qty = 3) ----------

        # Sub graniță: 2 mere – nicio unitate gratuită (2 // 3 = 0).
        # 2 × 2.00 = 4.00 RON; discount 0.
        total, lines = self.cart.calculate(["mar", "mar"])
        self.assertEqual(total, 4.00)
        self.assertEqual(lines[0].discount, 0.0)

        # Pe graniță: exact 3 mere – 1 gratuit.
        # 3 × 2.00 = 6.00; discount 2.00; net 4.00 RON.
        total, lines = self.cart.calculate(["mar"] * 3)
        self.assertEqual(total, 4.00)
        self.assertEqual(lines[0].discount, 2.00)

        # Peste graniță: 4 mere – încă un singur gratuit (4 // 3 = 1).
        # 4 × 2.00 = 8.00; discount 2.00; net 6.00 RON.
        total, lines = self.cart.calculate(["mar"] * 4)
        self.assertEqual(total, 6.00)
        self.assertEqual(lines[0].discount, 2.00)

        # ---- Promoția "portocala + strugure" ---------------------------

        # Fără strugure: portocala singură – discount 0.
        # 1 × 3.00 = 3.00 RON.
        total, lines = self.cart.calculate(["portocala"])
        self.assertEqual(total, 3.00)
        self.assertEqual(lines[0].discount, 0.0)

        # Cu strugure: promoția -5% se activează pe portocale.
        # 1 × 3.00 = 3.00; discount 0.15; net 2.85.
        # + 1 × 5.00 strugure = 5.00.
        # Total = 7.85 RON.
        total, lines = self.cart.calculate(["portocala", "strugure"])
        self.assertEqual(total, 7.85)
        line_portocala = next(l for l in lines if l.item == "portocala")
        self.assertEqual(line_portocala.discount, 0.15)

        # ---- Limita maximă per produs (prag: qty = 10) -----------------

        # Pe graniță: exact 10 banane – valid, fără excepție.
        # 10 × 1.50 = 15.00; discount 10% = 1.50; net 13.50 RON.
        total, lines = self.cart.calculate(["banana"] * 10)
        self.assertEqual(total, 13.50)

        # Peste graniță: 11 banane – ValueError.
        with self.assertRaises(ValueError):
            self.cart.calculate(["banana"] * 11)


if __name__ == "__main__":
    unittest.main()
