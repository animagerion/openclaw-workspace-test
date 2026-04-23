# Cero Energético Ibérico — 28 de abril de 2025
## Guión de presentación — Versión 2

---

## SLIDE 1 — Portada

**Título:** Cero Energético Ibérico
**Subtítulo:** Análisis Causa — Función
**Fecha:** 28 de abril de 2025

**Narrativa:**
«El 28 de abril de 2025, a las 12:33 CEST, el sistema eléctrico peninsular español y portugués sufrió el mayor incidente registrado en más de veinte años. Este documento analiza, de forma estructurada y basada en los informes oficiales publicados, qué ocurrió ese día, por qué ocurrió, cuál era el papel de cada actor implicado, y cómo ambas dimensiones — causa y función — se relacionan entre sí.»

**Diseño:**
- Fondo oscuro (gradiente rojo oscuro / negro)
- Logo de Élan Forensic arriba a la izquierda
- Título en blanco, subtítulo en dorado
- Línea accent naranja

---

## SLIDE 2 — Los hechos: contexto del sistema

**Título:** El estado del sistema antes del incidente

**Narrativa:**
«Para comprender lo que ocurrió necesitamos entender cómo estaba el sistema esa mañana. Era un lunes de primavera sin acontecimientos meteorológicos singulares. La demanda se situaba en niveles normales para la época del año.

Sin embargo, el sistema presentaba tres características que lo hacían especialmente vulnerable.

Primera: una penetración de generación renovable extraordinariamente alta. El 70 por ciento de la electricidad que se producía en ese momento venía de fuentes no síncronas — principalmente paneles solares y, en menor medida, aerogeneradores. Estas tecnologías dependen de convertidores electrónicos, no de generadores mecánicos. Eso altera significativamente la forma en que el sistema responde a perturbaciones.

Segunda: un parque convencional muy mermado. Por mantenimiento, revisiones e indisponibilidades, estaban fuera de servicio 7.400 MW de ciclo combinado, 3.000 MW nucleares, 1.400 MW de bombeo y prácticamente toda la capacidad de fuel-gas. Quedaban solo 11 grupos síncronos operativos, cuando lo habitual son entre 30 y 50. Esto reducía drásticamente la inercia del sistema — su capacidad de absorber perturbaciones.

Tercera: ya se habían producido episodios de sobretensión en días previos. El 16, el 22 y el 24 de abril se habían registrado picos de tensión que activaron protecciones en plantas solares del sur. Las plantas de Cáceres y Cuenca, con 739 MW combinados, ya se habían desconectado el día 22. Volvieron a hacerlo el 28.»

**Datos clave:**
- 70% generación no síncrona
- 11 grupos síncronos operativos (normal: 30-50)
- 2,3 segundos de inercia (mínimo de referencia: 2s)
- Episodios de sobretensión los días 16, 22 y 24 de abril

**Diseño:**
- Fondo claro
- Barra horizontal de colores mostrando mix energético: 59% amarillo solar, 11% azul verdoso eólica, 10% gris nuclear, resto otros
- Dos columnas: narrativa izquierda, datos derecha
- Warning callout: episodios de sobretensión previos en borde naranja

---

## SLIDE 3 — Los hechos: las oscilaciones previas

**Título:** Las oscilaciones previas al cero

**Narrativa:**
«Treinta minutos antes del colapso, el sistema atravesó dos episodios de oscilaciones de baja frecuencia que los informes consideran relevantes como señal de alerta.

Entre las 12:03 y las 12:07, se registró una oscilación de frecuencia en torno a 0,63 hercios — la península ibérica oscilaba desfasada respecto al resto del sistema eléctrico europeo. La amplitud llegó a 70 milihercios. El amortiguamiento tardó casi cinco minutos en reducir la oscilación a niveles inapreciables.

Un segundo episodio comenzó hacia las 12:19. La frecuencia de la oscilación bajó a aproximadamente 0,2 hercios — un modo de oscilación diferente, que involucra el este y el centro-oeste del sistema europeo. La amplitud llegó a 200 milihercios y el tiempo de amortiguamiento fue de más de tres minutos.

