# Resistencia Bacteriana a los Antibióticos: Mecanismos Moleculares y Estructura Genética

**Guía completa para ponencia — 60 minutos**
*Dirigida a: Bióloga molecular y bioquímica experta en bacterias recuperadoras de tierras degradadas*

**Contexto:** Enfocada en biología molecular de la resistencia: mecanismos, estructura genética y evolución en el contexto de suelos degradados.

---

## ÍNDICE DE LA PONENCIA

| # | Sección | Tiempo |
|---|---|---|
| 1 | Prólogo: la pregunta molecular | 5 min |
| 2 | Anatomía molecular de la resistencia: los cinco mecanismos | 18 min |
| 3 | Arquitectura genética: plásmidos, transposones e integrones | 12 min |
| 4 | Evolución en tiempo real: velocidad y selección | 8 min |
| 5 | El suelo degradado como observatorio molecular | 12 min |
| 6 | Cierre | 5 min |
| | **TOTAL** | **60 min** |

---

## 1. PRÓLOGO: LA PREGUNTA MOLECULAR

**Tiempo:** 5 minutos

### Desarrollo

**[Titular de apertura]**
Hay una pregunta que merece una respuesta precisa:

*¿Qué está pasando — literalmente — dentro de cada bacteria resistente que vemos?*

No desde el punto de vista clínico. No desde el punto de vista ambiental. Sino a nivel molecular: qué enzima está produciendo, qué gen la codifica, cómo se lo ha conseguido, y por qué la evolución tuvo millones de años para perfeccionar este sistema.

Esta es la pregunta de una bióloga molecular. Y es donde vamos a pasar los próximos 55 minutos.

**[Mapa de la sesión]**
Vamos a hacer cuatro cosas:
1. Desmontar una bacteria resistente pieza por pieza — los cinco mecanismos moleculares reales
2. Ver cómo se organizan esos mecanismos genéticamente — la arquitectura del ADN resistente
3. Entender la velocidad del problema — selección, replicación, evolución en tiempo real
4. Mirar el suelo degradado como un laboratorio natural donde podemos estudiar esto

Vamos a hablar de cómo funciona la máquina de la resistencia — y de lo que pasa cuando la miramos con ojos de bióloga molecular.

---

## 2. ANATOMÍA MOLECULAR DE LA RESISTENCIA: LOS CINCO MECANISMOS

**Tiempo:** 18 minutos

### Desarrollo

Cada bacteria resistente emplea una combinación de cinco mecanismos. Los detallo con dianas moleculares concretas, porque eso es lo que diferencia esta sección de cualquier otra charla del día.

---

#### 2.1. Inactivación enzimática

La bacteria produce una enzima que destroza o modifica el antibiótico antes de que alcance su diana.

**Beta-lactamasas — el caso paradigmático**

El anillo beta-lactámico es la estructura central de penicilinas, cefalosporinas, monobactámicos y carbapenémicos. Las beta-lactamasas rompen ese anillo por hidrólisis.

Clasificación funcional de Ambler:

- **Clase A** (serina-proteasas): TEM, SHV, CTX-M, KPC. La familia **CTX-M** es ahora la más diseminada globalmente en enterobacterias. Desproporcionadamente activa contra cefalosporinas de tercera generación.
- **Clase B** (metalo-beta-lactamasas, requieren zinc): NDM-1, VIM-1, IMP-1. Confieren resistencia a prácticamente todos los beta-lactámicos excepto aztreonam. El gen **NDM-1** (*New Delhi Metallo-beta-lactamase*) se detectó primero en India y se ha globalizado en menos de una década.
- **Clase C** (AmpC): cefalosporinasa cromosómica o adquirida. Hidroliza cefalosporinas de tercera generación y es inducible.
- **Clase D** (OXA): OXA-48, OXA-181. Particularmente preocupantes en *Klebsiella*. Resisten a carbapenémicos.

**Enzimas modificadoras de aminoglicósidos:**
- **Acetiltransferasas (AAC)**: acetilan grupos amino del antibiótico
- **Fosfotransferasas (APH)**: fosforilan grupos hidroxilo
- **Nucleotidiltransferasas (ANT)**: adenilan grupos hidroxilo

Resultado: el antibiótico entra en la bacteria pero deja de funcionar antes de llegar al ARNr 16S, su diana.

