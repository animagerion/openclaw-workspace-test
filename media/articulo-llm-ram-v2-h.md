# El problema de la RAM que nadie cuenta pero que está frenando la IA de verdad

La verdad es que me tiene fascinado lo que está pasando con la memoria en inferencia de LLMs. Llevamos años hablando de modelos más grandes, más potentes, más parámetros —pero lo que nadie te dice es que el verdadero bottleneck no es el modelo en sí, es la maldita RAM. Cada token que genera un LLM necesita acceder a una cantidad absurda de datos, y eso sin entrar en lo que pasa cuando tienes cien usuarios simultáneos.

## Lo que nadie te cuenta del KV cache

Vale, necesito explicar algo rápido. El KV cache. Si ya lo sabes, sáltate este párrafo. Si no, quédate: cuando un LLM genera texto, es autoregresivo —un token a la vez, y cada token depende de todos los anteriores. En cada paso, el modelo recalcula la atención de cada token contra todos los anteriores. Eso es una locura computacional. El KV cache evita eso guardando las matrices de atención ya calculadas, así cada nuevo token solo suma su parte. Práctico, sí. El problema es que ese cache crece de forma cuadrática con la longitud de la secuencia.

Contexto de 4.096 tokens en un LLaMA 70B, el KV cache puede superar los 60 GB. Sesenta gigas. Por solicitud. En un sistema con 100 usuarios concurrently, estás hablando de necesitar 100 copias independientes de ese cache. Esto no lo invento yo, lo documentan ellos mismos en los papers de arXiv de marzo de 2026 —el trabajo de Yichun Xu, Navjot K. Khaira y Tejinder Singh lo llama directamente "el factor limitante para el throughput en sistemas de producción". A mí me parece que lo están diciendo bastante claro y la gente sigue hablando de cosas más espectaculares.

## TurboQuant y la compresión que cambia todo

Acá es donde se pone interesante. La cuantización del KV cache a 3 bits por valor —sí, leíste bien, 3 bits— permite reducir el consumo de memoria en un factor de más de 5x. El paper de Hu, Wang y Liu (27 de marzo de 2026) lo demuestra con una técnica basada en rotación ortogonal y corrección Johnson-Lindenstrauss. En modelos de proteínas, donde el KV cache crece de forma cuadrática, pasar de 16 bits a 3 bits es una diferencia brutal. La gente no se da cuenta de lo que implica esto hasta que lo ve en números.

Pero hay más. Lu, Qiu y Zhou et al. propusieron en febrero de 2026 algo que a mí me parece elegante: comprimir cada token del KV cache de forma independiente según su importancia. Tokens más relevantes reciben más bits, los menos relevantes se comprimen más. Se llama cuantización token-wise adaptativa, y permite ajustes finos sin pérdida significativa de calidad. En la práctica, significa que puedes decidir qué importa de verdad en una conversación larga y guardar solo eso.

Y luego está PRISM. Park y Park, marzo de 2026. Propusieron una arquitectura donde el consumo de memoria se mantiene constante O(1) independientemente de la longitud del contexto. Si esto escala, y eso es un si importante, la longitud de contexto deja de ser un problema de memoria. Imagina eso.

## Qwen 3.5 y el mito del modelo grande siempre necesario

A mí me llama la atención que nadie hable de lo que ha hecho Alibaba con Qwen. Los modelos Qwen 3.5, con variantes desde 0.5B hasta 32B parámetros, superan en múltiples benchmarks a modelos de tamaño comparable de OpenAI y Anthropic. La versión Qwen 3.5-72B-Instruct. Con un perfil de memoria que cabe en GPUs de consumo si usas cuantización adecuada.

No es magia. Es destilación de conocimiento: un modelo grande genera datos sintéticos, uno pequeño aprende de ellos. Si el proceso está bien diseñado, el modelo pequeño captura entre el 90% y el 95% del rendimiento del grande, consume diez veces menos memoria, y genera respuestas en una fracción del tiempo. Esto no es teoría, son resultados medidos. Lo interesante es que el resto de la industria está tardando en reaccionar.

También hay trabajo en modelos todavía más pequeños. Dikshit documentó en febrero de 2026 cómo modelos de 1B-3B parámetros cuantizados a 8 bits funcionan en dispositivos móviles para tareas de recuperación legal con latencias inferiores a 100ms. Cien milisegundos. En un móvil.

## Cuantización en 2026: no todo es igual

Acá necesito ser concreto porque hay mucha confusión.

GPTQ (Frantar et al., 2023) permite cuantizar a 3 y 4 bits con pérdidas controladas. Funciona con calibración sobre un dataset representativo y ajuste fino de los pesos para minimizar el error de reconstrucción. AWQ (Lin et al., 2024) protege los pesos más importantes para las activaciones, cuantizando solo los menos críticos. El resultado es mejor que GPTQ en el mismo nivel de bits. NF4, de Tim Dettmers y colaboradores, es un formato específico para datos con distribución normal —nuevos kernels publicados el 2 de abril de 2026 reducen la latencia de inferencia con NF4 hasta en un 40%.

