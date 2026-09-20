"""Smoke test for neuroevolution.py using a synthetic fitness function
(no PyTorch, no CIFAR-10 download required). This only proves the GA loop
(selection, crossover, mutation, population replacement) runs correctly end
to end -- it says nothing about real CIFAR-10 accuracy.

For a real fitness function, replace synthetic_fitness with something like:

    def cifar10_proxy_fitness(genotype: list[int]) -> float:
        model = build_cnn_from_genotype(genotype)   # you implement this
        return train_and_validate(model, epochs=15, dataset="cifar10")

and wire it into run_neuroevolution(cfg, cifar10_proxy_fitness).
"""
from __future__ import annotations

import random


def synthetic_fitness(genotype: list[int]) -> float:
    """Deterministic pseudo-fitness: rewards genotypes whose total channel
    'budget' is close to a fixed target, with a fixed-seed noise term so the
    GA has something non-trivial (but reproducible) to optimize against.
    """
    target = 900
    budget = sum(genotype)
    rng = random.Random(hash(tuple(genotype)) & 0xFFFFFFFF)
    noise = rng.uniform(-0.05, 0.05)
    score = 1.0 - min(1.0, abs(budget - target) / target)
    return max(0.0, min(1.0, score + noise))


def main() -> None:
    from neuroevolution import GAConfig, run_neuroevolution

    cfg = GAConfig(population_size=10, n_generations=5, seed=42)
    result = run_neuroevolution(cfg, synthetic_fitness)

    print("Smoke test (fitness sintetico, sin CIFAR-10 ni PyTorch)")
    print("=" * 55)
    for row in result.history:
        print(
            f"Gen {row['generation']:>2}: "
            f"fitness medio={row['mean_fitness']:.4f}  "
            f"mejor de la generacion={row['best_fitness']:.4f}"
        )
    print(f"\nMejor genotipo encontrado: {result.best_genotype}")
    print(f"Mejor fitness:             {result.best_fitness:.4f}")
    assert result.best_fitness > 0, "el bucle evolutivo no produjo ningun individuo valido"
    print("\nOK: el bucle de neuroevolucion (seleccion, cruce, mutacion) corre sin errores.")


if __name__ == "__main__":
    main()
