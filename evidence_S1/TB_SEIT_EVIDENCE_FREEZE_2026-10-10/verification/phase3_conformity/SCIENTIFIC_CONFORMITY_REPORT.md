# Auditoría de conformidad de Fase 3 — 10 de octubre de 2026

Los resultados existentes son conformes con el protocolo disponible adoptado por el autor. Pasan las **49 comprobaciones** de integridad, procedencia, aritmética y coherencia matemática. No se detecta una discrepancia científica que impida utilizar estos resultados dentro del alcance y las limitaciones especificados abajo.

La auditoría no ejecutó optimizadores, solucionadores, perfiles ni nuevos experimentos de R₀/DFE. Reconstruyó relaciones aritméticas y métricas a partir de las tablas conservadas e inspeccionó el código y los registros originales. No se reabrió la búsqueda del protocolo perdido. No se modificaron protocolos, resultados históricos, manuscrito, PR, ramas ni archivos versionados; no hubo commit, push o merge.

## 1. Protocolo, identidad y cronología

Se audita exclusivamente `PROTOCOL_DECISION.md`, con el hash adoptado:

`58d4bed36871f9c63cd93e4c199d5c9890f006ccaf96ede85362480dee91469b`

Su contenido coincide con los bytes recuperados de la llamada original que creó el archivo y con el hash registrado en `execution_provenance.json`. El ejecutor conserva igualmente su hash:

`35d9bb9ce6951be1d9a4a7a5034f94a3a1385f63e7dfabc998aa76e9d6eaa5ae`

| Evento, según el registro local de sesión | UTC, 8 de octubre | Europe/Madrid, CEST |
|---|---|---|
| Escritura de los bytes exactos del protocolo | 19:36:16.660 | 21:36:16.660 |
| Escritura de los bytes exactos del ejecutor | 19:38:57.125 | 21:38:57.125 |
| Lanzamiento de la ejecución de Fase 3 | 19:40:16.626 | 21:40:16.626 |

Las líneas 679, 693 y 716 de la sesión original están reproducidas en `chronology_fragments.jsonl`. Los hashes de los contenidos recuperados coinciden con los archivos conservados.

**Anterioridad que sí está documentada:** antes de ejecutar Fase 3 ya constaban el observable, cotas, rejilla de α, perfiles β/γ/d, semillas diagnósticas, presupuesto DE, referencia primaria para la banda del 1 %, bandas auxiliares, controles de paso, fórmula/normalización de R₀ y alcance autónomo de Matignon. Las decisiones se aplicaron al ejecutar, sin cambios posteriores de límites o selección de semillas.

**Anterioridad que no se atribuye:** esas decisiones no precedieron a Fases 1 y 2; el vector primario y la proximidad de α a la frontera ya eran conocidos. El registro local tampoco constituye un sellado temporal independiente. La adopción documental y la aceptación explícita de la rejilla y de las cuatro semillas diagnósticas por el autor son decisiones del 10 de octubre. No se atribuye equivalencia con el protocolo desaparecido ni preespecificación de toda la investigación. La frase de autorización incluida en el documento no se usa como prueba independiente de aprobación humana anterior.

La ejecución se conserva en el worktree de Fase 1, sobre `b3ad21bb059eb5357742693a4d5072107dc0df63`; la diferencia de nombre de worktree está documentada y no modifica el contrato numérico adoptado.

## 2. La calibración global existente corresponde a S1

La estimación primaria se obtuvo en Fase 1, con semilla `20260815`, calibración 2001–2020 y RMSE de la integral ordinaria mensual de σE. `ordinary_monthly_flow` toma **E corregido, índice 1**, integra trapecios ordinarios en cada intervalo y suma dentro de cada mes. No utiliza los incrementos del acumulador fraccional C como observable.

El código versionado conserva la misma dinámica SEIT. C no realimenta S/E/I/T. El estado inicial depende analíticamente de los parámetros evaluados. DE no recibió `x0` ni una población inicial construida con parámetros del operador antiguo: estos solo participaron en el control de ablación de preflight.

| Parámetro/resultado primario | Valor conservado |
|---|---:|
| β | 0.12003782836824817 |
| σ | 0.010004327168969401 |
| γ | 0.2613467372251754 |
| d | 0.03910000958695751 |
| α | 0.5022029993981696 |
| μ | 1/888 |
| RMSE de calibración | 619.3187514936859 |