Durante este período, las tensiones en la red de 400 kilovoltios se mantenían dentro del rango operativo pero con tendencia al alza. El operador del sistema pidió la puesta en marcha de ciclos combinados para dar soporte de tensión en el sur peninsular, pero los tiempos de arranque de estos grupos — superiores a noventa minutos — hacían imposible tenerlos disponibles antes del incidente.

El cambio de modo de control del enlace HVDC España-Francia — de emulación de corriente alterna a potencia constante— pudo haber debilitado el acoplamiento síncrono con el continente.»

**Datos clave:**
- 12:03-12:07: oscilación 0,63 Hz, amplitud 70 mHz, 4m 42s de amortiguamiento
- 12:19-12:22: oscilación 0,2 Hz, amplitud 200 mHz, 3m 20s de amortiguamiento
- Tensiones en 400 kV dentro de rango pero en tendencia al alza

**Diseño:**
- Fondo claro
- Dos bloques lado a lado, uno por episodio
- Fechas y horas en naranja
- Nota al pie: la relación entre oscilaciones y el incidente se analiza en la sección de causas

---

## SLIDE 4 — Los hechos: la cronología del colapso

**Título:** La cronología del colapso

**Narrativa:**
«Vamos ahora a la secuencia precisa de lo que ocurrió en menos de un minuto.

A las 12:32:57 — treinta y tres minutos después del mediodía — se produjo la primera desconexión. En la zona de Granada, se desconectaron instalaciones fotovoltaicas por un total de 355 MW de potencia activa y 165 MVAr de absorción de reactiva. Simultáneamente, se registran desconexiones adicionales de plantas solares en Badajoz, Cáceres, Cuenca, Sevilla y Huelva, además de una instalación ferroviaria de ADIF en Cartagena. En esta primera fase se perdieron entre 355 y algo más de 700 MW según las distintas fuentes.

A las 12:33:16, segunda pérdida: una caída de aproximadamente 730 MW en menos de dos segundos, asociada a nuevas desconexiones de renovable. La frecuencia del sistema cayó unos 55 milihercios sin llegar a recuperarse.

A las 12:33:20, el punto de no retorno. La interconexión con Francia, que hasta ese momento importaba electricidad para equilibrar la península, alcanzó su máximo de importación: 3.807 MW. En apenas 260 milisegundos, el flujo se invirtió. Pasó a exportar 5.587 MW — una configuración físicamente inviable que provocó que las protecciones de sincronismo dispararan.

En una ventana de apenas 400 milisegundos — entre las 12:33:20,180 y las 12:33:20,520 — la frecuencia cayó por debajo de 49,50 hercios, la interconexión con Francia invirtió su flujo y se perdió el sincronismo con el continente de forma simultánea.

A las 12:33:24, el sistema peninsular quedó a oscuras. Portugal, Francia, Marruecos y las Islas Baleares quedaron aisladas o desconectadas.

La frecuencia mínima registrada fue de 47,79 hercios. Las sobretensiones en la red alcanzaron picos de 456 kilovoltios en la red de 400 kV — un 14 por ciento por encima de lo nominal.»

**Datos clave:**
- 12:32:57 → ~355-700 MW perdidos (fase 1)
- 12:33:16 → ~730 MW perdidos (fase 2)
- 12:33:20 → Inversión del flujo Francia: 3.807 MW import → 5.587 MW export
- 12:33:24 → Colapso total del sistema

**Diseño:**
- Fondo claro
- Timeline vertical con 4 hitos con marca temporal exacta
- Línea gradient naranja→rojo representando la escalada
- Columna derecha con datos: frecuencia mínima 47,79 Hz, sobretensión 456 kV
- Usar color para distinguir gravedad creciente

---

## SLIDE 5 — Los hechos: la reposición del servicio

**Título:** La reposición del servicio

**Narrativa:**
«Tras el colapso, el sistema pasó quince horas y media en proceso de reposición en España y doce horas en Portugal. Los principales hitos fueron los siguientes.

A las 13:04, apenas treinta minutos después del cero, Marruecos empezó a aportar soporte: 100 MW desde el sistema marroquí a través de la interconexión.

A las 15:59, el enlace HVDC con Francia comenzó a transmitir potencia. A las 17:49 se unificaron las islas Duero y País Vasco. Progresivamente, isla a isla, el sistema fue recuperándose.

