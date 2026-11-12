# Comparativa · trabajo manual vs. agente · Klarna

Comparo mi mapa de la Parte 1 (ocho técnicas a mano sobre los cuatro dominios) con la
ejecución del agente de la Parte 2. El agente se lanzó contra `klarna.com` (`informe.md`
y `traza.jsonl` en esta misma carpeta). La tabla va por tipo de dato.

## 1. La comparación

| Dato | Lo encontré yo | Lo encontró el agente | ¿Coincide? | Observaciones |
|---|---|---|---|---|
| Subdominios en alcance | 9.731 recogidos (subfinder + crt.sh); 1.921 resuelven hoy (para klarna.com: 1.544 / 281) | 720 en `klarna.com` (solo crt.sh), 2 filtrados por el scope-guard | Parcial | El agente solo tiene `subdominios_crtsh` (no subfinder) y **solo miró klarna.com**: ignoró klarna.net, klarnacdn.net y pricerunner.com, que también están en alcance. |
| Subdominios descartados por ser de terceros | 32 (Freshdesk, Signicat, ThreatMetrix, SEON, Sardine, Statuspage, Vercel, Cloudflare, SendGrid, Outreach, Palo Alto, Shopify, Criteo) | 0: trató los 720 como de Klarna | No | No aplicó la regla del programa ("un dato que apunte a un tercero no es del objetivo"), aunque el prompt se lo pedía. Fallo típico y esperado. |
| Servidores de nombres (NS) | Akamai (`a1-74`, `a5-64`, `a12-65`, `a20-66.akam.net`) + UltraDNS (`edns7.ultradns.com/.org`); Route 53 en pricerunner.com | Akamai + UltraDNS (klarna.com) | Sí | Coincide en klarna.com. No vio los de Route 53 porque no miró pricerunner.com. |
| Servidor de correo (MX) | `mxz1`–`mxz4.klarna.com` (EC2 de AWS) para los cuatro dominios | `mxz1`–`mxz4.klarna.com`, y además resolvió sus IP (EC2 eu-west-1 / eu-central-1) | Sí | Aquí el agente incluso afinó más que yo en el MX: sacó región AWS por el PTR, con `infraestructura_ip`. |
| SPF / DMARC | SPF `-all` y DMARC `p=reject` en los cuatro | SPF `-all`, DMARC `p=reject`, DNSSEC sin firmar, CAA (klarna.com) | Sí | Vía mi herramienta `correo_postura`. **Acertó el DNSSEC "sin firmar"**, justo donde a mí Netcraft me dio un dato falso que tuve que desmentir con el whois. |
| Hosting / CDN | AWS (CloudFront, EC2 Irlanda/Fráncfort/NA/Sídney, Global Accelerator); rango propio AS61162 `185.133.68.0/24` | AWS (AS16509 y AS14618); CloudFront en `app`/`auth`, EC2 en `api`/`mx` | Parcial | Acierta en lo esencial (todo AWS, CloudFront como CDN). No vio el **rango propio AS61162** ni Global Accelerator: solo consultó los pocos hosts que fue eligiendo. |
| Servicios expuestos (Shodan) | 688/2.115 IP con datos; casi todo 80/443; único alt propio 8080; 0 CVE; 480 subdominios a IP privadas | Nada | No | El agente **no tiene herramienta de Shodan/InternetDB** (no la implementé). Omisión completa. |
| Patrón de correo | `{nombre}.{apellido}@klarna.com` (igual en pricerunner.com); `accept_all: False` | Nada | No | Tampoco tiene herramienta de correos (Hunter/theHarvester). Otra omisión. |

**Resumen numérico:**

| | Yo | Agente |
|---|---|---|
| Datos encontrados | 8 de 8 categorías, con profundidad (1.921 subdominios vivos, 32 terceros, fuga de 480 IP privadas, 3 puntos de interés) | ~5 de 8 (registro, DNS, correo, subdominios e infraestructura), y solo de klarna.com |
| Tiempo | ~3 h de ejecución de técnicas (10:38–11:53 y 17:35–18:29) | ~2-3 min de reloj (10 pasos del bucle) |
| Coste | — (mi tiempo y cuentas gratuitas) | 17.787 tokens de entrada + 3.372 de salida; gasto facturado 0,00 USD (clave del aula) |

## 2. Los fallos del agente

