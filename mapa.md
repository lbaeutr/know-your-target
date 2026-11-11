# Mapa de superficie de ataque · Klarna

Este es el documento que entregaría al equipo antes de pasar a la fase activa. Todo lo que aparece aquí se ha obtenido con técnicas pasivas entre el 1 y el 2 de noviembre de 2026, así que es una foto de ese momento. La columna o la nota **Ref.** indica la hora de la entrada de [cuaderno.md](cuaderno.md) de la que sale cada dato (todas del 2026-11-02 salvo que se indique otra cosa).

## 1. Resumen

Klarna Bank AB es una fintech sueca de pagos aplazados, con sede en Sveavägen 46 (Estocolmo), que también es dueña del comparador de precios PriceRunner (PriceRunner International AB, misma dirección). Su infraestructura pública está casi entera en AWS (CloudFront, EC2 y Global Accelerator), con DNS en Akamai y UltraDNS, y además tiene un rango de IP propio (AS61162, `185.133.68.0/24`). He identificado 9.731 subdominios en alcance, de los que 1.921 existen hoy; su nomenclatura deja ver la arquitectura interna (servicio, entorno y región) e incluso 480 nombres públicos apuntan a IP privadas. La superficie expuesta está muy contenida, porque casi todo publica solo los puertos 80 y 443. Lo más llamativo está en PriceRunner, cuya infraestructura es más heterogénea: un portal SSL-VPN de Fortinet, un servidor FTP y varios entornos no productivos a la vista.

*Ref.: 10:38, 11:05, 11:22, 11:41, 17:35, 17:38, 17:58*

## 2. Dominios y subdominios

### 2.1 Cifras globales

| Dominio | Encontrados (subfinder + crt.sh) | Resuelven hoy | Excluidos por el programa |
|---|---|---|---|
| klarna.com | 1.544 | 281 | 24 (`locker.klarna.com` y lo que cuelga de él) |
| klarna.net | 7.790 | 1.608 | 0 |
| klarnacdn.net | 176 | 6 | 0 |
| pricerunner.com | 216 | 23 | 1 (`jobs.pricerunner.com`) |
| **Total** | **9.731** (+5 dominios raíz) | **1.921** | **25** |

Además, **32 subdominios vivos apuntan a servicios de terceros** (Freshdesk, Signicat, Statuspage, Vercel, Cloudflare, SendGrid, ThreatMetrix, SEON, Sardine, Shopify, Criteo, Palo Alto…) y, según la política, **quedan fuera de alcance** aunque cuelguen de un comodín.

*Ref.: 11:10, 11:17, 11:20, 11:22, 11:33*

**Cómo se organiza `klarna.net`:** los nombres siguen el formato `<servicio>.<entorno>.<región>.<sistema>.klarna.net`, por ejemplo `production.eu1.core-banking.klarna.net`. Los entornos son production, staging, playground y nonprod, y las regiones eu1, us1 y ap1. Las zonas más grandes son `e2e` (1.036), `fd-dev` (746), `c2c` (500), `cloud-automation-acmtest` (397) y `fd` (373). No son 7.790 servicios distintos, sino combinaciones de servicio × entorno × región. Además, 871 subdominios públicos tienen un CNAME hacia esta capa interna.

*Ref.: 11:10, 11:22*

### 2.2 Selección de subdominios

No caben 9.731 filas, así que la tabla recoge los más representativos: los principales, los de los puntos de interés, ejemplos de cada zona y ejemplos de lo que queda fuera.