Este vector coincide exactamente con el reutilizado por Fase 3. La calibración global no se repitió para Fase 3 y no se sustituyó por una solución diagnóstica de menor coste. Su procedencia es Fase 1, no el protocolo original desaparecido.

El ejecutor de Fase 1 mantiene el SHA-256 registrado `2469b1cf2447c7d1659f8e98937d450e62a4d9d0b0baf3113eed17f312a04938`. La modificación del paquete original fue únicamente detenerse ante un resultado de optimización fallido o inválido; no cambió el algoritmo ni sus parámetros.

## 3. Conformidad de lo efectivamente ejecutado

| Elemento | Comprobación |
|---|---|
| Cotas | β [.01,1], σ [.01,.5], γ [.05,.30], d [.0001,.05], α [.50,1]; todas las soluciones cumplen |
| DE | best1bin; popsize=15; mutation=(.5,1); recombination=.7; tol=.01; maxiter=1000; polish=False |
| Semillas | primaria 20260815; diagnósticas 20260816–19 conservadas todas; perfiles con 20260815 |
| Rejillas | α: 21 puntos; β, γ y d: siete cada uno; valores ejecutados coinciden exactamente con el registro |
| Soluciones | 47: primaria reutilizada + cuatro diagnósticas + 42 perfiles reoptimizados |
| Estados iniciales | 47 inicializaciones reconstruidas aritméticamente, con entrenamiento y μ correctos |
| Predicciones globales existentes | 47 × 264 = 12.408 filas, sin duplicados ni cambios de observaciones/fechas |
| Costes y validación | Todos los RMSE de entrenamiento y RMSE/MAE/bias de validación se reconstruyen desde las predicciones guardadas |
| Leakage | Objetivo con 240 meses; hash de entrenamiento común; validación excluida de la optimización y consultada después de terminar los ajustes |
| Estados DE | 46 ajustes nuevos registrados como exitosos; nfev coherente con dimensiones, popsize e iteraciones; 129 candidatos inválidos recibieron la penalización original |
| Controles numéricos | 115 registros y 114 checkpoints concordantes; el control primario restante consta en la tabla y en Fase 2 |

No se detectaron cambios reales de cotas, tolerancias, semillas, presupuesto, datos u observable respecto del protocolo disponible. Los perfiles con un parámetro fijo tienen cuatro dimensiones libres y conservan el multiplicador de población y el máximo de iteraciones declarados. Esto concuerda con el diseño ejecutado y no es una selección de presupuesto según resultados.

La columna adicional `feasible_cost_upper_bound` es el mínimo entre dos costes factibles, fijo y DE; no sustituye las columnas originales, la solución primaria ni los puntos utilizados en la envolvente de R₀. La separación entre ambas modalidades se mantiene.

## 4. Perfiles de α y equivalencia práctica

La sección fija mantiene β, σ, γ y d en sus valores primarios. El perfil reoptimizado fija α y optimiza esos cuatro parámetros. Ambos emplean exactamente la misma rejilla de 21 puntos; las soluciones DE crudas permanecen conservadas.

| α seleccionado de la rejilla | RMSE sección fija | RMSE reoptimizado | Reoptimizado dentro del 1 % |
|---:|---:|---:|---|
| 0.500000 | 618.964597 | 618.874920 | Sí |
| 0.500881 | 619.096280 | 618.788127 | Sí |
| 0.502203 | 619.318751 | 619.002596 | Sí |
| 0.520000 | 625.448103 | 621.860400 | Sí |
| 0.550000 | 651.185171 | 627.899092 | No |
| 1.000000 | 4057.569604 | 776.040852 | No |

La tabla completa permanece en `existing_phase3_evidence/alpha_profile_comparison.csv`. El punto α=1 recupera exactamente los parámetros y el coste del ajuste entero independiente de Fase 1, un control de conformidad útil.

El criterio se aplica al RMSE primario preservado, no al menor RMSE del pool:

**Admisibilidad: RMSE ≤ 619.3187514936859 × 1.01 = 625.5119390086228.**

Hay **32 soluciones admisibles de 47**. En los puntos explorados del perfil de α, la banda admite α entre 0.50 y 0.52; el siguiente punto, 0.55, queda fuera. Esto no identifica un límite continuo entre ambos puntos ni constituye un intervalo de confianza.