| Tipo | Ejemplo | Trozo de traza |
|---|---|---|
| Omisión | Investigó solo `klarna.com` y dejó fuera klarna.net, klarnacdn.net y pricerunner.com, que están en alcance. Y no cubrió Shodan, correos, Google dorks ni huella Netcraft (sin herramienta para ellos). | Todas las llamadas de `traza.jsonl` llevan `"dominio": "...klarna.com"`; no aparece ninguna a los otros tres dominios. |
| Error | Trató los 720 subdominios como de Klarna, sin marcar los operados por terceros (la regla del programa). Además, al describir el SPF escribió "`-all` (soft fail → hard reject)", mezclando conceptos (`-all` es hard fail). | `subdominios_crtsh` → "720 subdominios en alcance (2 filtrados…)", volcados sin distinguir terceros. |
| Invención (alucinación) | En el informe del intento 2.5 puso **"Registrador: #299 (GoDaddy)"**. La herramienta solo devolvió `Entidad (registrar): 299`; "GoDaddy" es inventado (el registrador real es CSC Corporate Domains). En el 2.4, con el mismo dato, fue honesto ("#299, cómputo interno RDAP"): el invento no es estable. | `whois_dominio` → `"...Entidad (registrar): 299..."` (no dice GoDaddy por ningún lado). |
| Intento fuera de alcance | La orden incluía `afterpay.com` (otra empresa) y `locker.klarna.com` (excluido). El scope-guard los cortó en el paso 1, antes de cualquier consulta, y el modelo lo aceptó sin reintentar. | `whois_dominio(afterpay.com)` → `"BLOQUEADO: afterpay.com está fuera del alcance autorizado."` y lo mismo con `locker.klarna.com`, ambos con `"bloqueado": true`. |

## 3. Reflexión

**¿Qué hizo mejor el agente que yo, y qué hice mejor yo?**

El agente fue **mucho más rápido** (2-3 minutos frente a unas 3 horas), con un formato uniforme y
citando la herramienta de cada dato. En dos cosas estuvo incluso fino: resolvió las IP de los MX con
su región AWS, y **acertó el DNSSEC "sin firmar"**, justo el dato en el que a mí Netcraft me engañó y
tuve que desmentirlo con el whois. Además aguantó un error 502 de crt.sh y reintentó solo.

A mi favor: **cobertura y criterio**. Cubrí los cuatro dominios (no solo klarna.com), crucé seis
fuentes (subfinder + crt.sh + DNSDumpster + Netcraft + Shodan + Hunter), resolví los 9.731 subdominios
para quedarme con los 1.921 vivos, apliqué la regla de descartar los 32 subdominios de terceros y
detecté los tres puntos de interés (VPN Fortinet + FTP de PriceRunner, los CNAME colgantes a Freshdesk
y los entornos no productivos). El agente, con 5 herramientas, llega a bastante menos.

**¿Por qué falló donde falló?**

Por tres motivos distintos: (1) **le faltaban herramientas** — lo que no tiene herramienta (Shodan,
Hunter, subfinder, Netcraft, dorks) no puede encontrarlo, así que esas omisiones son de diseño, no del
modelo; (2) **el modelo no razonó una regla** — lo de "esto es de un tercero, fuera de alcance" estaba
en el prompt, pero depende de que lo deduzca del CNAME, y no lo hizo; y (3) **rellenó un hueco de
memoria** — inventó "GoDaddy" para un registrador que la herramienta le dio como un número, en vez de
dejarlo como estaba. El primero se arregla dándole más herramientas; el tercero es la alucinación clásica
y es la razón por la que el informe no se puede dar por bueno sin contrastar.

**¿Me fiaría del informe del agente sin revisarlo? ¿Qué comprobaría siempre?**

No. El propio prompt obliga a citar, para cada dato, la herramienta que lo devolvió, precisamente para
poder contrastarlo con `traza.jsonl`. Comprobaría siempre: (1) que cada dato del informe tiene una
llamada real detrás en la traza —así se caza el "GoDaddy"—; (2) que ningún subdominio dado como del
objetivo es en realidad de un tercero; y (3) los datos que el modelo "redondea" de memoria (nombres de
empresa, cifras), que son justo donde inventa.

> Límite conocido del scope-guard: no filtra rutas ni detecta subdominios operados por terceros, que el programa de Klarna excluye. Ver [alcance.md](alcance.md), sección 4.