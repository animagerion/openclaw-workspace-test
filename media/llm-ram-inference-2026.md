## Artículo: La memoria ya no es el problema de los LLMs (y te explico por qué debería importarte)

Si has intentado alguna vez correr un modelo de lenguaje medianamente decente en tu máquina, conoces el ritual: hoping y praying a que los 16GB de VRAM sean suficientes, dividiendo el modelo entre GPU y RAM del sistema con técnicas de offloading que funcionan cuando quieren, y renunciando a contexts largos porque cada token adicional cuesta un riñón en memoria.

Eso se está acabando. Y no hablo de promesas de aquí a tres años — estoy hablando de publicaciones de las últimas tres semanas.

Vamos a lo que ha pasado.

### El KV cache nos estaba estrangulando

Antes de entrar en las novedades, hay que entender por qué la RAM/VRAM es el verdadero bottleneck de la inferencia de LLMs en 2026.

Cuando generas texto, el modelo no procesa todo de golpe. Lo hace token por token, y en cada paso necesita "recordar" todo lo que ya ha procesado. Ese "recuerdo" se guarda en el **KV cache** — las matrices de key y value de la atención. El problema: escala con el producto de las dimensiones del modelo y la longitud del contexto. Un context de 128k tokens en un Llama 3.1 70B puede necesitar más de 100GB solo para el KV cache.

Aquí es donde entra lo interesante.

### TurboQuant: Google nos acaba de regalar 6x menos memoria

El 25 de marzo de 2026, Google Research publicó **TurboQuant**, un algoritmo de compresión que reduce el KV cache a **3.5 bits por canal** — frente a los 16 bits originales de FP16. Esto supone **6 veces menos memoria** para el KV cache. En benchmarks con Nvidia H100, el speedup en atención es de hasta **8x**. Y lo más importante: **cero pérdida de precisión**.

¿Cómo funciona? Son dos técnicas combinadas:

1. **PolarQuant** — rota los vectores para que su geometría sea más predecible, eliminando la necesidad de normalización costosa. Piensa en pasar de coordenadas Cartesianas (X, Y, Z) a polares (radio + ángulo). El patrón de ángulos es conocido y concentrado, así que no necesitas calcular límites de cuantización cada vez.

2. **QJL (Quantized Johnson-Lindenstrauss)** — usa un solo bit por valor para corregir el error residual de la primera etapa.

El paper se presenta en **ICLR 2026** y ya está generando adopción en la comunidad. Las acciones de empresas de memoria GPU cayeron un 4% el mismo día del anuncio — eso te dice cuánto impacto tiene esto en el supply chain de IA.

### Qwen 3.5 Small: 9B parámetros que rinden como 120B

Si los 6x de TurboQuant te parecen poco, Alibaba publicó el 2 de marzo de 2026 los **Qwen 3.5 Small**, una familia de cuatro modelos distilled — **0.8B, 2B, 4B y 9B parámetros** — diseñados para correr en hardware de consumo sin absolutamente ninguna dependencia de la nube.

El Qwen3.5-4B puntúa **88.8 en MMLU-Redux**. Para ponerlo en contexto: eso es más alto que modelos open-source de 20B parámetros de la generación anterior. Y consume entre **2 y 14 GB de RAM** dependiendo de la variante. En un MacBook Air con 16GB unificados puedes correr el modelo de 4B con contexte de 32k tokens sin sudar.

La pregunta es obvia: ¿cómo es posible? La respuesta está en técnicas de distillation agresivas combinadas con arquitecturas optimizadas para inference eficiente desde el diseño.

Y el 30 de marzo salió **Qwen3.6-Plus Preview** con capacidades de agentic coding mejoradas sustancialmente. Si pensabas que el 3.5 era impresionante, esto es otra cosa.

### Cuantización: GGUF, GPTQ, AWQ — el tridente de 2026

Los formatos de cuantización han madurado mucho. En 2026 tienes tres opciones claras:

- **GGUF**: tu opción para CPU y ejecución local con llama.cpp. Carga el modelo en fragmentos, lo divide entre RAM y VRAM según necesites. Un 70B en Q4_K_M ocupa ~40GB, repartible.
- **GPTQ**: optimizado para GPUs NVIDIA, mejor throughput en batch inference. Los pesos se cuantizan post-training con calibración.
- **AWQ (Activation-aware Weight Quantization)**: considera la distribución de activaciones, no solo pesos. Tiende a preservar mejor la calidad en 4-bit que GPTQ para modelos grandes.