| Técnica | Bits | Calidad vs FP16 | Velocidad | Cuándo usarla |
|---------|------|-----------------|-----------|---------------|
| FP16 | 16 | 100% | 1x | Baseline |
| INT8 | 8 | 98-99% | 1.5-2x | Producción estable |
| AWQ | 4 | 96-98% | 3-4x | GPU limitada |
| GPTQ | 4 | 95-97% | 3-4x | GPU limitada |
| NF4 | 4 | 96-98% | 3-5x | Muy limitado |
| 3-bit | 3 | 92-95% | 5-7x | Investigación |

Para producción donde la calidad importa: INT8 o AWQ 4-bit. Para memoria muy limitada: NF4 o AWQ 4-bit. Cuantización a 3 bits sigue siendo investigación activa, no lo uses en producción todavía.

## PagedAttention y EAGLE: las dos técnicas que importan ahora mismo

PagedAttention. La desarrolló el equipo de vLLM en Berkeley. Inspirada en gestión de memoria virtual de sistemas operativos. En lugar de allocate bloques contiguos de memoria para el KV cache, lo divide en páginas de 4 KB que pueden mapearse de forma no contigua. Esto permite compartición de páginas entre secuencias con prefijos compartidos —múltiples usuarios con el mismo prompt del sistema, por ejemplo—, asignación dinámica que evita desperdicio, y throughput hasta 24x superior a sistemas sin PagedAttention según sus benchmarks. En 2026, vLLM soporta LLaMA 3, Mistral, Mixtral, Qwen 3 y variantes instruct.

EAGLE es otra historia. Decodificación especulativa: un modelo pequeño propone varios tokens siguientes, el modelo grande los verifica en paralelo. Si la propuesta es correcta, ganas varios tokens por el precio de una sola evaluación del modelo grande. EAGLE trabaja al nivel de features en lugar de tokens, lo que simplifica la autoregresión. Logra 2.7x-3.5x de speedup en latencia para LLaMA2-Chat 70B. La gente de Yuhui Li et al. publicaron el paper original, y en febrero de 2026 salió P-EAGLE que extiende esto a modelos de razonamiento con outputs muy largos.

SGLang (Lianmin Zheng et al.) alcanza hasta 6.4x más throughput que sistemas del estado del arte gracias a RadixAttention, que reutiliza fragmentos del KV cache entre múltiples llamadas.

Ahora bien, y esto me parece importante señalarlo, un trabajo de marzo de 2026 —Liu, Yu, Park, Stoica, Cheung— cuestiona si los beneficios de la decodificación especulativa son reales en todos los escenarios. Argumentan que los speedups reportados asumen hardware específico y patrones de tráfico que no siempre se cumplen en producción. Merece atención ese paper.

## Lo que esto significa para la industria

La democratización ya está pasando. Modelos de 7B-13B cuantizados a 4 bits caben en una RTX 4090 con 24 GB de VRAM. Investigadores independientes, pequeñas empresas, desarrolladores individuales pueden experimentar con capacidades que hace dos años requerían clusters de GPUs costing cientos de miles de euros. No es teoría, es el presente.

Qualcomm y Apple ya integran NPUs capaces de ejecutar modelos de 3B parámetros a 30 tokens por segundo en smartphones. La combinación de modelos pequeños con cuantización agresiva está haciendo viable la inferencia en el borde de forma seria.

Los avances en gestión de KV cache permiten a sistemas de agentes mantener conversaciones de miles de turnos sin degradación. Agentes de IA que recuerdan interacciones протяженных over months —esto antes era impensable por las limitaciones de memoria.

Y la eficiencia energética. Menos memoria significa menos accesos a DRAM, menor consumo. En centros de datos sirviendo miles de millones de solicitudes diarias, esto se traduce en reducciones significativas de coste y huella de carbono. No es menor.

Lo que veo venir: sistemas heterogéneos. Modelos pequeños para consultas simples, escalado dinámico a modelos grandes cuando el reasoning lo requiere, gestión inteligente de memoria que mueve modelos entre CPU, GPU y almacenamiento según la demanda. No una solución única, sino la combinación adecuada según el caso.

La era de necesitar hardware de gama alta para acceder a capacidades avanzadas de IA se está cerrando. El ingenio algorítmico está ganando la batalla contra las limitaciones del silicio, y eso —la verdad— me parece una buena noticia para todos.

Si llegaste hasta aquí, probablemente ya estés pensando en qué modelo puedes meter en tu máquina. Yo empezaría por Qwen 3.5-7B con AWQ 4-bit y vLLM. Eso te da una idea de dónde estamos ahora mismo.