A las 21:32, twentyún grupos térmicos estaban sincronizados y aproximadamente el 50 por ciento de la demanda había sido recuperada. Hacia las cuatro de la madrugada del día 29, la reposición en España se dio por completada.

Los informes concurren en que, pese a la magnitud del incidente, el plan de reposición funcionó sin incidentes operativos de segundo orden.»

**Diseño:**
- Fondo claro
- Timeline horizontal o vertical con hitos clave
- Datos: 13:04 primer soporte externo, 15:59 HVDC Francia, 21:32 50% demanda recuperada, 04:00 reposición completa
- Callout verde: reposición sin incidentes secundarios

---

## SLIDE 6 — Las causas: desencadenante

**Título:** Causa 1 — La pérdida en cascada de generación renovable

**Narrativa:**
«La primera causa identificada por todos los informes es la desconexión sucesiva y parcialmente simultánea de instalaciones de generación renovable, predominantemente fotovoltaicas, en el sur y suroeste peninsular.

Las protecciones de las plantas solares actuaron correctamente — estavam configuradas para desconectar cuando la tensión superaba ciertos umbrales. Lo que no debería haber ocurrido era que la tensión cruzara esos umbrales. Pero los días previos habían acumulado un nivel de tensión elevado en la red de transporte, y las actuaciones del operador esa mañana — como la reconexión de once líneas de transporte para aumentar la capacidad de absorción de reactiva — tuvieron el efecto colateral de elevar aún más las tensiones, acercándolas a los umbrales de protección.

El resultado fue una pérdida escalonada. Cada desconexión modificaba el balance local de reactiva, elevando las tensiones y disparando las protecciones de las plantas vecinas. Fue un bucle de realimentación positiva: pérdida genera más tensión, más tensión genera más pérdida.

Las plantas de Cáceres y Cuenca, con 739 MW combinados, ya habían sufrido exactamente la misma desconexión el día 22 de abril. Su recurrencia apunta a una vulnerabilidad identificada con antelación y no corregida.»

**Datos clave:**
- Desconexiones en cadena por activación de protecciones de sobretensión
- Tres escalones en aproximadamente 20 segundos
- Pérdidas acumuladas: entre 1.600 y 2.200 MW
- Las plantas de Cáceres y Cuenca se habían desconectado el 22 de abril por la misma causa

**Diseño:**
- Fondo claro
- Una sola columna con narrativa completa
- Borde izquierdo naranja para la tarjeta
- Datos clave destacados en naranja

---

## SLIDE 7 — Las causas: control de tensión

**Título:** Causa 2 — El control de tensión y la gestión de potencia reactiva

**Narrativa:**
«La segunda causa es estructural y tiene varias dimensiones.

La primera dimensión es la saturación de la capacidad de absorción de reactiva. La potencia reactiva es la que controla los niveles de tensión en la red. Si no hay suficiente capacidad para absorberla, las tensiones se disparan. En el momento del incidente, la capacidad de absorción de reactiva del sistema estaba была близка к saturación — las reactancias estaban aprovechadas al 80 por ciento. En la zona de Andalucía — donde se iniciaron las desconexiones — la capacidad de absorción de los grupos síncronos era de apenas 117 MVAr, frente a 1.850 MVAr de reactancias. Era un desequilibrio territorial grave.

La segunda dimensión es que la generación renovable, por el marco regulatorio vigente entonces, no podía hacer control dinámico de tensión. El procedimiento de operación P.O. 7.4 articulaba el soporte de tensión principalmente en torno a la generación síncrona. Las plantas fotovoltaicas y eólicas tenían requerimientos de factor de potencia fijo — básicamente estaban obligadas a mantener un perfil de reactiva estático, sin capacidad de responder dinámicamente ante perturbaciones. Esto dejaba la respuesta de control de tensión casi exclusivamente en manos del parque síncrono, que ese día era numéricamente muy reducido.

La tercera dimensión es la visibilidad. El operador del sistema no disponía de visibilidad integrada en tiempo real sobre la inyección y absorción de reactiva en la red de distribución. No podía anticipar con precisión dónde estaban los desequilibrios.»

