"""White-box and boundary-oriented tests for ShoppingCart.

This module implements the documented minimal white-box dataset and
adds stronger boundary checks useful for mutation testing.
"""

import unittest

from shopping_cart import ShoppingCart


def _log(label, items, expected, actual):
    print(f"\n  [{label}]")
    print(f"    Input:    {items}")
    print(f"    Expected: {expected}")
    print(f"    Actual:   {actual}")


class TestShoppingCartWhiteBox(unittest.TestCase):
    """Tests aligned with documented white-box scenarios."""

    def setUp(self):
        self.cart = ShoppingCart()

    def _line_by_item(self, lines, item):
        return next(line for line in lines if line.item == item)

    # Documented minimal set (statement + branch coverage)
    def test_tc1_empty_cart(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: TC1 Empty cart")
        print("=" * 60)

        total, lines = self.cart.calculate([])
        _log("TC1_EMPTY_CART", [], "total=0.0, lines=[]", f"total={total}, lines={lines}")
        self.assertEqual(total, 0.0)
        self.assertEqual(lines, [])

    def test_tc2_valid_mixed_promotions(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: TC2 Valid mixed promotions")
        print("=" * 60)

        items = ["mar", "banana", "banana", "banana", "portocala", "strugure"]
        total, lines = self.cart.calculate(items)
        line_mar = self._line_by_item(lines, "mar")
        line_banana = self._line_by_item(lines, "banana")
        line_portocala = self._line_by_item(lines, "portocala")
        line_strugure = self._line_by_item(lines, "strugure")

        _log(
            "TC2_VALID_MIXED_PROMOS",
            items,
            "total=13.9, mar_discount=0.0, banana_discount=0.45, portocala_discount=0.15, strugure_discount=0.0",
            (
                f"total={total}, mar_discount={line_mar.discount}, "
                f"banana_discount={line_banana.discount}, "
                f"portocala_discount={line_portocala.discount}, "
                f"strugure_discount={line_strugure.discount}"
            ),
        )

        self.assertEqual(total, 13.9)
        self.assertEqual(line_mar.discount, 0.0)
        self.assertEqual(line_banana.discount, 0.45)
        self.assertEqual(line_portocala.discount, 0.15)
        self.assertEqual(line_strugure.discount, 0.0)

    def test_tc3_unknown_product_raises(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: TC3 Unknown product")
        print("=" * 60)

        items = ["kiwi"]
        print("\n  [TC3_UNKNOWN_PRODUCT]")
        print(f"    Input:    {items}")
        print("    Expected: ValueError")
        with self.assertRaises(ValueError):
            self.cart.calculate(items)
        print("    Actual:   ValueError raised OK")

    def test_tc4_over_max_quantity_raises(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: TC4 Over max quantity")
        print("=" * 60)

        items = ["banana"] * 11
        print("\n  [TC4_OVER_MAX_QUANTITY]")
        print("    Input:    ['banana'] x 11")
        print("    Expected: ValueError")
        with self.assertRaises(ValueError):
            self.cart.calculate(items)
        print("    Actual:   ValueError raised OK")

    # Extra boundary and mutation-oriented checks
    def test_banana_boundary_2_3_4(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: Banana boundary 2/3/4")
        print("=" * 60)

        total2, lines2 = self.cart.calculate(["banana"] * 2)
        total3, lines3 = self.cart.calculate(["banana"] * 3)
        total4, lines4 = self.cart.calculate(["banana"] * 4)

        _log(
            "Banana qty=2",
            "['banana'] x 2",
            "total=3.0, discount=0.0",
            f"total={total2}, discount={lines2[0].discount}",
        )
        _log(
            "Banana qty=3",
            "['banana'] x 3",
            "total=4.05, discount=0.45",
            f"total={total3}, discount={lines3[0].discount}",
        )
        _log(
            "Banana qty=4",
            "['banana'] x 4",
            "total=5.4, discount=0.6",
            f"total={total4}, discount={lines4[0].discount}",
        )

        self.assertEqual(total2, 3.0)
        self.assertEqual(lines2[0].discount, 0.0)

        self.assertEqual(total3, 4.05)
        self.assertEqual(lines3[0].discount, 0.45)

        self.assertEqual(total4, 5.4)
        self.assertEqual(lines4[0].discount, 0.6)

    def test_apple_boundary_2_3_4(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: Apple boundary 2/3/4")
        print("=" * 60)

        total2, lines2 = self.cart.calculate(["mar"] * 2)
        total3, lines3 = self.cart.calculate(["mar"] * 3)
        total4, lines4 = self.cart.calculate(["mar"] * 4)

        _log(
            "Mar qty=2",
            "['mar'] x 2",
            "total=4.0, discount=0.0",
            f"total={total2}, discount={lines2[0].discount}",
        )
        _log(
            "Mar qty=3",
            "['mar'] x 3",
            "total=4.0, discount=2.0",
            f"total={total3}, discount={lines3[0].discount}",
        )
        _log(
            "Mar qty=4",
            "['mar'] x 4",
            "total=6.0, discount=2.0",
            f"total={total4}, discount={lines4[0].discount}",
        )

        self.assertEqual(total2, 4.0)
        self.assertEqual(lines2[0].discount, 0.0)

        self.assertEqual(total3, 4.0)
        self.assertEqual(lines3[0].discount, 2.0)

        self.assertEqual(total4, 6.0)
        self.assertEqual(lines4[0].discount, 2.0)

    def test_apple_multiple_groups_qty_6(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: Apple multiple groups qty=6")
        print("=" * 60)

        total, lines = self.cart.calculate(["mar"] * 6)
        # 6 apples => 2 free apples => discount 4.00, net 8.00
        _log(
            "Mar qty=6",
            "['mar'] x 6",
            "total=8.0, discount=4.0",
            f"total={total}, discount={lines[0].discount}",
        )
        self.assertEqual(total, 8.0)
        self.assertEqual(lines[0].discount, 4.0)

    def test_orange_combo_multiple_oranges(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: Orange combo with multiple oranges")
        print("=" * 60)

        total, lines = self.cart.calculate(["portocala", "portocala", "strugure"])
        line_orange = self._line_by_item(lines, "portocala")

        # 2 oranges => gross 6.00, 5% discount = 0.30; plus grapes 5.00
        _log(
            "Portocala x2 + strugure",
            "['portocala', 'portocala', 'strugure']",
            "total=10.7, portocala_discount=0.3",
            f"total={total}, portocala_discount={line_orange.discount}",
        )
        self.assertEqual(line_orange.discount, 0.3)
        self.assertEqual(total, 10.7)

    def test_orange_without_grapes_has_no_discount(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: Orange without grapes")
        print("=" * 60)

        total, lines = self.cart.calculate(["portocala", "portocala"])
        line_orange = self._line_by_item(lines, "portocala")
        _log(
            "Portocala x2 fara strugure",
            "['portocala', 'portocala']",
            "total=6.0, portocala_discount=0.0",
            f"total={total}, portocala_discount={line_orange.discount}",
        )
        self.assertEqual(line_orange.discount, 0.0)
        self.assertEqual(total, 6.0)

    def test_max_quantity_exactly_10_is_valid(self):
        print("\n" + "=" * 60)
        print("TEST WHITE-BOX: Max quantity boundary qty=10")
        print("=" * 60)

        total, lines = self.cart.calculate(["banana"] * 10)
        _log(
            "Banana qty=10",
            "['banana'] x 10",
            "total=13.5, discount=1.5",
            f"total={total}, discount={lines[0].discount}",
        )
        self.assertEqual(total, 13.5)
        self.assertEqual(lines[0].discount, 1.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
