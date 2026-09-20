# Nota de transparencia: discrepancia entre precision reportada y precision validada

Este repositorio es una **reconstruccion metodologica independiente**, escrita
en septiembre de 2026, del procedimiento AHP-TOPSIS descrito en el articulo
publicado. **No es el codigo original** de Castro Pinza y Vera Pinargote: ese
codigo, los registros de las 600 evaluaciones de fitness y las matrices AHP
individuales de los 5 expertos no estaban disponibles para el autor
correspondiente al momento de construir este paquete, a pesar de que la
seccion "Disponibilidad de datos y codigo" del articulo publicado indica que
existen "a solicitud del autor de correspondencia".

## El problema encontrado

Durante la revision adversarial interna del manuscrito (version 2, previa al
envio definitivo), se identifico una inconsistencia aritmetica entre dos
partes del mismo articulo:

- **Tabla 2** reporta la precision de test de `NE_Arch_B` como **95.80%**
  (un unico valor, sin desviacion estandar). Este es el numero que alimenta
  toda la cadena TOPSIS publicada (Tablas 3, 4 y 5) y produce el resultado
  central del articulo: `NE_Arch_B` gana con CCi = 0.8459.
- **Seccion 3.4** (validacion estadistica, 10 corridas independientes)
  reporta para el mismo `NE_Arch_B` una media real de **86.41%** (desviacion
  estandar 0.51%). Ademas, la **Tabla 6** muestra que el promedio de la
  poblacion en la generacion final (20) es 84.23%.

Una brecha de casi 9.4 puntos porcentuales entre el valor de la Tabla 2 y la
media validada de la seccion 3.4, sin explicacion en el texto, no es
defendible: 95.8% de precision en CIFAR-10 con solo 1.4M de parametros seria
un resultado de nivel estado del arte que requeriria un protocolo de
entrenamiento detallado que el articulo no proporciona.

Se detecto ademas una segunda instancia del mismo problema, no marcada
explicitamente en la revision original: la Tabla 2 reporta `Modelo_referencia`
con 94.90% de precision, mientras que la "red convolucional de referencia"
de la seccion 3.4 (que corresponde al mismo modelo baseline) valida una media
real de 82.40% (desviacion estandar 0.43%) en las mismas 10 corridas.

`NE_Arch_A` y `NE_Arch_C` nunca fueron sometidas a la validacion de 10
corridas en el articulo: solo existe para ellas el valor de una sola corrida
publicado en la Tabla 2.

## Que hace este repositorio al respecto

En vez de reconstruir codigo y datos sinteticos que reproduzcan
artificialmente el 95.80%/0.8459 tal como fueron publicados -- lo cual
fabricaria evidencia para una cifra ya identificada como indefendible --,
este repositorio ofrece **dos versiones explicitas y claramente etiquetadas**
de la cadena AHP-TOPSIS:

1. `data/table2_architecture_metrics_as_published.csv` +
   `topsis/run_topsis_as_published.py`: reproduce fielmente la Tabla 2 y el
   ranking **tal como fueron publicados** (sirve para verificar que la
   aritmetica TOPSIS del articulo es correcta dado ese input).
2. `data/table2_architecture_metrics_corrected.csv` +
   `topsis/run_topsis_corrected.py`: sustituye el C1 de `NE_Arch_B` y de
   `Modelo_referencia` por sus medias validadas de 10 corridas (seccion 3.4),
   dejando `NE_Arch_A` y `NE_Arch_C` sin cambios (nunca fueron validadas) y
   propaga la correccion a traves de toda la cadena TOPSIS.

## Resultado de la version corregida

Al usar las medias validadas, **el ranking cambia por completo**:

| Version | 1er lugar | CCi | Ultimo lugar |
|---|---|---|---|
| Publicada (Tabla 5 del articulo) | NE_Arch_B | 0.8459 | NE_Arch_A |
| Corregida (este repositorio) | **NE_Arch_C** | **0.9612** | Modelo_referencia |

`NE_Arch_B` -- la arquitectura que el articulo presenta como ganadora y
mejor equilibrada -- cae al **tercer lugar** (CCi = 0.3900) una vez que se
usa su precision realmente validada. Este resultado no confirma ni refuta
la conclusion cualitativa del articulo (que un enfoque multicriterio evita
depender de una sola metrica); lo que si muestra es que **la conclusion
cuantitativa especifica -- "NE_Arch_B es la mejor arquitectura" -- depende
enteramente de un valor de precision que la propia validacion estadistica
del articulo contradice.**

Ver `topsis/results/topsis_as_published.json` y
`topsis/results/topsis_corrected.json` para los valores numericos completos.

## Recomendacion

Antes de que este repositorio se use como respaldo de reproducibilidad ante
el tribunal de titulacion o en una version futura del articulo, se
recomienda:

1. Recuperar el codigo y los registros reales de Castro Pinza y Vera
   Pinargote para confirmar cual de las dos cifras (95.80% o 86.41%) refleja
   lo que realmente ocurrio en el experimento.
2. Si la cifra correcta es 86.41%, corregir formalmente la Tabla 2, las
   Tablas 3-5 y la Seccion 3.3/Conclusiones del articulo (incluyendo, muy
   probablemente, cual arquitectura se declara ganadora).
3. Si la version ya publicada en NCML Vol. 44 no puede corregirse, considerar
   una fe de erratas (corrigendum) formal ante la revista.
