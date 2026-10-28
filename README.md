# Know Your Target · Klarna

**Alumno:** Luis Baena
**Proyecto:** Proyecto 1 · Know Your Target (UD1 · Eyes on Target)
**Objetivo elegido:** [Klarna Bug Bounty en HackerOne](https://hackerone.com/klarna), con alcance `*.klarna.com`, `*.klarna.net`, `*.klarnacdn.net` y `*.pricerunner.com`

## Por qué Klarna

- Es un programa público y activo, con recompensa y *Gold Standard Safe Harbor*.
- Tiene cuatro comodines, así que el mapa de superficie no se queda corto.
- Sus exclusiones son pocas pero variadas: hosts concretos, rutas, una marca (Kustom) y subdominios de terceros bajo el comodín.
- Sus reglas (sin herramientas automáticas, cabecera `X-Bug-Bounty` obligatoria) encajan con un reconocimiento solo pasivo.

## Contenido

| Fichero | Qué es |
|---|---|
| [alcance.md](alcance.md) | Programa, reglas y alcance, con las decisiones tomadas |
| [scope.txt](scope.txt) | El alcance en formato de una línea por objetivo |
| [cuaderno.md](cuaderno.md) | Cuaderno de trabajo de la Parte 1 |
| [mapa.md](mapa.md) | Mapa de superficie de ataque |

## Reglas que sigo

- Solo técnicas pasivas: nada de escaneo de puertos, escáneres ni fuerza bruta.
- No contacto con personas ni creación de cuentas.
- Las peticiones directas a servidores de Klarna llevan `X-Bug-Bounty: h1-<handle>`.
- Si aparece algo grave, se anota sin el dato sensible y se avisa al profesor.