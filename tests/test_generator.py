"""Автотесты метода обратного преобразования и итоговых наблюдений."""

from pathlib import Path
from base64 import b85decode
import json
import re
import unittest
import zlib

from src.generator import EmpiricalGenerator, dkw_threshold, kolmogorov_distance
from src.stats_utils import contingency_analysis, load_sessions


ROOT = Path(__file__).resolve().parents[1]


class GeneratorTests(unittest.TestCase):
    def test_exact_empirical_distribution(self) -> None:
        gen = EmpiricalGenerator.fit([0, 2, 2, 2, 4])
        self.assertEqual(gen.values, (0, 2, 4))
        self.assertAlmostEqual(gen.probability(0), 0.2)
        self.assertAlmostEqual(gen.probability(2), 0.6)
        self.assertAlmostEqual(gen.cdf_at(1), 0.2)
        self.assertAlmostEqual(gen.cdf_at(2), 0.8)
        self.assertAlmostEqual(gen.mean, 2.0)

    def test_reproducible_seed_and_support(self) -> None:
        gen = EmpiricalGenerator.fit([0, 2, 2, 4])
        a = gen.sample(500, seed=42)
        b = gen.sample(500, seed=42)
        self.assertEqual(a, b)
        self.assertEqual(set(a), {0, 2, 4})
        self.assertNotEqual(a, gen.sample(500, seed=43))

    def test_invalid_observations(self) -> None:
        with self.assertRaises(ValueError):
            EmpiricalGenerator.fit([])
        with self.assertRaises(ValueError):
            EmpiricalGenerator.fit([1, -1])
        with self.assertRaises(ValueError):
            EmpiricalGenerator.fit([1, 1.5])
        with self.assertRaises(ValueError):
            EmpiricalGenerator.fit([1, float("nan")])

    def test_invalid_sample_size(self) -> None:
        with self.assertRaises(ValueError):
            EmpiricalGenerator.fit([1]).sample(-1)

    def test_distribution_matches_for_large_sample(self) -> None:
        gen = EmpiricalGenerator.fit([0, 1, 1, 2, 2, 2, 4])
        simulated = gen.sample(30000, seed=2026)
        d = kolmogorov_distance(gen, simulated)
        self.assertLess(d, dkw_threshold(len(simulated), alpha=0.01))

    def test_real_dataset_contract(self) -> None:
        d = load_sessions(str(ROOT / "data" / "online_shoppers_intention.csv"))
        self.assertEqual(len(d), 12330)
        self.assertEqual(d["Revenue"].sum(), 1908)
        observed, _, _, _, min_expected, _ = contingency_analysis(d)
        self.assertEqual(observed.to_numpy().sum(), len(d))
        self.assertGreaterEqual(min_expected, 5)

    def test_marimo_embedded_frequencies_match_csv(self) -> None:
        original = (ROOT / 'marimo_app.py').read_text(encoding='utf-8')
        match = re.search(r'COUNTS_B85 = "([^"]+)"', original)
        self.assertIsNotNone(match)
        compressed = b85decode(match.group(1))
        pairs = json.loads(zlib.decompress(compressed).decode('utf-8'))
        frame = load_sessions(str(ROOT / 'data' / 'online_shoppers_intention.csv'))
        real_counts = frame['ProductRelated'].value_counts().sort_index()
        self.assertEqual(pairs, [[int(k), int(v)] for k, v in real_counts.items()])


if __name__ == "__main__":
    unittest.main()