La diferencia práctica en 2026: si tienes una RTX 4060 con 8GB, AWQ en Q4_K_M te permite correr un 7B a velocidad decente. Con GGUF en Q5_K_S puedes meterlo en 16GB de RAM de sistema y usar la GPU solo para la parte crítica.

Un 70B en FP16 necesita 140GB. En AWQ Q4_K_M baja a ~35GB. En una sola RTX 4090 de 24GB no entra, pero con offloading a RAM del sistema la cosa cambia.

### Speculative decoding: el atajo que nadie te cuenta

Aquí hay una técnica que me挂 — nadie habla de ella en términos de impacto real.

El speculative decoding usa un **modelo pequeño (draft)** que propone tokens por delante, mientras el **modelo grande (target)** los verifica en paralelo. Cuando el draft acierta, generates múltiples tokens en un solo forward pass del target. El resultado: **2-3x más throughput** manteniendo exactamente la misma calidad de salida.

En la práctica, con EAGLE3 o Medusa como draft models, puedes conectar un Llama 3.1 70B como target con un Llama 3.2 1B como draft. La mejora de velocidad es brutal. Y lo que es más interesante: el draft puede residir en RAM del sistema mientras el target está en GPU, reduciendo la presión de VRAM sin sacrificar velocidad.

Ollama 3.0 soporta esto nativamente desde marzo de 2026. Si no lo estás usando, estás dejando rendimiento sobre la mesa.

### PagedAttention: el truco de la memoria que viene del SO

Si usas vLLM, ya estás beneficiándote de PagedAttention sin saberlo.

La idea: el KV cache se allocates en bloques no contiguos, como hace un sistema operativo con la memoria virtual. Antes, el cache se almacenaba en bloques contiguos que se desperdicaban terriblemente — típicamente 60-80% de waste porque cada request necesita una cantidad variable e impredecible de memoria.

PagedAttention reduce ese waste a **cerca de cero**. En la práctica significa **2-4x más requests concurrentes** en la misma GPU. Con TurboQuant encima, la misma GPU sirve a 10x usuarios que hace un año.

### ¿Qué significa esto para el futuro?

Lo que estamos viendo es una convergencia. Las técnicas de quantización por un lado, los modelos distilled más eficientes por otro, y las optimizaciones de sistema como PagedAttention y TurboQuant por un tercero. Juntas están produciendo un efecto compuesto que hace que los muros de memoria que dábamos por hechos hace 18 meses se estén derrumbando.

Un 70B que requería un nodo entero de 8x H100 en 2024 hoy cabe en un par de consumer GPUs con quantización agresiva + offloading + speculative decoding. Un 7B que necesitaba 14GB de VRAM hace un año ahora corre en 4GB de RAM de sistema con Qwen3.5-4B.

La implicación es directa: el bottleneck ya no es la memoria. Es el compute. Y cuando el compute se convierte en el bottleneck, empiezan a funcionar cosas como parallel sampling, beam search pesado, y generación de tokens a velocidades que antes eran impensables.

Esto está democratizando el inference de forma real. No porque las bigtechs lo quieran, sino porque la investigación open source está empujando tan rápido que mantener modelos propietarios con 100B+ parámetros empieza a no tener sentido económico para muchos casos de uso.

### En resumen

Si hace un año me hubieras dicho que tendría un modelo razonablemente inteligente corriendo en un MacBook Air con 16GB, le habría dicho que estaba sniffando demasiado glue. Pero aquí estamos.

Las próximas 3-6 meses van a ser brutales para las empresas que viven de cobrar por inference a precios de 2024. El software existe, los modelos existen, y las técnicas están madurando tan rápido que el próximo modelo que publiques en HuggingFace probablemente llegue con configs optimizadas para correr en el hardware que ya tienes.

La era de "necesitas una workstation de 5000€ para esto" se está cerrando. Abrete.

**P.D.:** Si tienes una RTX 4090 cogiendo polvo, actualiza tu vLLM y prueba AWQ con cualquier 7B reciente. Te va a sorprender lo que cabe.