**Esterasas de macrólidos y cloranfenicol acetiltransferasas:** modificaciones similares en otros grupos de antibióticos.

---

#### 2.2. Modificación de la diana

La bacteria altera la molécula contra la que va dirigido el antibiótico. El fármaco ya no reconoce su objetivo.

**Substitución de PBP (Penicillin-Binding Protein):**

Los beta-lactámicos se unen a las PBPs para inhibir la síntesis de pared celular. *Staphylococcus aureus* resistente a meticilina (MRSA) tiene el gen *mecA* — que codifica **PBP2a**, una PBP funcionalmente equivalente a la normal pero con tal baja afinidad por los beta-lactámicos que estos no pueden unirse. La bacteria sintetiza pared celular normal aunque el antibiótico esté presente.

La PBP2a trabaja con el complejo celular de síntesis de peptidoglicano intacto. Los beta-lactámicos se quedan fuera.

**Metilación del ARNr 16S:**

Los aminoglicósidos se unen al ARNr 16S de la subunit 30S del ribosoma. Ciertas bacterias adquieren genes *rmt* o *armA* que codifican metiltransferasas que añaden un grupo metilo en la posición A1408 del ARNr 16S. Esto bloquea estereicamente la unión del antibiótico. El ribosoma sigue funcionando, pero el antibiótico ya no entra.

**Mutaciones en topoisomerasas (gyrA, parC):**

Las quinolonas inhiben la ADN girasa (GyrA) y la topoisomerasa IV (ParC). Mutaciones puntuales en los genes *gyrA* y *parC* — frecuentemente en un dominio concreto llamado **QRDR (Quinolone Resistance Determining Region)** — alteran la estructura de la enzima lo suficiente para impedir la unión del antibiótico sin destruir la función enzimática.

Una sola mutación en *gyrA* ya confiere nivel bajo de resistencia. Dos o tres mutaciones superpuestas en *gyrA* y *parC* producen resistencia de alto nivel.

**Proteínas de fusión MCR:**

La colistina es el antibiótico de último recurso para infecciones por Gram-negativos multirresistentes. El gen **mcr-1** (*Mobile Colistin Resistance*) codifica una fosfoetanolamina transferasa que modifica el lipopolisacárido (LPS) de la membrana externa, reduciendo la unión de la colistina. Se detectó primero en China (2015) en cerdos, y en menos de dos años se había globalizado.

Lo notable de MCR: es un gen móvil — viaja en plásmidos. La resistencia a colistina, antes unimous, ahora se transmite horizontalmente.

---

#### 2.3. Reducción de la permeabilidad de membrana

Las bacterias Gram-negativas tienen una membrana externa con canales acuosos llamados **porinas**. Estos canales dejan pasar antibióticos hidrofílicos de bajo peso molecular.

La bacteria puede reducir la entrada de dos formas:
- **Downregulation de porinas**: reducir el número de canales expresados
- **Mutación del canal**: cambiar el diámetro o la selectividad de carga para excluir el antibiótico

Ejemplo clásico: *Pseudomonas aeruginosa* reduce la expresión de **OprD**, la porina específica para carbapenémicos. Cuando OprD desaparece, los carbapenémicos no tienen forma de entrar. La bomba de eflujo + la pérdida de OprD = resistencia intrínseca a carbapenémicos.

Esto no es un mecanismo de resistencia "activo" en el sentido de destruir el antibiótico. Es más sutil: la bacteria simplemente cierra la puerta.

---

#### 2.4. Bombas de eflujo (efflux pumps)

Las bombas de eflujo son proteínas transmembrana que expulsan activamente antibióticos de la célula contra un gradiente de concentración. Requieren energía (ATP o fuerza protón-motriz).

Lo crítico sobre estas bombas: son **inespecíficas**. Una misma bomba puede exportar beta-lactámicos, tetraciclinas, macrólidos, fluoroquinolonas y metales pesados simultáneamente. Sobreexpresar una bomba RND confiere resistencia a múltiples clases de antibióticos a la vez.

Familias principales:
- **RND (Resistance-Nodulation-Division)**: sistemas tripartito (bomba + proteína de fusión + porina). Ejemplo: *MexAB-OprM* en *P. aeruginosa*. Confiere multirresistencia.
- **MFS (Major Facilitator Superfamily)**: ejemplos: TetA (tetraciclina), MdfA.
- **SMR (Small Multidrug Resistance)**: pequeños transportadores que funcionan como dímeros.
- **ABC (ATP-Binding Cassette)**: usan ATP directamente.

