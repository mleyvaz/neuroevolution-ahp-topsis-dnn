# Reproducibility package -- Neuroevolucion + AHP-TOPSIS para arquitecturas DNN

Paquete de reproducibilidad para:

> Castro Pinza, N. A., Vera Pinargote, D. A., Rumbaut Rangel, D. & Leyva
> Vazquez, M. Y. (2026). *Modelo hibrido de neuroevolucion para optimizar
> arquitecturas DNN con AHP-TOPSIS*. Neutrosophic Computing and Machine
> Learning, 44, 598-618.

## ⚠️ Que es y que NO es este repositorio

**Es** una reconstruccion metodologica independiente, escrita en septiembre
de 2026 a partir del texto publicado del articulo, que:

- Verifica de forma independiente la razon de consistencia (CR) de la
  ponderacion AHP publicada en la Tabla 1.
- Reimplementa el procedimiento TOPSIS con normalizacion Max-Min descrito en
  la seccion 2.2, y lo corre sobre los datos de la Tabla 2.
- Ofrece una implementacion de referencia, funcional y documentada, del
  algoritmo de neuroevolucion descrito (poblacion N=30, G=20 generaciones,
  torneo k=2, pc=0.8, pm=0.2).

**No es** el codigo original que ejecutaron los estudiantes. Ese codigo, los
registros de las 600 evaluaciones de fitness y las matrices AHP individuales
de los 5 expertos no estaban disponibles al construir este repositorio.
**Lee `docs/DISCREPANCY_NOTE.md` antes de citar o usar cualquier numero de
este repositorio** -- documenta una inconsistencia real entre la Tabla 2 del
articulo (95.80% de precision para NE_Arch_B) y la validacion estadistica de
la seccion 3.4 del mismo articulo (media real de 86.41%), y muestra que el
ranking final de arquitecturas cambia por completo si se usa la cifra
validada.

## Estructura

```
ahp/
  verify_ahp_consistency.py   -> recalcula CI/CR desde lambda_max publicado
data/
  table1_ahp_weights.csv                       -> Tabla 1 del articulo
  table2_architecture_metrics_as_published.csv -> Tabla 2 tal cual publicada
  table2_architecture_metrics_corrected.csv    -> Tabla 2 con C1 corregido (ver nota)
  table6_convergence_history.csv               -> Tabla 6 del articulo
topsis/
  topsis.py                     -> implementacion generica TOPSIS Max-Min
  run_topsis_as_published.py    -> reproduce el ranking publicado (Tabla 5)
  run_topsis_corrected.py       -> ranking recalculado con precision validada
  results/*.json                -> salidas de ambas corridas
neuroevolution/
  neuroevolution.py             -> GA de referencia (poblacion/generaciones/torneo/cruce/mutacion)
  smoke_test.py                 -> prueba end-to-end con fitness sintetico (sin CIFAR-10/PyTorch)
docs/
  DISCREPANCY_NOTE.md           -> nota completa sobre la inconsistencia 95.80%/86.41%
```

## Uso rapido

```bash
pip install -r requirements.txt

# 1) Verificar la consistencia AHP (Tabla 1)
python ahp/verify_ahp_consistency.py

# 2) Reproducir el ranking TOPSIS tal como fue publicado (Tabla 5)
python topsis/run_topsis_as_published.py

# 3) Ver como cambia el ranking con la precision realmente validada
python topsis/run_topsis_corrected.py

# 4) Probar el bucle de neuroevolucion (sin necesidad de CIFAR-10/PyTorch)
python neuroevolution/smoke_test.py
```

Para conectar `neuroevolution.py` a un fitness real sobre CIFAR-10 (entrenar
cada arquitectura candidata 15 epocas y medir precision de validacion), hay
que implementar una funcion `fitness_fn(genotype) -> float` con PyTorch +
torchvision y pasarla a `run_neuroevolution(cfg, fitness_fn)`; ver los
comentarios en `neuroevolution/neuroevolution.py` y
`neuroevolution/smoke_test.py`.

## Autoria y contacto

Nahin Adrian Castro Pinza, Diego Adrian Vera Pinargote, Dayron Rumbaut
Rangel, Maikel Yelandi Leyva Vazquez (autor de correspondencia,
myleyvav@ube.edu.ec). Universidad Bolivariana del Ecuador.

## Licencia

Codigo: MIT (ver `LICENSE`). Datos derivados de las tablas del articulo:
mismos terminos, citando el articulo original.

## Como citar

Ver `CITATION.cff`.