**Datos clave:**
- Capacidad de reactivas instalada: 13.300 MVAr, aprovechada al ~80%
- Capacidad de absorción grupos síncronos en Andalucía: solo 117 MVAr
- Las renovables no podían hacer soporte dinámico de tensión (P.O. 7.4)
- Sin visibilidad integrada de reactiva en distribución

**Diseño:**
- Fondo claro
- Grid de 3 tarjetas con datos numéricos destacados
- Borde naranja izquierdo en cada tarjeta

---

## SLIDE 8 — Las causas: oscilaciones y reservas

**Título:** Causa 3 — Oscilaciones no amortiguadas y Causa 4 — Reservas y programación insuficientes

**Narrativa:**
«La tercera causa son las oscilaciones de baja frecuencia de los treinta minutos previos. Los estabilizadores de sistema de potencia — los PSS — que incorporan los reguladores de tensión de los grupos síncronos están diseñados para amortiguar oscilaciones en bandas entre 0,1 y 1,0 hercios. Pero su efectividad depende del número y la ubicación de los grupos síncronos acoplados. Con solo once grupos operativos, la capacidad de amortiguamiento sistémico era muy inferior a la habitual.

La cuarta causa es la configuración de reservas y programación. El mercado eléctrico diario había cerrado sin ciclos combinados despachados. El operador del sistema tuvo que forzar su entrada por Restricciones Técnicas por motivos de seguridad, pero las reoptimizaciones de la mañana redujeron ese volumen progresivamente. Cuando a las 12:18 se identificó la necesidad de refuerzos en el sur, los九十 minutos de tiempo de arranque hacían imposible desplegarlos a tiempo.

Además, los errores de previsión de generación renovable habían alcanzado el 36 por ciento en las horas previas. El sistema estaba funcionando con una imagen de la realidad muy alejada de la realidad.»

**Datos clave:**
- Oscilaciones 0,63 Hz y 0,2 Hz no amortiguadas con eficacia
- Mercado diario sin ciclos combinados
- 90+ minutos para arrancar un ciclo combinado
- Error de previsión renovable: hasta 36%

**Diseño:**
- Fondo claro
- Dos columnas, una por causa
- Borde naranja izquierdo en cada columna

---

## SLIDE 9 — Las funciones: mapa de actores

**Título:** Funciones de los actores del sistema

**Narrativa:**
«Vamos ahora a las funciones. Esta sección describe, con carácter general pero aplicado al día 28 de abril, cuál era el papel de cada actor del sistema eléctrico según el marco regulatorio y contractual vigente ese día.

El operador del sistema — REE — tenía la responsabilidad de gestionar el equilibrio entre generación y demanda en tiempo real, garantizar la seguridad del sistema, aplicar los procedimientos de Restricciones Técnicas, supervisar la tensión en la red de transporte, y coordinar la activación de los planes de defensa y reposición.

La CNMC — la Comisión Nacional de los Mercados y la Competencia — era la autoridad regulatoria. Le correspondía aprobar y supervisar los procedimientos de operación del sistema, incluido el P.O. 7.4 sobre control de tensión, y el diseño de los servicios de ajuste.

Los generadores — compañías eléctricas con instalaciones de producción — tenían la obligación de cumplir los requisitos técnicos de conexión a red, ajustar sus protecciones a los parámetros establecidos por el operador, y responder a las órdenes de despacho.

Los comercializadores y consumidores tenían la obligación de participar en los mercados de electricidad con sus programas de producción y consumo.

El enlace HVDC con Francia y con Marruecos tenía protocolos de funcionamiento definidos que incluían la actuación automática ante perturbaciones del sistema.

Cada actor tenía un rol delimitado. El marco regulatorio definía quién hacía qué.»

**Diseño:**
- Fondo claro
- Grid de 4-5 tarjetas con icono y descripción breve de cada actor
- Borde superior coloreado para distinguir actores (rojo=RREE, dorado=CNMC, gris=generadores, blanco=comercio)
- Texto conciso, una tarjeta por actor

---

## SLIDE 10 — La relación causa-función: la matriz

**Título:** Relación Causa — Función

**Narrativa:**
«Ahora cruzamos ambas dimensiones. Para cada causa, identificamos qué función del marco regulatorio estaba implicada y, por tanto, qué actor tenía responsabilidad funcional en esa área.

