"""
Testare Functionala (Blackbox) - TestShoppingCartFunctional
============================================================
Modulul testeaza clasa ShoppingCart exclusiv pe baza specificatiilor
(reguli de business), fara a inspecta codul sursa.

Reguli de business relevante:
    banana    - 1.50 RON/buc;  qty >= 3  -> -10% pe linie
    mar       - 2.00 RON/buc;  fiecare al 3-lea gratuit (qty // 3 gratuite)
    portocala - 3.00 RON/buc;  portocala + strugure in cos -> -5% pe portocale
    strugure  - 5.00 RON/buc;  fara promotie proprie
    Limita: qty > 10 per produs -> ValueError
    Produs inexistent -> ValueError
"""

import unittest

from shopping_cart import ShoppingCart


def _log(label, items, expected, actual):
    print(f"\n  [{label}]")
    print(f"    Input:    {items}")
    print(f"    Expected: {expected}")
    print(f"    Actual:   {actual}")


class TestShoppingCartFunctional(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    # ==================================================================
    # 1. PARTITIONARE IN CLASE DE ECHIVALENTA
    # ==================================================================

    def test_equivalence_partitioning(self):
        print("\n" + "=" * 60)
        print("TEST: Partitionare in clase de echivalenta")
        print("=" * 60)

        # ------------------------------------------------------------------
        # Clasa 1 - Cos gol
        # Lista goala nu contine niciun produs.
        # Ne asteptam la total 0 si lista de linii vida.
        # ------------------------------------------------------------------
        items = []
        total, lines = self.cart.calculate(items)
        _log("Clasa 1 - Cos gol", items,
             "total=0.0, lines=[]",
             f"total={total}, lines={lines}")
        self.assertEqual(total, 0.0,
            msg=f"Clasa 1: expected total=0.0, got {total}")
        self.assertEqual(lines, [],
            msg=f"Clasa 1: expected lines=[], got {lines}")

        # ------------------------------------------------------------------
        # Clasa 2 - Cos valid fara promotie
        # Un singur produs (strugure), cantitate 1.
        # 1 x 5.00 = 5.00 RON, discount = 0.
        # ------------------------------------------------------------------
        items = ["strugure"]
        total, lines = self.cart.calculate(items)
        _log("Clasa 2 - Fara promotie", items,
             "total=5.0, discount=0.0",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 5.00,
            msg=f"Clasa 2: expected total=5.0, got {total}")
        self.assertEqual(lines[0].discount, 0.0,
            msg=f"Clasa 2: expected discount=0.0, got {lines[0].discount}")

        # ------------------------------------------------------------------
        # Clasa 3 - Cos valid cu promotie activa
        # 3 banane -> promotia -10% se activeaza.
        # 3 x 1.50 = 4.50; discount = 0.45; net = 4.05 RON.
        # ------------------------------------------------------------------
        items = ["banana", "banana", "banana"]
        total, lines = self.cart.calculate(items)
        _log("Clasa 3 - Promotie activa (3 banane)", items,
             "total=4.05, discount=0.45",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 4.05,
            msg=f"Clasa 3: expected total=4.05, got {total}")
        self.assertEqual(lines[0].discount, 0.45,
            msg=f"Clasa 3: expected discount=0.45, got {lines[0].discount}")

        # ------------------------------------------------------------------
        # Clasa 4 - Cos mixt (produse cu si fara promotie)
        # 3 mere (al 3-lea gratuit) + 1 strugure (fara promotie).
        # Mere: 3 x 2.00 = 6.00; 1 gratuit -> discount 2.00; net 4.00.
        # Strugure: 1 x 5.00 = 5.00; discount 0.
        # Total = 9.00 RON.
        # ------------------------------------------------------------------
        items = ["mar", "mar", "mar", "strugure"]
        total, lines = self.cart.calculate(items)
        line_mar = next(l for l in lines if l.item == "mar")
        _log("Clasa 4 - Cos mixt", items,
             "total=9.0, mar_discount=2.0",
             f"total={total}, mar_discount={line_mar.discount}")
        self.assertEqual(total, 9.00,
            msg=f"Clasa 4: expected total=9.0, got {total}")
        self.assertEqual(line_mar.discount, 2.00,
            msg=f"Clasa 4: expected mar discount=2.0, got {line_mar.discount}")

        # ------------------------------------------------------------------
        # Clasa 5a - Produs inexistent in catalog
        # "kiwi" nu exista -> se asteapta ValueError.
        # ------------------------------------------------------------------
        items = ["kiwi"]
        print(f"\n  [Clasa 5a - Produs inexistent]")
        print(f"    Input:    {items}")
        print(f"    Expected: ValueError")
        with self.assertRaises(ValueError,
                msg=f"Clasa 5a: expected ValueError for input {items}"):
            self.cart.calculate(items)
        print(f"    Actual:   ValueError raised OK")

        # ------------------------------------------------------------------
        # Clasa 5b - Cantitate depaseste limita maxima (> 10)
        # 11 banane -> se asteapta ValueError.
        # ------------------------------------------------------------------
        items = ["banana"] * 11
        print(f"\n  [Clasa 5b - Cantitate peste limita]")
        print(f"    Input:    ['banana'] x 11")
        print(f"    Expected: ValueError")
        with self.assertRaises(ValueError,
                msg=f"Clasa 5b: expected ValueError for 11 bananas"):
            self.cart.calculate(items)
        print(f"    Actual:   ValueError raised OK")

    # ==================================================================
    # 2. ANALIZA VALORILOR DE FRONTIERA
    # ==================================================================

    def test_boundary_value_analysis(self):
        print("\n" + "=" * 60)
        print("TEST: Analiza valorilor de frontiera")
        print("=" * 60)

        # ---- Promotia "banana" (prag: qty = 3) -------------------------
        print("\n  -- banana: prag qty=3 (discount -10%) --")

        # Sub granita: 2 banane - discount 0. 2 x 1.50 = 3.00 RON.
        items = ["banana"] * 2
        total, lines = self.cart.calculate(items)
        _log("Sub granita (qty=2)", items,
             "total=3.0, discount=0.0",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 3.00,
            msg=f"Banana sub granita: expected 3.0, got {total}")
        self.assertEqual(lines[0].discount, 0.0,
            msg=f"Banana sub granita: expected discount=0.0, got {lines[0].discount}")

        # Pe granita: exact 3 banane - promotia -10% se activeaza.
        # 3 x 1.50 = 4.50; discount 0.45; net 4.05 RON.
        items = ["banana"] * 3
        total, lines = self.cart.calculate(items)
        _log("Pe granita (qty=3)", items,
             "total=4.05, discount=0.45",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 4.05,
            msg=f"Banana pe granita: expected 4.05, got {total}")
        self.assertEqual(lines[0].discount, 0.45,
            msg=f"Banana pe granita: expected discount=0.45, got {lines[0].discount}")

        # Peste granita: 4 banane - promotia ramane activa.
        # 4 x 1.50 = 6.00; discount 0.60; net 5.40 RON.
        items = ["banana"] * 4
        total, lines = self.cart.calculate(items)
        _log("Peste granita (qty=4)", items,
             "total=5.40, discount=0.60",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 5.40,
            msg=f"Banana peste granita: expected 5.40, got {total}")
        self.assertEqual(lines[0].discount, 0.60,
            msg=f"Banana peste granita: expected discount=0.60, got {lines[0].discount}")

        # ---- Promotia "mar" (al 3-lea gratuit, prag: qty = 3) ----------
        print("\n  -- mar: prag qty=3 (al 3-lea gratuit) --")

        # Sub granita: 2 mere - nicio unitate gratuita (2 // 3 = 0).
        # 2 x 2.00 = 4.00 RON; discount 0.
        items = ["mar"] * 2
        total, lines = self.cart.calculate(items)
        _log("Sub granita (qty=2)", items,
             "total=4.0, discount=0.0",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 4.00,
            msg=f"Mar sub granita: expected 4.0, got {total}")
        self.assertEqual(lines[0].discount, 0.0,
            msg=f"Mar sub granita: expected discount=0.0, got {lines[0].discount}")

        # Pe granita: exact 3 mere - 1 gratuit.
        # 3 x 2.00 = 6.00; discount 2.00; net 4.00 RON.
        items = ["mar"] * 3
        total, lines = self.cart.calculate(items)
        _log("Pe granita (qty=3)", items,
             "total=4.0, discount=2.0",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 4.00,
            msg=f"Mar pe granita: expected 4.0, got {total}")
        self.assertEqual(lines[0].discount, 2.00,
            msg=f"Mar pe granita: expected discount=2.0, got {lines[0].discount}")

        # Peste granita: 4 mere - 1 gratuit (4 // 3 = 1).
        # 4 x 2.00 = 8.00; discount 2.00; net 6.00 RON.
        items = ["mar"] * 4
        total, lines = self.cart.calculate(items)
        _log("Peste granita (qty=4)", items,
             "total=6.0, discount=2.0",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 6.00,
            msg=f"Mar peste granita: expected 6.0, got {total}")
        self.assertEqual(lines[0].discount, 2.00,
            msg=f"Mar peste granita: expected discount=2.0, got {lines[0].discount}")

        # ---- Promotia "portocala + strugure" ---------------------------
        print("\n  -- portocala: discount -5% doar cu strugure in cos --")

        # Fara strugure: portocala singura - discount 0. 1 x 3.00 = 3.00.
        items = ["portocala"]
        total, lines = self.cart.calculate(items)
        _log("Fara combo (portocala singura)", items,
             "total=3.0, discount=0.0",
             f"total={total}, discount={lines[0].discount}")
        self.assertEqual(total, 3.00,
            msg=f"Portocala fara combo: expected 3.0, got {total}")
        self.assertEqual(lines[0].discount, 0.0,
            msg=f"Portocala fara combo: expected discount=0.0, got {lines[0].discount}")

        # Cu strugure: promotia -5% se activeaza pe portocale.
        # portocala: 3.00 - 5% = 2.85 (discount 0.15); strugure: 5.00.
        # Total = 7.85 RON.
        items = ["portocala", "strugure"]
        total, lines = self.cart.calculate(items)
        line_portocala = next(l for l in lines if l.item == "portocala")
        _log("Cu combo (portocala + strugure)", items,
             "total=7.85, portocala_discount=0.15",
             f"total={total}, portocala_discount={line_portocala.discount}")
        self.assertEqual(total, 7.85,
            msg=f"Portocala cu combo: expected 7.85, got {total}")
        self.assertEqual(line_portocala.discount, 0.15,
            msg=f"Portocala cu combo: expected discount=0.15, got {line_portocala.discount}")

        # ---- Limita maxima per produs (prag: qty = 10) -----------------
        print("\n  -- limita maxima per produs: MAX_QUANTITY=10 --")

        # Pe granita: exact 10 banane - valid.
        # 10 x 1.50 = 15.00; discount 10% = 1.50; net 13.50 RON.
        items = ["banana"] * 10
        total, lines = self.cart.calculate(items)
        _log("Pe granita (qty=10)", "['banana'] x 10",
             "total=13.50",
             f"total={total}")
        self.assertEqual(total, 13.50,
            msg=f"Limita max pe granita: expected 13.50, got {total}")

        # Peste granita: 11 banane - ValueError.
        print(f"\n  [Peste granita (qty=11)]")
        print(f"    Input:    ['banana'] x 11")
        print(f"    Expected: ValueError")
        with self.assertRaises(ValueError,
                msg="Limita max peste granita: expected ValueError for 11 bananas"):
            self.cart.calculate(["banana"] * 11)
        print(f"    Actual:   ValueError raised OK")


if __name__ == "__main__":
    unittest.main(verbosity=2)