| Subdominio | IP | En alcance | Para qué parece servir | Ref. |
|---|---|---|---|---|
| `klarna.com` | 3.173.21.37 / .22.37 / .23.37 | Sí | Dominio raíz, web vía CloudFront | 10:50 |
| `www.klarna.com` | 52.84.118.48 | Sí | Web principal (CloudFront, servidor envoy) | 11:38 |
| `api.klarna.com` | 34.250.60.129 | Sí | API principal, EC2 en Irlanda | 10:57 |
| `api-global.klarna.com` | 13.248.252.240 | Sí | API global, AWS Global Accelerator | 10:57 |
| `api-na.klarna.com` | 98.88.145.188 | Sí | API de Norteamérica | 10:57 |
| `api-oc.klarna.com` | 15.135.94.176 | Sí | API de Oceanía, EC2 en Sídney | 10:57 |
| `api-eu-mtls.klarna.com` | 18.238.55.102 | Sí | API de Europa con autenticación por certificado de cliente | 10:57 |
| `app.klarna.com` | 13.249.91.88 | Sí (salvo la ruta `/us/api/connected_card_bff/`) | API de la app de Klarna | 10:57 |
| `app-api-staging.klarna.com` | 108.139.47.43 | Sí | API de la app en entorno de pruebas | 10:57 |
| `auth-bp.klarna.com` | 18.164.116.44 | Sí | Autenticación (CloudFront) | 10:57 |
| `xs2a.banking.klarna.com` | 63.35.7.249 | Sí | API bancaria XS2A, EC2 en Irlanda | 10:57 |
| `eba.banking.klarna.com` | 63.32.48.135 | Sí | Servicio bancario, EC2 en Irlanda | 10:57 |
| `drive-to-store-ads.klarna.com` | — | Sí | "Klarna Partner Portal", informes para socios | 17:58 |
| `owp.klarna.com` | — | Sí | Almacén de ficheros de la web (PDF corporativos) | 17:58 |
| `mxz1`–`mxz4.klarna.com` | 52.30.236.203, 54.73.174.245, 3.73.181.240, 35.156.176.213 | Sí | Servidores de correo entrante, EC2 en Irlanda y Fráncfort | 10:57 |
| `185-133-68-X.v4.byoip.klarna.com` | 185.133.68.0/24 | Sí | Registros inversos del rango propio (AS61162) | 10:57 |
| `ob-de-modulith-us.production.c2c.klarna.net` | 100.61.34.31 | Sí | Servicio interno, único con un puerto alternativo (8080) | 17:38 |
| `nxdomain.klarna.net` y `cb-sta-account-lookup` (3 entornos) | 127.0.0.1 | Sí | Registros que apuntan a localhost | 17:38 |
| `pricerunner.com` | 3.173.21.37 / .22.37 / .23.37 | Sí | Dominio raíz; mismas IP de CloudFront que klarna.com | 10:50 |
| `www.pricerunner.com` | 108.139.29.124 | Sí | Web del comparador (CloudFront) | 11:05 |
| `api` / `api-us` / `api-stage.pricerunner.com` | 99.84.234.5 / 18.238.49.106 / 52.85.31.101 | Sí (salvo `/swagger-ui.html`) | APIs del comparador, una de ellas de pruebas | 11:05 |
| `vpn` / `pocvpn.pricerunner.com` | 99.80.232.166 | Sí | Portal SSL-VPN de Fortinet (punto de interés 1) | 11:05, 17:58 |
| `ftp.pricerunner.com` | 18.196.146.3 | Sí | Servidor ProFTPD (punto de interés 1) | 11:05 |
| `branch.nonprod` / `www.nonprod.pricerunner.com` | 99.84.234.12 / 99.84.234.35 | Sí | Entornos no productivos | 11:05 |
| `locker.klarna.com` | — | **No** (excluido) | Excluido por el programa, igual que lo que cuelga de él | 11:20 |
| `jobs.pricerunner.com` | 207.120.32.232 | **No** (excluido) | Ofertas de empleo, en Level3 | 11:05 |
| `status.klarna.com` | — | **No** (tercero) | Página de estado en Atlassian Statuspage | 11:33 |
| `engineering.klarna.com` | 162.159.152.4 / .153.4 | **No** (tercero) | Blog técnico en Medium, detrás de Cloudflare | 17:38, 17:58 |
| `investors.klarna.com` | 162.159.129.11 | **No** (tercero, dudoso) | Web de inversores, detrás de Cloudflare | 17:38 |
| `brand.klarna.com` | 76.76.21.93 | **No** (tercero) | Guías de marca, alojadas en Vercel | 10:57, 11:33 |
| `tmfp.klarna.com` | — | **No** (tercero) | Huella de dispositivo antifraude (ThreatMetrix) | 11:33 |
| `sase.klarna.net` | — | **No** (tercero) | Acceso remoto corporativo (Palo Alto Prisma Access) | 11:33 |
| `o4085.abmail.a.klarna.com` | 223.165.113.69 | **No** (tercero) | Seguimiento de correos de SendGrid | 10:57 |
| `design.pricerunner.com` | 198.185.159.145 | **No** (tercero) | Web en Squarespace | 11:05 |
| `pardko.pricerunner.com` | 74.119.117.62 | **No** (tercero) | Publicidad (Criteo) | 11:05 |
| 3 subdominios de `*.klarna.net` (detalle comunicado al profesor) | no resuelven | Registro DNS sí; servicio no | CNAME hacia Freshdesk sin destino (punto de interés 2) | 11:33 |

"—" indica que la IP no se recogió para ese host en las consultas hechas.

## 3. Infraestructura y servicios