**Interés evolutivo:** algunas bombas de eflujo son cromosomicas y se expresan normalmente a niveles bajos (house-keeping). Cuando hay presión selectiva por antibióticos, la bacteria puede sobre-expresarlas mediante mutaciones regulatorias. Esto convierte una función normal de detoxificación celular en un mecanismo de resistencia.

---

#### 2.5. Metabolismo bypass

La bacteria substituye la enzima inhibida por una versión que funciona aunque el antibiótico esté presente.

El ejemplo más elegante es la resistencia a sulfonamidas. Las sulfonamidas inhiben la enzima *DHPS* (dihidropteroato sintasa) en la vía de síntesis del ácido fólico. Algunas bacterias adquieren un gen *folP* resistente que codifica una DHPS que no liga la sulfonamida pero sigue sintetizando folato. La vía sintética sigue funcionando por un camino alternativo.

Esto no deshace el daño. Lo evita. La bacteria mantiene su metabolismo mientras el antibiótico falla en su diana.

**[Momento visual sugerido]**
Un diagrama central con una bacteria como hub y los cinco mecanismos como ramas independientes — no como una lista, sino como un sistema integrado donde la bacteria puede activar varios a la vez.

**Apoyo visual para público mixto:** Si la audiencia no es toda de microbiólogos, cada mecanismo gana mucho con una metáfora visual sencilla:
- **Inactivación enzimática** → un cortasetos cortando el anillo beta-lactámico
- **Modificación de diana** → una cerradura cuya llave ya no encaja
- **Reducción de permeabilidad** → una puerta que se cierra con llave
- **Bombas de eflujo** → una bomba de achique en un barco (saca el antibiótico más rápido de lo que entra)
- **Metabolismo bypass** → un desvío en la carretera: el tráfico fluye por otra ruta aunque el puente esté cortado

---

## 3. ARQUITECTURA GENÉTICA: PLÁSMIDOS, TRANSPOSONES E INTEGRONES

**Tiempo:** 12 minutos

### Desarrollo

Los mecanismos moleculares existen como genes. Los genes viven en estructuras genéticas. Entender cómo se organizan esas estructuras es clave para entender por qué la resistencia se disemina tan rápido.

---

#### 3.1. Plásmidos: los vectores de la multirresistencia

Los plásmidos son moléculas circulares de ADN extracromosómico que se replican de forma independiente. Tienen su propio origen de replicación, genes de partición, y a menudo genes de resistencia.

Lo que hace a los plásmidos especiales en la resistencia:

**Replicón:** cada plásmido tiene una secuencia de inicio de replicación que determina su compatibilidad. Dos plásmidos con el mismo replicón no pueden coexistir establemente en la misma célula. Esto define los grupos de incompatibilidad (Inc).

