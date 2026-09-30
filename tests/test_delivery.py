import unittest

from src.delivery import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):
    def test_rejects_weight_below_minimum(self):
        self.assertEqual(calculate_delivery_cost(0.09, 100, "обычный"), (-1, "0000-00-00"))

    def test_rejects_weight_above_maximum(self):
        self.assertEqual(calculate_delivery_cost(50.1, 100, "обычный"), (-1, "0000-00-00"))

    def test_rejects_distance_below_minimum(self):
        self.assertEqual(calculate_delivery_cost(1.0, 0, "обычный"), (-1, "0000-00-00"))

    def test_rejects_distance_above_maximum(self):
        self.assertEqual(calculate_delivery_cost(1.0, 5001, "обычный"), (-1, "0000-00-00"))

    def test_rejects_unknown_package_type(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "нестандартный"), (-1, "0000-00-00"))

    def test_accepts_minimum_boundaries(self):
        self.assertEqual(calculate_delivery_cost(0.1, 1, "обычный"), (205, "2026-09-04"))

    def test_accepts_maximum_boundaries(self):
        self.assertEqual(calculate_delivery_cost(50.0, 5000, "обычный"), (37800, "2026-09-13"))

    def test_calculates_basic_delivery(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "обычный"), (700, "2026-09-04"))

    def test_keeps_base_rate_for_weight_exactly_five_kg(self):
        self.assertEqual(calculate_delivery_cost(5.0, 500, "обычный"), (2700, "2026-09-04"))

    def test_applies_medium_weight_coefficient(self):
        self.assertEqual(calculate_delivery_cost(10.0, 500, "обычный"), (3240, "2026-09-04"))

    def test_keeps_medium_weight_coefficient_at_twenty_kg(self):
        self.assertEqual(calculate_delivery_cost(20.0, 100, "обычный"), (840, "2026-09-04"))

    def test_applies_heavy_weight_coefficient_above_twenty_kg(self):
        self.assertEqual(calculate_delivery_cost(21.0, 100, "обычный"), (1050, "2026-09-04"))

    def test_adds_fragile_package_surcharge(self):
        self.assertEqual(calculate_delivery_cost(2.0, 100, "хрупкий"), (1000, "2026-09-04"))

    def test_adds_dangerous_package_surcharge(self):
        self.assertEqual(calculate_delivery_cost(2.0, 100, "опасный"), (1700, "2026-09-04"))

    def test_express_delivery_increases_cost_by_half(self):
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", True)
        self.assertEqual(cost, 1050)

    def test_rounds_delivery_days_up_after_five_hundred_km(self):
        self.assertEqual(calculate_delivery_cost(2.0, 501, "обычный"), (2705, "2026-09-05"))

    def test_rounds_delivery_days_up_before_one_thousand_km(self):
        self.assertEqual(calculate_delivery_cost(2.0, 999, "обычный"), (5195, "2026-09-05"))

    def test_calculates_two_days_at_one_thousand_km(self):
        self.assertEqual(calculate_delivery_cost(2.0, 1000, "обычный"), (5200, "2026-09-05"))

    def test_express_delivery_still_takes_at_least_one_day(self):
        _, delivery_date = calculate_delivery_cost(2.0, 500, "обычный", True)
        self.assertEqual(delivery_date, "2026-09-04")

    def test_returns_integer_cost_and_string_date(self):
        cost, delivery_date = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertIsInstance(cost, int)
        self.assertIsInstance(delivery_date, str)


if __name__ == "__main__":
    unittest.main()
