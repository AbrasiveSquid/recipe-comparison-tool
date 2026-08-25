import unittest

from recipe_logic.ocr import fix_mixed_fraction


class TestFixMixedFraction(unittest.TestCase):
    def test_fixes_mixed_fraction_without_space(self):
        self.assertEqual(
            fix_mixed_fraction("11/2 cups chocolate chips"),
            "1 1/2 cups chocolate chips",
        )

    def test_fixes_larger_whole_number(self):
        self.assertEqual(
            fix_mixed_fraction("21/2 cups flour"),
            "2 1/2 cups flour",
        )

    def test_preserves_normal_fraction(self):
        self.assertEqual(
            fix_mixed_fraction("3/4 cup cocoa"),
            "3/4 cup cocoa",
        )

    def test_preserves_non_fraction_quantity(self):
        self.assertEqual(
            fix_mixed_fraction("12 ounces butter"),
            "12 ounces butter",
        )

    def test_preserves_invalid_mixed_fraction_pattern(self):
        self.assertEqual(
            fix_mixed_fraction("12/2 cups flour"),
            "12/2 cups flour",
        )

    def test_preserves_leading_bullet(self):
        self.assertEqual(
            fix_mixed_fraction("• 11/3 cups sugar"),
            "• 1 1/3 cups sugar",
        )
