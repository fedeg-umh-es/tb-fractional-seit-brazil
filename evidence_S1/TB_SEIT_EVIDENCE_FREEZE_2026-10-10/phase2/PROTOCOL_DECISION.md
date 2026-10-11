# Decisión previa al rolling-origin ordinario

Estado: PHASE_2_AUTHORIZED_AFTER_NUMERICAL_GATE.

Se mantiene el rango fractional **alpha ∈ [0.50, 1.00]** de Fase 1, idéntico en los 13 orígenes. Integer fija alpha=1 y se reajusta independientemente. No se amplía el rango ni se cambia por origen. La proximidad a una frontera se documenta y no se resuelve escogiendo otro protocolo.

Se mantiene DE best1bin, popsize=15, mutation=(0.5,1.0), recombination=0.7, tol=0.01, maxiter=1000, polish=False, semilla única 20260815, límites beta [0.01,1.00], sigma [0.01,0.50], gamma [0.05,0.30], d [0.0001,0.05].

Se mantiene h_solver=1 mes; el gate previo sobre los vectores reales de Fase 1 pasó. Su umbral fue escrito antes de ejecutar: máximo cambio relativo mensual y cambios relativos de RMSE/MAE entre h=1 y h=.25 <=1%, cambio de bias <=1% de la media observada y reducción de la discrepancia al refinar. Las tres mallas se usan únicamente como control numérico de parámetros congelados. Se verificará también la resolución de los nuevos vectores por origen, sin recalibrarlos ni seleccionar malla por resultados.

La evaluación comprende exactamente 13 orígenes 2020-12…2021-12, 12 horizontes y 156 pares por modelo: fractional, integer, persistence, seasonal_naive_12 y SARIMA. Solo se reutilizan las 468 predicciones históricas de baselines después de comprobar soporte, datos, fechas de entrenamiento, protocolo y procedencia. Las 312 predicciones SEIT se generan de nuevo exclusivamente con observación ordinaria.

Skill_RMSE(h)=1-RMSE_modelo(h)/RMSE_baseline(h); Skill_MAE(h)=1-MAE_modelo(h)/MAE_baseline(h). Bias=mean(predicted-observed). H_relax es el último horizonte de skill estrictamente positivo, o cero. H_strict es la longitud del tramo positivo contiguo desde h=1, o cero. Se reportarán por baseline y métrica, sin seleccionar el más favorable. Se añade la comparación fractional frente a integer, claramente distinguida de los baselines externos.

La interpretación será descriptiva: no habrá inferencia de significación estadística, memoria epidemiológica ni superioridad general. Que fractional gane a integer no basta para reclamar habilidad frente a persistence/SARIMA. Los signos negativos y resultados desfavorables se conservan. Ningún resultado se escogerá para mantener una conclusión histórica.

alpha próximo al límite es una señal de sensibilidad y motivo de reevaluación posterior de identificabilidad; por sí solo no demuestra que el coste sea plano o que la frontera, y no los datos, determine el resultado. Con autovalores fijos, reducir alpha disminuye el umbral de Matignon alpha*pi/2; la reevaluación sigue siendo necesaria porque también cambiaron los parámetros/Jacobiano. No se trasladan los resultados antiguos de identificabilidad, R0 o DFE al modelo reajustado.

No se modifica el manuscrito, PR #3 ni resultados canónicos. Results, Abstract y Discussion históricos se consideran científicamente pendientes de actualización; PR #3 y compilación permanecen bloqueados. No habrá commit, push o merge. Se preservan todos los archivos sin seguimiento de las auditorías anteriores.