El menor coste explorado es 618.7881269993687, inferior al primario en 0.5306244943172 (aproximadamente 0.0857 %). Se conserva el primario por diseño. Esta diferencia es coherente con una búsqueda DE aproximada y demuestra por qué `success=True` no acredita un mínimo global único. La cota inferior de α permanece activa como limitación de interpretación; no se identifica un parámetro interior ni se demuestra memoria epidemiológica a partir de este perfil.

## 5. Envolvente de R₀: dos conjuntos distintos

La auditoría verifica la identidad aritmética de la columna guardada:

R₀ de referencia = βσ / [(σ+μ)(γ+μ+d)], con μ=1/888.

| Conjunto | n | Mínimo | Máximo | R₀<1 | R₀>1 |
|---|---:|---:|---:|---:|---:|
| Pool diagnóstico completo | 47 | 0.3416572023 | 1.6619977217 | 44 | 3 |
| Región explorada de equivalencia del 1 % | 32 | 0.3416572023 | 0.5879257724 | 32 | 0 |

El valor primario es **0.3577675038**. Se reconstruyen las seis envolventes publicadas (pool completo y bandas .1 %, .5 %, 1 %, 2 %, 5 %), incluidos tamaños, extremos, cuantiles y recuentos. La sección fija no se mezcla con el pool reoptimizado. Las soluciones R₀>1 permanecen en el conjunto diagnóstico completo; su exclusión de la banda del 1 % procede del coste de entrenamiento, no de su clasificación de estabilidad.

La envolvente describe las soluciones exploradas: no prueba que todas las soluciones matemáticamente posibles bajo el umbral estén comprendidas entre sus extremos. Tampoco es un intervalo de confianza ni una justificación para declarar R₀ identificado de forma exhaustiva.

El intervalo histórico **1.1542–1.1892** no se traslada al observable corregido. La normalización de R₀ se refiere al sistema autónomo con Nref=S*=Λ/μ; no se presenta como una estimación epidemiológica independiente de la población exógena y de los supuestos del modelo.

## 6. DFE: demostración de referencia y comprobación numérica

El DFE epidemiológico es (Λ/μ,0,0,0). Satisface las cuatro ecuaciones en ausencia de infección, incluso si N(t) es exógeno. Esto no hace constante su jacobiano.

Con q=S*/N, a=σ+μ y b=γ+μ+d, el jacobiano correcto es:

```text
J(q) = [ -μ    0   -βq    0 ]
       [  0   -a    βq    0 ]
       [  0    σ    -b    0 ]
       [  0    0     γ   -μ ]
```

La derivada ∂Tdot/∂I=γ está incluida. T no realimenta la infección; no es correcto afirmar que todas sus derivadas respecto de los otros estados sean cero. El acumulador de observación se excluye del criterio epidemiológico porque no realimenta estos cuatro estados.

**Referencia autónoma, q=1.** El bloque infectado tiene traza −(a+b), determinante ab−βσ=ab(1−R₀) y discriminante (a−b)²+4βσ>0. Sus dos autovalores son reales:

λ± = [−a−b ± √((a−b)²+4βσ)]/2.

Los otros dos autovalores son −μ. La matriz de próxima generación, con F=[[0,β],[0,0]] y V=[[a,0],[−σ,b]], tiene radio espectral βσ/(ab), la fórmula usada en las tablas. Un factor común positivo de escala temporal en F y V cancela y conserva los argumentos de los autovalores.