**Hosting y red**
- Casi todo está en **AWS**: CloudFront para la web y las APIs, EC2 en eu-west-1 (Irlanda), eu-central-1 (Fráncfort), Norteamérica y ap-southeast-2 (Sídney), y Global Accelerator para la API global. *(10:57, 11:05)*
- **Rango de IP propio**: AS61162 (KLARNA-BANK-AB), `185.133.68.0/24`, traído a AWS (BYOIP) y ubicado en Irlanda. *(10:57)*
- `klarna.com` y `pricerunner.com` comparten las mismas tres IP de CloudFront. *(10:50, 11:05)*
- Las APIs están organizadas por región (eu, na, oc), con variantes `-mtls` en cada una. *(10:57)*

**DNS y registro**
- Los cuatro dominios están en el registrador corporativo **CSC Corporate Domains**. *(10:38)*
- klarna.com, klarna.net y klarnacdn.net usan **Akamai + UltraDNS** como servidores DNS; pricerunner.com usa **AWS Route 53**. *(10:38)*
- **Ninguno tiene DNSSEC.** Netcraft dice lo contrario, pero el whois de Verisign lo desmiente. *(10:38, 11:38)*

**Tecnologías web**
- La web principal va detrás de CloudFront, con servidor **envoy** (proxy de *service mesh*) y HTTP/2. *(11:38)*
- El certificado TLS es de Amazon (ACM), con TLS 1.3 y *forward secrecy*. Incluye un nombre interno, `klarna.production.us1.one-web-platform.klarna.net`, que revela el origen real. *(11:38)*
- El error 404 de `security.txt` es un XML `NoSuchKey` de **Amazon S3**, así que la web sirve desde un bucket detrás de CloudFront. *(11:53)*
- Trackers: 5, todos de Google, iguales en las dos webs. *(11:38, 11:41)*
- El `robots.txt` de klarna.com contiene las mismas rutas `/shopping/` que el de pricerunner.com, porque el comparador está integrado en la web de Klarna. También deja ver nombres de APIs internas (`search-compare-gateway`, `search-edge-rest`, `product-information-edge-rest`). *(11:53)*

**Correo**
- El correo entrante de los cuatro dominios, PriceRunner incluido, llega a `mxz1`–`mxz4.klarna.com` (EC2 de AWS). *(10:50, 10:57)*
- Para el correo saliente, klarna.com usa SendGrid, Google, Atlassian, Proofpoint y Amazon SES; pricerunner.com usa Microsoft 365, Google y HubSpot. *(10:50)*
- SPF con `-all` y **DMARC `p=reject`** en los cuatro dominios: la configuración más estricta. *(10:50)*

**Servicios en la nube (verificaciones en los TXT de klarna.com)**
- Productividad: Google Workspace, Microsoft 365, Atlassian, Notion, Miro, Loom y DocuSign.
- Identidad y dispositivos: Adobe IdP (SSO), Apple y Jamf.
- Seguridad: Palo Alto Networks, OneTrust y HackerOne.
- IA: OpenAI, Anthropic, ElevenLabs y Cursor.
- Desarrollo y producto: Docker, Stripe, Twilio, Mixpanel, IBM y Facebook.

*(10:50)*

**Servicios de terceros enlazados por CNAME:** antifraude (ThreatMetrix, SEON, Sardine), verificación de identidad (Signicat), soporte (Freshdesk), páginas de estado (Statuspage), webs (Vercel, Cloudflare), correo y ventas (SendGrid, Outreach) y acceso remoto (Palo Alto Prisma Access). *(11:33)*

**Lo que muestra Shodan (InternetDB)**
- De las 2.115 IP públicas propias, 688 tienen datos. Casi todas exponen **solo los puertos 80 y 443**. *(17:38)*
- El único puerto alternativo propio es el 8080, en `ob-de-modulith-us.production.c2c.klarna.net`. Los puertos raros de engineering e investors son los que Cloudflare abre en todos sus proxies. *(17:38)*
- No hay ninguna IP con CVE asociados. *(17:38)*
- **Fuga de direcciones internas:** 480 subdominios públicos resuelven a IP privadas (977 direcciones distintas), y 4 resuelven a `127.0.0.1`. *(17:35, 17:38)*

## 4. Correos y personas

- **Patrón de correo:** `{nombre}.{apellido}@klarna.com`, y el mismo en pricerunner.com. *(18:16)*
- Los servidores **no aceptan direcciones inexistentes** (`accept_all: False`), así que se podría comprobar si un correo es real. *(18:16)*
- **Volumen público:**
  - klarna.com: 1.161 correos indexados (1.086 personales, 143 de directivos y 75 genéricos).
  - pricerunner.com: solo 18, lo que sugiere que la mayoría del personal usa ya `@klarna.com`. *(18:16)*
