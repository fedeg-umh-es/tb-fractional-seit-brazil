# Control de lectura antes de cerrar métricas

Se comprobará que los signos de Skill(h) calculados con los parámetros de cada origen congelados se mantengan en h_solver=1,0.5,0.25. Las curvas de control ya previstas aportan estas predicciones; no se realiza ningún ajuste adicional. Para la comparación SEIT interna se refina ambos modelos en el mismo paso; las predicciones de baselines externos permanecen guardadas e idénticas.

Si un signo cambia, no se declarará robusto el horizonte correspondiente ni se seleccionará la malla que favorezca la conclusión; se detendrá la interpretación para revisión humana. La comparación principal sigue en h=1. Este control no define una significación estadística ni un umbral retrospectivo de materialidad.
