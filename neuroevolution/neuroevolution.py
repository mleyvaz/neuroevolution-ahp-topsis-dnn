"""Reference implementation of the neuroevolution procedure described in
section 2.2 of the article (population N=30, G=20 generations, tournament
selection k=2, crossover probability pc=0.8, mutation probability pm=0.2,
fitness estimated via a short proxy training run on CIFAR-10).

WHAT THIS IS: a runnable, documented implementation of the *method as
described in the text*, built independently for this reproducibility
package.

WHAT THIS IS NOT: the original code written by Castro Pinza and Vera
Pinargote. The article does not specify the exact genotype encoding, the
exact crossover/mutation operators, or the exact fitness function used
during the evolution loop (flagged as an unresolved gap in the article's own
review process -- see docs/DISCREPANCY_NOTE.md). Those design choices below
are reasonable, explicit defaults consistent with the console log in Figure
1 of the article (genotypes shown there are variable-length lists of
integers, e.g. "[52, 52, 335, 159, 237]"), but running this script will NOT
reproduce the article's specific published numbers.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field


@dataclass
class GAConfig:
    population_size: int = 30
    n_generations: int = 20
    tournament_k: int = 2
    crossover_prob: float = 0.8
    mutation_prob: float = 0.2
    min_layers: int = 1
    max_layers: int = 6
    min_channels: int = 8
    max_channels: int = 512
    seed: int | None = None


Genotype = list[int]  # variable-length list of conv-layer channel counts


def random_genotype(cfg: GAConfig, rng: random.Random) -> Genotype:
    n_layers = rng.randint(cfg.min_layers, cfg.max_layers)
    return [rng.randint(cfg.min_channels, cfg.max_channels) for _ in range(n_layers)]


def tournament_select(pop: list[Genotype], fitness: list[float], k: int, rng: random.Random) -> Genotype:
    contenders = rng.sample(range(len(pop)), k)
    best = max(contenders, key=lambda i: fitness[i])
    return pop[best]


def crossover(a: Genotype, b: Genotype, rng: random.Random) -> tuple[Genotype, Genotype]:
    """Single-point crossover on the shorter genotype's length."""
    cut = rng.randint(1, min(len(a), len(b)) - 1) if min(len(a), len(b)) > 1 else 1
    child1 = a[:cut] + b[cut:]
    child2 = b[:cut] + a[cut:]
    return child1, child2


def mutate(genotype: Genotype, cfg: GAConfig, rng: random.Random) -> Genotype:
    """Reinitializes one random gene (layer width) within bounds."""
    genotype = list(genotype)
    idx = rng.randrange(len(genotype))
    genotype[idx] = rng.randint(cfg.min_channels, cfg.max_channels)
    return genotype


@dataclass
class GAResult:
    best_genotype: Genotype
    best_fitness: float
    history: list[dict] = field(default_factory=list)


def run_neuroevolution(cfg: GAConfig, fitness_fn) -> GAResult:
    """fitness_fn(genotype) -> float in [0, 1] (e.g. validation accuracy).

    Injecting fitness_fn keeps this module independent of any particular
    training backend (PyTorch, a synthetic stand-in for the smoke test,
    etc.) -- see neuroevolution/smoke_test.py and the README for how to
    wire in a real CIFAR-10 proxy-training fitness function.
    """
    rng = random.Random(cfg.seed)
    population = [random_genotype(cfg, rng) for _ in range(cfg.population_size)]
    history = []
    best_genotype, best_fitness = None, -1.0

    for gen in range(1, cfg.n_generations + 1):
        fitness = [fitness_fn(ind) for ind in population]

        gen_best_idx = max(range(len(population)), key=lambda i: fitness[i])
        if fitness[gen_best_idx] > best_fitness:
            best_fitness = fitness[gen_best_idx]
            best_genotype = population[gen_best_idx]

        mean_fit = sum(fitness) / len(fitness)
        history.append({"generation": gen, "mean_fitness": mean_fit, "best_fitness": max(fitness)})

        next_population: list[Genotype] = []
        while len(next_population) < cfg.population_size:
            p1 = tournament_select(population, fitness, cfg.tournament_k, rng)
            p2 = tournament_select(population, fitness, cfg.tournament_k, rng)
            if rng.random() < cfg.crossover_prob:
                c1, c2 = crossover(p1, p2, rng)
            else:
                c1, c2 = list(p1), list(p2)
            if rng.random() < cfg.mutation_prob:
                c1 = mutate(c1, cfg, rng)
            if rng.random() < cfg.mutation_prob:
                c2 = mutate(c2, cfg, rng)
            next_population.extend([c1, c2])
        population = next_population[: cfg.population_size]

    return GAResult(best_genotype=best_genotype, best_fitness=best_fitness, history=history)


def _cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--population", type=int, default=30)
    parser.add_argument("--generations", type=int, default=20)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="Use a synthetic fitness function (no CIFAR-10 / no PyTorch needed).",
    )
    args = parser.parse_args()

    cfg = GAConfig(population_size=args.population, n_generations=args.generations, seed=args.seed)

    if args.synthetic:
        from neuroevolution.smoke_test import synthetic_fitness

        fitness_fn = synthetic_fitness
    else:
        raise SystemExit(
            "Fitness real sobre CIFAR-10 no incluido en este CLI: implementa un "
            "fitness_fn con PyTorch/torchvision (ver README) y llama a "
            "run_neuroevolution(cfg, fitness_fn) desde tu propio script."
        )

    result = run_neuroevolution(cfg, fitness_fn)
    print(f"Mejor genotipo: {result.best_genotype}")
    print(f"Mejor fitness:  {result.best_fitness:.4f}")


if __name__ == "__main__":
    _cli()