- **Buzones de rol:**
  - Klarna usa `<función>.<país>@`, por ejemplo `press.us@`, `dataprotection.ca@` o `datenschutz.ch@`, además de `hello@`, `service@` y `feedback@`.
  - PriceRunner los escribe pegados (`infose@`, `infouk@`) y tiene buzones en sueco y danés. *(18:16)*
- **Organización:**
  - Entre 1.001 y 5.000 empleados, con sede en Estocolmo.
  - Por departamento, IT e ingeniería es claramente el mayor (389 de los correos identificados), seguido de dirección (125), ventas (122) y datos (75): un tercio de la plantilla visible es técnica. *(18:16)*


## 5. Puntos de interés

Estos son los tres elementos que investigaría primero en la fase activa.

**1. El perímetro de acceso remoto de PriceRunner: VPN de Fortinet y FTP**
`vpn.pricerunner.com` y `pocvpn.pricerunner.com` comparten IP (EC2, Irlanda) y Google los indexa como un portal **SSL-VPN de Fortinet** ("Launch FortiClient", token y SSO). Además, `ftp.pricerunner.com` expone un servidor **ProFTPD** en EC2 Fráncfort. Son las puertas de entrada remota de la filial, que tiene una infraestructura menos homogénea que la de Klarna. Los SSL-VPN de Fortinet han tenido vulnerabilidades críticas muy explotadas, el prefijo "poc" sugiere una prueba de concepto que se quedó publicada y el FTP es un protocolo heredado. En la fase activa tocaría confirmar versiones y configuración, siempre dentro de las reglas del programa. *(11:05, 17:38, 17:58)*

**2. Posibles registros DNS colgantes hacia Freshdesk**
Tres subdominios de `*.klarna.net` tienen un CNAME que apunta a Freshdesk pero no resuelve. Es el patrón típico del *subdomain takeover*: si el portal se dio de baja en Freshdesk, otra persona podría reclamarlo y servir contenido bajo un dominio de Klarna. El servicio de Freshdesk está fuera de alcance, pero **el registro DNS es de Klarna**, y el programa paga expresamente estos hallazgos (150 $). *(11:33)*

**3. Entornos no productivos accesibles desde Internet**
`app-api-staging.klarna.com`, `api-stage.pricerunner.com`, `branch.nonprod.pricerunner.com` y `www.nonprod.pricerunner.com` resuelven a IP públicas, y la nomenclatura muestra cientos de nombres `playground`, `nonprod` y `e2e`. Los entornos de pruebas suelen tener controles más débiles, datos de prueba y funciones a medio terminar, y sirven para entender cómo funcionan las APIs de producción. La política avisa de que estos hallazgos pueden pagarse menos, pero siguen siendo una vía de entrada habitual. *(10:57, 11:05, 11:10)*

**Otros hallazgos que conviene tener presentes:**
- La fuga de direcciones internas por DNS (480 subdominios).
- Los 4 registros a `127.0.0.1`.
- La ausencia de `security.txt` en las dos webs, aunque hay programa de bug bounty.
- El portal de socios `drive-to-store-ads.klarna.com`, indexado en Google.

*(11:53, 17:35, 17:38, 17:58)*

## 6. Limitaciones y alcance del trabajo

- **Es una foto del 1 y 2 de noviembre de 2026.** El DNS y la infraestructura cambian, y un 80 % de los subdominios encontrados ya no existe.
- **Las fuentes son imperfectas:**
  - DNSDumpster solo muestra 50 de los 1.685 registros de klarna.com.
  - Los 1.264 certificados comodín ocultan hosts.
  - InternetDB no tiene datos de la VPN ni del FTP de PriceRunner.
  - Netcraft se equivoca con el DNSSEC y los servidores DNS.
  - theHarvester no devolvió nada con las fuentes gratuitas.

  Por eso cada dato se ha contrastado con al menos otra fuente cuando ha sido posible.
- **Técnicas opcionales:** se ha hecho la primera (resolver los subdominios y mirar de quién es cada IP, y si es CDN o está expuesta directamente). No se han hecho Wayback Machine, exiftool, LinkedIn, Have I Been Pwned ni Sherlock.
- **Las únicas peticiones directas a Klarna** fueron las 4 de la técnica 5 (robots.txt y security.txt), con la cabecera `X-Bug-Bounty: h1-lbaeutr`.