Para el sistema autónomo con orden Caputo común, la estabilidad asintótica lineal exige |arg(λ)|>απ/2 para todos los autovalores; la estabilidad local del equilibrio no lineal se apoya en el principio de estabilidad por linearización. [Cong et al., 2016](https://arxiv.org/abs/1512.04989), [Brandibur, Garrappa y Kaslik, 2021](https://doi.org/10.3390/math9080914).

Aquí, si R₀<1, los cuatro autovalores son negativos y satisfacen el criterio para todo 0<α≤1. Si R₀>1, aparece un autovalor real positivo y falla el criterio. R₀=1 es un caso no hiperbólico que no debe clasificarse automáticamente como estabilidad asintótica. Reducir α con autovalores fijos reduce el umbral angular; no lo hace más exigente.

**Comprobación de las tablas existentes.** Los 188 autovalores guardados coinciden con las raíces analíticas del jacobiano de cuatro estados; argumentos, umbrales y márgenes también concuerdan. Las 32 soluciones admisibles son estables en la referencia autónoma. En el pool completo hay 44 estables y tres inestables, coincidiendo con la clasificación de R₀. El margen primario de Matignon es 2.3527340268 radianes.

**Implementación con N(t).** El cociente q(t)=S*/N(t) cambia y, por tanto, J(t) también. Los 12.408 registros congelados en el tiempo coinciden con la población de entrenamiento y su extrapolación conservadas, con el cociente q, la fórmula de R₀ congelado y las raíces correspondientes. Todos están rotulados como diagnósticos sin prueba no autónoma. Matignon aplicado punto a punto no constituye una demostración de estabilidad del sistema temporal. Esta limitación está en el protocolo y en los resultados originales; no es una falla aritmética descubierta después.

## 7. Convergencia, reproducibilidad e integridad

Los 115 controles guardados en h=1,0.5,0.25 cumplen los umbrales establecidos y concuerdan con sus checkpoints. La mayor diferencia mensual relativa registrada es **0.0011913373**, es decir, aproximadamente **0.119134 %**, por debajo del 1 %. Las discrepancias disminuyen al refinar. La pertenencia a la región del 1 % es idéntica al usar los costes guardados de h=0.25 y su referencia primaria correspondiente.

No están archivadas todas las trayectorias de estados de las mallas finas de Fase 3. Su evidencia de resolución consiste en controles y checkpoints, código completo e insumos conservados. Esta auditoría no vuelve a ejecutar el solucionador para confirmarlas de forma independiente, conforme a la restricción del autor. Los costes h=1 sí se verifican independientemente desde todas las predicciones guardadas. Esto es una limitación de granularidad del archivo, no un incumplimiento del protocolo, que no exigía guardar esos estados.

Se verifican los 239 archivos versionados, los 61 archivos de fases anteriores y los hashes de protocolo, ejecutores y resultados incluidos en la reconciliación previa. Todos los archivos de Fase 3 se copian byte a byte en `existing_phase3_evidence/` y se inventarían con SHA-256. El manifiesto integral actual documenta la auditoría; no se presenta como un sellado prospectivo inexistente de todos los resultados anteriores.

El paquete incluye el verificador `audit_phase3_conformity_20261010.py`, `conformity_checks.csv`, `audit_evidence.json`, fragmentos de cronología y copia de las tablas y fuentes existentes. El verificador realiza inspección estática y reconstrucción aritmética; no llama al ejecutor científico. Para repetir la comprobación se necesitan el entorno de dependencias documentado y los insumos del repositorio sobre el commit indicado. No se ha repetido el benchmark rolling-origin.

## 8. Comparación con los claims históricos y alcance de cierre

| Aspecto | Histórico | Evidencia corregida auditada |
|---|---|---|
| α primario | 0.964011 | 0.502203; perfil próximo a la frontera |
| Identificabilidad práctica | Claims del observable anterior | Diagnóstico condicionado a cotas y conjunto explorado; sin unicidad demostrada |
| Envolvente R₀ del 1 % | 1.1542–1.1892 | 0.341657–0.587926 en 32 soluciones exploradas |
| DFE | Resultado histórico no trasladable | Estabilidad de referencia autónoma; no prueba no autónoma con N(t) |
| Forecasting | Resultados anteriores del otro observable | Fase 2 conserva su evaluación independiente; no se repitió ni se congeló aquí |

Las diferencias documentales aceptadas —identidad del protocolo, 21 puntos de α y cuatro semillas diagnósticas— no alteran la lectura descriptiva de los cálculos conservados. No acreditan, sin embargo, una preespecificación anterior a Fases 1/2 ni autorizan claims causales, inferenciales o de identificación exhaustiva.

No se encuentra una desviación real que exija recalibrar, repetir perfiles o volver a calcular R₀/DFE para utilizar la evidencia **dentro de este alcance**. Queda preparada para la siguiente etapa de reconciliación de claims y congelación por el autor. Esta auditoría no actualiza el manuscrito ni libera PR #3 para merge o compilación; esos bloqueos editoriales continúan hasta el cierre científico correspondiente.

**Dictamen: `PHASE3_PASS_WITH_DOCUMENTED_LIMITATIONS`.**