**Plásmidos multirresistencia:**
Un solo plásmido puede portar múltiples genes de resistencia simultáneamente.
- **IncF**: porta *blaCTX-M*, *blaTEM*, *qnrS*, *aac(6')-Ib-cr*. Un plásmido, cinco resistencias.
- **IncHI1**: asociados con *Salmonella* Typhi multirresistente.
- **IncA/C**: amplio rango de hospedador, encontrado en enterobacterias clínicas y ambientales.

**Conjugación:**
Los plásmidos pueden transferirse de una bacteria a otra mediante el sistema de apareamiento (pili F). Una bacteria donadora con un plásmido multirresistencia puede copiarlo y pasarlo a una receptora en minutos. La nueva bacteria expresa todos los genes simultáneamente.

Los plásmidos son el vehículo más eficiente de diseminación horizontal. Y lo que los hace realmente peligrosos es que no respetan fronteras entre especies: un plásmido que nace en *Klebsiella* puede terminar en *E. coli* intestinal humana sin que ninguna de las dos lo "quiera".

---

#### 3.2. Transposones: genes saltarines

Los transposones son secuencias de ADN capaces de moverse de una posición a otra dentro del genoma, o de un plásmido a un cromosoma y viceversa.

**Estructura:**
- Secuencias de inserción (IS) en los extremos
- Gen(es) de resistencia en el medio
- Gen(es) de la transposasa que cataliza el corte y pegado

**Transposones compuestos:**
Incluyen dos IS flanqueando un bloque de genes de resistencia. Son especialmente móviles porque cada IS puede actuar como punto de recombinación, permitiendo que todo el bloque salte junto.

Los transposones pueden capturar genes de resistencia de un plásmido e insertarlos en el cromosoma, haciéndolos estables y perpetuos. Una bacteria que "aprende" un transposón de resistencia lo guarda para siempre, incluso si pierde el plásmido original.

---

#### 3.3. Integrones: las fábricas de multirresistencia

Los integrones son sistemas de recombinación sitio-específica que capturan y expresan casetes genéticos. A diferencia de los transposones, no se mueven solos — necesitan transposasas o otros elementos para su movilidad.

**Estructura:**
- Gen *intI* (integrasa)
- Sitio de recombinación *attI*
- Promotor para expresar los casetes capturados

**Casetes genéticos:**
Cada casete es un pequeño ORF circular con un gen de resistencia y un sitio *attC*. Cuando la integrasa recombina un casete en el integrón, el gen se expresa bajo el promotor común. Los casetes se apilan: un integrón puede acumular múltiples casetes.

**Integrones de clase 1, 2 y 3** están fuertemente asociados con multirresistencia clínica. Contienen casetes para cefalosporinas (*bla*), aminoglicósidos (*aad*), Trimetoprim (*dfr*), sulfonamidas (*sul*).

**Transducción (30 segundos):**
Existe un tercer mecanismo de transferencia horizontal además de la conjugación: la **transducción**. Los bacteriófagos (virus que infectan bacterias) pueden encapsidar fragmentos de ADN bacteriano accidentalmente durante su ciclo lítico y transferirlos a la siguiente célula que infectan. En suelos, los fagos son las entidades biológicas más abundantes del planeta — se estima que hay 10³⁰ partículas fágicas globalmente, y cada gramo de suelo puede contener 10⁸ partículas víricas. Esto los convierte en vectores invisibles pero constantes del movimiento de genes de resistencia en el ambiente. La transducción es menos relevante que la conjugación para la diseminación clínica, pero es central en el resistoma del suelo.

**[Comparativa visual sugerida]**

| Elemento | ¿Se mueve solo? | ¿Cuántos genes puede portar? | ¿Dónde vive? |
|---|---|---|---|
| Plásmido | Sí (conjugativo) | Múltiples simultáneamente | Citoplasma |
| Transposón | No solo, requiere transposasa | 1-3 típicamente | Cromosoma o plásmido |
| Integrón | No solo, necesita ayuda | Múltiples en stack | Cromosoma o plásmido |

Los tres elementos pueden combinarse: un plásmido portador de un transposón que a su vez porta un integrón. Eso es una estructura de multirresistencia real — los genes se apilan jerárquicamente.

---

## 4. EVOLUCIÓN EN TIEMPO REAL: VELOCIDAD Y SELECCIÓN

**Tiempo:** 8 minutos

### Desarrollo

**[Pregunta provocadora]**
¿Cuánto tiempo tarda una bacteria en adquirir resistencia?

Respuesta: segundos.

**4.1. La matemática de la resistencia**

Una bacteria se divide cada 20 minutos en condiciones óptimas. Eso significa:
- 1 bacteria → 1.000 en menos de 7 horas
- 1 bacteria → 1.000.000 en menos de 14 horas

Cada división es una oportunidad de mutación. Y si la población es de 10⁹ UFC en una infección, las mutaciones raras (10⁻⁸ por gen por división) ocurren miles de veces por turno.

La selección no es un proceso lento. En una infección que dura días, hay suficientes generaciones para que la resistencia emerja incluso antes de que el tratamiento termine.

**4.2. Coste de fitness y compensación**

Adquirir resistencia tiene un coste. Las bombas de eflujo consumen energía. Las enzimas modificadoras necesitan recursos. Las PBPs alternativas pueden ser menos eficientes.

Pero las bacterias compensan. Mutaciones compensatorias en otros genes pueden restaurar el fitness perdido mientras mantienen la resistencia. Esto significa que una vez que la resistencia se establece, no desaparece aunque se retire el antibiótico.

**4.3. Fenotipos mutadores**

Algunas bacterias crónicamente dañadas genómicamente (mutadores, con defectos en MMR — *mutS*, *mutL*) tienen tasas de mutación 100-1.000 veces mayores. En entornos con antibióticos (hospitales, suelos contaminados), estas cepas generan resistencia más rápido. Son puntos calientes de evolución.

**4.4. Coselección**

Cuando un suelo está contaminado con metales pesados (arsénico, cadmio, mercurio), las bacterias que sobreviven a esos metales frecuentemente portan genes de resistencia a metales y antibióticos en los mismos plásmidos. Seleccionar por uno significa seleccionar por todos.

Esto es relevante para la investigación en tierras degradadas: un suelo contaminado por metales pesados puede estar seleccionando inadvertidamente bacterias con multirresistencia.

---

## 5. EL SUELO DEGRADADO COMO OBSERVATORIO MOLECULAR

**Tiempo:** 12 minutos

### Desarrollo

Esta es la sección donde la experiencia en recuperación de tierras degradadas se encuentra con la biología molecular de la resistencia.

---

#### 5.1. El microbioma del suelo como reservorio de resistencia

El suelo tiene la mayor diversidad bacteriana del planeta: 10⁸-10⁹ UFC por gramo, miles de especies diferentes. Gran parte de esa diversidad no está cultivable en laboratorio — solo accesible por secuenciación metagenómica.

Estudios de secuenciación shotgun en suelos prístinos han identificado homólogos de genes de resistencia clínica (*blaTEM*, *blaCTX-M*, *qnr*) en comunidades bacterianas que nunca han visto un antibiótico sintético. Esto confirma que la resistencia es un fenómeno antiguo y ambiental, no un invento hospitalario.

**El suelo es la biblioteca original de la resistencia.** Los genes que vemos hoy en patógenos clínicos son una fracción pequeña de un reservorio mucho mayor que existe desde hace millones de años.

---

#### 5.2. Suelos degradados: selección intensiva

Los suelos degradados por actividades humanas son los más interesantes para estudiar la estructura molecular de la resistencia.

**Suelos agrícolas:**
El uso de estiércol animal como fertilizante aporta antibióticos residuales (sulfamidas, tetraciclinas) al suelo. Estudios detectan niveles de antibióticos veterinarios en suelos de cultivo que, aunque bajos, son suficientes para ejercer presión selectiva subinhibitoria.

**Suelos contaminados con metales pesados:**
La coselección por metales pesados selecciona simultáneamente resistencia a metales y a antibióticos. Los genes de resistencia a arsénico (*ars*), cobre (*cop*), y plata (*pco/sil*) viajan en plásmidos junto con genes como *blaTEM*, *qnrS*, *aac(3)-II*.

**Suelos en recuperación:**
Cuando un suelo disturbado comienza a ser recolonizado, las primeras comunidades microbianas que aparecen incluyen géneros como *Pseudomonas*, *Bacillus*, *Streptomyces*. Los dos primeros son conocidos por su versatilidad metabólica y su capacidad de intercambio genético. *Streptomyces* es el grupo que produce la mayoría de antibióticos naturales del suelo.

¿Qué está pasando en esas comunidades pioneras en términos de resistoma? ¿Hay enriquecimiento de genes de resistencia en las primeras etapas de sucesión ecológica? Si lo hay, tendríamos un indicador de que la sucesión microbiana en suelos degradados no es solo un proceso de recuperación — es también un proceso de recomposición del resistoma.

---

#### 5.3. Qué podemos hacer desde la investigación en tierra degradada

**Secuenciación metagenómica de suelos de referencia:**
Comparar el resistoma de suelos prístinos vs. suelos degradados de la misma zona geológica. Cuantificar el enriquecimiento absoluto y relativo de genes de resistencia.

**Vigilancia del resistoma en proyectos de biorremediación:**
Si estamos añadiendo microorganismos a un suelo degradado para recuperarlo, ¿estamos añadiendo también genes de resistencia? ¿Se transfieren esos genes a la microbiota indígena? Necesitamos herramientas para rastrear esto.

**Fitorremediación y microbioma:**
Ciertas plantas estabilizan metales pesados en suelo. ¿Qué pasa con el microbioma rizosférico de esas plantas en términos de carga de resistencia? ¿Podemos diseñar comunidades vegetales que reduzcan el resistoma en lugar de aumentarlo?

**Biopelículas como sistemas modelo:**
Las biopelículas bacterianas en raíces y suelo son laboratorios naturales de transferencia horizontal. El espacio confinado, la proximidad celular y la cooperación metabólica facilitan eventos de conjugación que serían raros en agua o sangre. Estudiar biopelículas de suelos degradados puede enseñar-nos cómo se transfieren los genes de resistencia en condiciones naturales.

---

## 6. CIERRE

**Tiempo:** 5 minutos

### Desarrollo

Volvamos a la pregunta que abre esta sesión:

*¿Qué pasa dentro de cada bacteria resistente?*

Vemos ahora con más claridad. No una caja negra. Una máquina molecular extraordinariamente sofisticada, con cinco mecanismos posibles de defensa, organizada en estructuras genéticas que se copian, saltan y recombinan, todo a una velocidad que ningún otro sistema biológico iguala.

Lo que hace al problema tan difícil es también lo que lo hace tan fascinante. Las bacterias no están "aprendiendo" a resistir. Ya lo sabían hacer antes de que existiéramos. Lo que hicimos fue crear las condiciones para que esa capacidad preexistente se expresara a escala global.

Y el suelo — el suelo que la ponente estudia, trabaja y ayuda a recuperar — no es solo telón de fondo de esta historia. Es el escenario original. Es donde la resistencia se inventó. Y es donde, si sabemos mirar con ojos moleculares, todavía podemos aprender más sobre ella que en cualquier hospital.

Este enfoque es exactamente lo que propone el marco **One Health** de la OMS y la FAO: la resistencia a antibióticos no puede entenderse solo desde la salud humana ni solo desde la ambiental. Salud humana, salud animal y salud ambiental son interdependientes. Un suelo degradado que selecciona bacterias resistentes no es solo un problema ecológico — es un problema de salud pública. Y a la inversa: cuando usamos antibióticos en medicina humana, los residuos llegan al ambiente y alteran el resistoma del suelo. La ponente, desde su trabajo en tierras degradadas, está contribuyendo directamente a esa cadena.

**[Frase de cierre]**
*"Cada gramo de suelo degradado que recuperamos es también una oportunidad de entender — y quizás de influir — en el resistoma más antiguo del mundo."*

---

## RECURSOS Y REFERENCIAS

### Documentación OMS/PAHO
- OMS 2024 Bacterial Priority Pathogens List: https://www.who.int/news/item/17-05-2024-who-updates-list-of-drug-resistant-bacteria-most-threatening-to-human-health
- PAHO — OMS actualiza lista de patógenos resistentes: https://www.paho.org/es/noticias/10-7-2024-oms-actualiza-lista-patogenos-resistentes

### Datos y estadísticas
- *The Lancet* 2022 (GRAM report): https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)02724-0/fulltext
- National Geographic España 2024 — Proyección 39 millones de muertes para 2050: https://www.nationalgeographic.com.es/ciencia/auge-superbacterias-desafio-sanitario-para-2050_23261

### Mecanismos moleculares
- USP 2025 — Resistência antimicrobianos: https://edisciplinas.usp.br/pluginfile.php/9184520/mod_resource/content/1/Resistência-antimicrobianos_2025.pdf
- INECOL México — Genes de resistencia a los antibióticos: https://www.inecol.mx/index.php/divulgacion/ciencia-hoy/genes-de-resistencia-a-los-antibioticos
- OAJI 2020 — Revisión mecanismos de resistencia: https://oaji.net/articles/2020/8277-1599877484.pdf

### Transferencia horizontal
- SciELO — Superbactérias: mecanismos de resistência: https://books.scielo.org/id/qhzxr/pdf/assef-9786557082331-07.pdf
- Elsevier — Papel de los integrones: https://www.elsevier.es/es-revista-enfermedades-infecciosas-microbiologia-clinica-28-articulo-papel-integrones-resistencia-agentes-antimicrobianos-13074963

### Aspectos ambientales
- FAO — Resistencia a antimicrobianos y epidemiología: https://openknowledge.fao.org/server/api/core/bitstreams/a1b53296-9a5d-4198-80b0-a8f8238519d9/content/y5468s0d.htm

---

*Documento preparado por Gerion — 2026-04-19*
