# Know Your Target · Klarna

- **Alumno:** Luis Baena
- **Proyecto:** Proyecto 1 · Know Your Target (UD1 · Eyes on Target)
- **Objetivo elegido:** [programa de bug bounty de Klarna en HackerOne](https://hackerone.com/klarna)
- **Alcance:** `*.klarna.com`, `*.klarna.net`, `*.klarnacdn.net` y `*.pricerunner.com` (detalle en [alcance.md](alcance.md))

## Por qué Klarna

Es un programa público, activo y con recompensa, gestionado por HackerOne y con *Gold Standard Safe Harbor*. Tiene cuatro comodines, así que da para un mapa de superficie completo y no se queda en una sola aplicación.

Además, sus exclusiones son pocas pero variadas, hosts concretos, rutas dentro de hosts permitidos, una marca entera (Kustom) y los subdominios que cuelgan del comodín pero opera un tercero. Y sus reglas (nada de herramientas automáticas y cabecera `X-Bug-Bounty` obligatoria) encajan muy bien con un reconocimiento solo pasivo.

## Contenido

**Parte 1 · Mapa de superficie de ataque (a mano)**

| Fichero | Qué es |
|---|---|
| [alcance.md](alcance.md) | El programa, lo que entra y lo que no, sus reglas y las decisiones que he tomado |
| [scope.txt](scope.txt) | El alcance convertido a lista, un objetivo por línea |
| [cuaderno.md](cuaderno.md) | El cuaderno de trabajo: cada acción con cuándo, objetivo, comando, resultado y siguiente paso |
| [mapa.md](mapa.md) | El mapa de superficie de ataque que entregaría al equipo antes de la fase activa |

**Parte 2 · First Agent (agente de reconocimiento)**

| Fichero | Qué es |
|---|---|
| [agente/src/tus_herramientas.py](agente/src/tus_herramientas.py) | Las herramientas que he añadido al agente (`correo_postura`, `infraestructura_ip`) |
| [agente/pruebas.md](agente/pruebas.md) | Comprobaciones del scope-guard, pruebas de las herramientas, el prompt y los intentos fuera de alcance |
| [agente/instrucciones.md](agente/instrucciones.md) | La plantilla del prompt del agente, ajustada al proyecto |
| [agente/informe.md](agente/informe.md) | El informe que generó el agente al lanzarlo contra el objetivo |
| [agente/traza.jsonl](agente/traza.jsonl) | La traza completa de la ejecución del agente, paso a paso |

**Parte 3 · Análisis comparativo**

| Fichero | Qué es |
|---|---|
| [comparativa.md](comparativa.md) | Comparación entre el trabajo manual y el del agente: qué encontró cada uno, los fallos del agente y la reflexión |

## Reglas que sigo

- Solo técnicas pasivas: nada de escaneo de puertos, escáneres de vulnerabilidades ni fuerza bruta.
- No contacto con ninguna persona de Klarna ni creo cuentas en sus servicios.
- Las pocas peticiones directas a servidores de Klarna llevan la cabecera `X-Bug-Bounty: h1-lbaeutr` que exige el programa.
- Si aparece algo grave (credenciales, un panel expuesto, datos personales), lo anoto sin el dato sensible y aviso al profesor.