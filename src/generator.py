"""Дискретный генератор по эмпирической функции распределения.

Метод: обратное преобразование U ~ Uniform[0, 1) через F_n^{-1}.
Для воспроизводимости используется random.Random (Mersenne Twister).
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections import Counter
from dataclasses import dataclass
from math import isfinite, log, sqrt
from random import Random
from typing import Iterable


@dataclass(frozen=True)
class EmpiricalGenerator:
    values: tuple[int, ...]
    counts: tuple[int, ...]
    cdf: tuple[float, ...]
    population_size: int

    @classmethod
    def fit(cls, observations: Iterable[int]) -> "EmpiricalGenerator":
        frequencies: Counter[int] = Counter()
        for observation in observations:
            try:
                value = int(observation)
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("Наблюдения должны быть конечными целыми числами") from exc
            if not isfinite(float(observation)) or observation != value or value < 0:
                raise ValueError("Количество страниц должно быть целым числом >= 0")
            frequencies[value] += 1
        if not frequencies:
            raise ValueError("Нельзя обучить генератор на пустом наборе")
        values = tuple(sorted(frequencies))
        counts = tuple(frequencies[value] for value in values)
        size = sum(counts)
        running = 0
        cum_probs = []
        for count in counts:
            running += count
            cum_probs.append(running / size)
        cum_probs[-1] = 1.0
        return cls(values=values, counts=counts, cdf=tuple(cum_probs), population_size=size)

    def sample(self, size: int, seed: int | None = None) -> list[int]:
        """Для каждого U_i выбирается минимальное x, для которого F_n(x) >= U_i."""
        if not isinstance(size, int) or size < 0:
            raise ValueError("size должен быть неотрицательным целым числом")
        rng = Random(seed)
        return [self.values[bisect_left(self.cdf, rng.random())] for _ in range(size)]

    def cdf_at(self, x: float) -> float:
        i = bisect_right(self.values, x)
        return 0.0 if i == 0 else self.cdf[i - 1]

    @property
    def mean(self) -> float:
        return sum(v * c for v, c in zip(self.values, self.counts)) / self.population_size

    @property
    def variance(self) -> float:
        mu = self.mean
        return sum(c * (v - mu) ** 2 for v, c in zip(self.values, self.counts)) / self.population_size

    def probability(self, value: int) -> float:
        i = bisect_left(self.values, value)
        if i >= len(self.values) or self.values[i] != value:
            return 0.0
        return self.counts[i] / self.population_size


def kolmogorov_distance(reference: EmpiricalGenerator, sample: Iterable[int]) -> float:
    """sup_x |F_reference(x) - F_sample(x)| для дискретных данных."""
    generated = EmpiricalGenerator.fit(sample)
    support = set(reference.values) | set(generated.values)
    return max(abs(reference.cdf_at(x) - generated.cdf_at(x)) for x in support)


def dkw_threshold(n: int, alpha: float = 0.05) -> float:
    """Достаточная DKW-граница уровня 1-alpha: sqrt(ln(2/alpha)/(2n))."""
    if n <= 0 or not 0 < alpha < 1:
        raise ValueError("Ожидается n > 0 и 0 < alpha < 1")
    return sqrt(log(2 / alpha) / (2 * n))

