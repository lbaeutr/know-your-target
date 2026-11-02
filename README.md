# Know Your Target · Klarna

- **Alumno:** Luis Baena
- **Proyecto:** Proyecto 1 · Know Your Target (UD1 · Eyes on Target)
- **Objetivo elegido:** [programa de bug bounty de Klarna en HackerOne](https://hackerone.com/klarna)
- **Alcance:** `*.klarna.com`, `*.klarna.net`, `*.klarnacdn.net` y `*.pricerunner.com` (detalle en [alcance.md](alcance.md))

## Por qué Klarna

Es un programa público, activo y con recompensa, gestionado por HackerOne y con *Gold Standard Safe Harbor*. Tiene cuatro comodines, así que da para un mapa de superficie completo y no se queda en una sola aplicación.

Además, sus exclusiones son pocas pero variadas: hosts concretos, rutas dentro de hosts permitidos, una marca entera (Kustom) y los subdominios que cuelgan del comodín pero opera un tercero. Y sus reglas (nada de herramientas automáticas y cabecera `X-Bug-Bounty` obligatoria) encajan muy bien con un reconocimiento solo pasivo.

## Contenido

| Fichero | Qué es |
|---|---|
| [alcance.md](alcance.md) | El programa, lo que entra y lo que no, sus reglas y las decisiones que he tomado |
| [scope.txt](scope.txt) | El alcance convertido a lista, un objetivo por línea  |
| [cuaderno.md](cuaderno.md) | El cuaderno de trabajo: cada acción con cuándo, objetivo, comando, resultado y siguiente paso |
| [mapa.md](mapa.md) | El mapa de superficie de ataque que entregaría al equipo antes de la fase activa |

## Reglas que sigo

- Solo técnicas pasivas: nada de escaneo de puertos, escáneres de vulnerabilidades ni fuerza bruta.
- No contacto con ninguna persona de Klarna ni creo cuentas en sus servicios.
- Las pocas peticiones directas a servidores de Klarna llevan la cabecera `X-Bug-Bounty: h1-lbaeutr` que exige el programa.
- Si aparece algo grave (credenciales, un panel expuesto, datos personales), lo anoto sin el dato sensible y aviso al profesor.