Sobre la desconexión en cascada por sobretensión: la función de gestión de restricciones técnicas y control de tensión era responsabilidad del operador del sistema.

Sobre el diseño del control de tensión: el P.O. 7.4 había sido aprobado por la CNMC. La función regulatoria de diseño del servicio de control de tensión recaía en la autoridad regulatoria.

Sobre la programación sin ciclos combinados y la insuficiencia de reservas: de nuevo el operador del sistema, en su función de garantía de seguridad y despacho económico.

Sobre la vulnerabilidad latente identificada el 22 de abril y no resuelta antes del 28: las funciones de vigilancia y propuesta de mejora regulatoria correspondían tanto a REE como a la CNMC.

Sobre las limitaciones de la generación no síncrona para el control dinámico de tensión: nos encontramos ante una característica del diseño del marco técnico de conexión, que involucra al regulador y al operador jointly.

Este análisis no establece responsabilidad individual ni corporativa. Muestra la relación estructural entre las causas del incidente y las funciones que el marco regulatorio atribuía a cada actor ese día. Es un mapa, no un veredicto.»

**Datos clave — Matriz:**

| Causa | Función implicada | Actor |
|---|---|---|
| Desconexiones por sobretensión | Gestión de restricciones técnicas y control de tensión | Operador del sistema (REE) |
| Diseño del P.O. 7.4 — control de tensión | Regulación del servicio de control de tensión | CNMC |
| Programación sin ciclos combinados | Garantía de seguridad y despacho | Operador del sistema (REE) |
| Vulnerabilidad identificada no resuelta | Vigilancia y mejora regulatoria | REE + CNMC |
| Limitaciones de renovables en control de tensión | Diseño técnico de conexión a red | Regulador + Operador |

**Diseño:**
- Fondo claro
- Tabla con 3 columnas: Causa | Función | Actor
- Badges de colores: REE en naranja, CNMC en dorado, ambos en rojo, marco regulatorio en gris
- Título de sección en cursiva arriba y abajo de la narrativa de cierre

---

## SLIDE 11 — Fuentes y metodología

**Título:** Fuentes y metodología

**Narrativa:**
«Este análisis se basa exclusivamente en los informes oficiales publicados.

Fuentes primarias: el Informe del Comité de Análisis del Gobierno de España, el informe factual y el informe final de ENTSO-E, el informe técnico de REE de junio de 2025, y el informe de la CNMC.

Análisis técnicos adicionales: NREL — laboratorio del Departamento de Energía de Estados Unidos—, la Universidad Friedrich-Alexander-Universität, y Compass Lexecon e INESC TEC, encargado por la asociación empresarial del sector.

Marco normativo: Reglamento (UE) 2017/1485, procedimientos de operación del sistema español vigentes el 28 de abril de 2025.

El orden de prelación entre fuentes ha sido: informes oficiales colegiados primero, informes técnicos de los actores con competencia directa después, análisis académicos y, finalmente, análisis de parte. Cuando existen divergencias relevantes entre fuentes, se reflejan expresamente en el texto.

Este documento no constituye investigación propia ni juicio de responsabilidad.»

**Diseño:**
- Fondo claro
- Grid de 3 columnas: Fuentes oficiales | Análisis académicos | Marco normativo
- Disclaimer pequeño en cursiva al final

---

## Estructura narrativa

| Fase | Slides | Narrativa |
|---|---|---|
| Apertura | 1 | Introducción al análisis |
| Los hechos | 2-5 | Qué ocurrió: contexto → oscilaciones previas → cronología → reposición |
| Las causas | 6-8 | Por qué ocurrió: desencadenante → control de tensión → oscilaciones y reservas |
| Las funciones | 9 | Quién hacía qué |
| Relación causa-función | 10 | El cruce: cómo se relacionan las causas con las funciones |
| Cierre | 11 | Fuentes y metodología |

**Errores a evitar:**
- No recargar las slides de texto — usar la narrativa hablada para el detalle, las slides para la estructura y los datos clave
- La matriz causa-función es el climax: dedicarle el tiempo que merece
- Evitar entrar en debate sobre quién tiene la culpa — el análisis es estructural
