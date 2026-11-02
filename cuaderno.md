# Cuaderno de trabajo · Klarna

Cada entrada recoge las cinco anotaciones que pide el enunciado: **cuándo · objetivo (y si está en alcance) · qué hice · qué salió · siguiente paso**.

Las peticiones directas a servidores de Klarna llevan la cabecera `X-Bug-Bounty: h1-lbaeutr`, como exige el programa.

```
2026-11-01 15:30 · objetivo: hackerone.com/klarna (fuente pública, no es el objetivo)
$ navegador: https://hackerone.com/klarna (lectura de la política, versión del 15/09/2026)
-> 4 comodines en alcance: *.klarna.com, *.klarna.net, *.klarnacdn.net, *.pricerunner.com
-> fuera: locker.klarna.com, jobs.pricerunner.com, nuji.com, 4 rutas, Kustom y subdominios de terceros
-> reglas: sin herramientas automáticas, cabecera X-Bug-Bounty obligatoria, sin ingeniería social
siguiente: redactar alcance.md y scope.txt, y empezar con whois de los 4 dominios raíz
```

```
2026-11-02 10:38 · objetivo: klarna.com, klarna.net, klarnacdn.net, pricerunner.com (in scope, dominios raíz)
$ whois -accepteula -nobanner <dominio> | Select-String "Registrar:","Creation Date","Registry Expiry","Name Server","DNSSEC"
$ Invoke-RestMethod https://rdap.verisign.com/<tld>/v1/domain/<dominio> → RDAP del registrador (rdap.cscglobal.com), entidad "registrant"
-> registrador de los 4: CSC Corporate Domains (registrador corporativo)
-> alta: pricerunner.com 1999-05-19 · klarna.com 2008-12-12 · klarna.net 2009-05-06 · klarnacdn.net 2014-11-03; caducan entre 05/2027 y 12/2027
-> NS de klarna.com, klarna.net y klarnacdn.net: Akamai (a1-74, a5-64, a12-65, a20-66.akam.net) + UltraDNS (edns7.ultradns.com/.org)
-> NS de pricerunner.com: AWS Route 53 (ns-149, ns-889, ns-1081, ns-1564.awsdns-*), infraestructura DNS separada
-> DNSSEC: unsigned en los 4
-> organización: "Klarna Bank AB" en klarna.com, klarna.net y klarnacdn.net; "PriceRunner International AB" en pricerunner.com (filial del grupo, en alcance de forma expresa)
-> el whois del registrador (whois.corporatedomains.com, puerto 43) da timeout, también consultado directamente; la organización se obtiene por RDAP, el sustituto oficial de whois (HTTPS)
siguiente: registros DNS (A, NS, MX, TXT y DMARC) de los 4 dominios
```

```
2026-11-02 10:50 · objetivo: klarna.com, klarna.net, klarnacdn.net, pricerunner.com (in scope, dominios raíz)
$ Resolve-DnsName <dominio> -Type A|NS|MX|TXT -DnsOnly  +  Resolve-DnsName _dmarc.<dominio> -Type TXT -DnsOnly
-> A: klarna.com y pricerunner.com → mismas 3 IP (3.173.21.37, 3.173.22.37, 3.173.23.37), rango AWS, probable CDN compartido; klarna.net y klarnacdn.net sin A en el raíz
-> MX: los 4 dominios → mxz1-4.klarna.com (klarnacdn.net solo mxz1-3); el correo de PriceRunner también lo recibe Klarna
-> SPF klarna.com (-all): SendGrid, Google, Atlassian, Proofpoint (pphosted.com) y 4 IP de AWS; klarna.net y klarnacdn.net: include:klarna.com
-> SPF pricerunner.com (-all): Microsoft 365, Google y HubSpot → correo saliente propio
-> DMARC: p=reject en los 4, informes a dmarc-reports@klarna.com
-> TXT klarna.com: 41 registros; servicios verificados: Google (x5), Microsoft 365, Atlassian, Notion, Miro, Loom, DocuSign, Adobe IdP, Apple, Jamf, Palo Alto Networks, OneTrust, HackerOne (x3), OpenAI, Anthropic, ElevenLabs, Cursor, Docker, Stripe, Twilio, Mixpanel, IBM, Amazon SES, Facebook; 2 tokens sin identificar
-> TXT klarna.net: 15 (Google x7, Microsoft x2, Apple, Atlassian, HackerOne x3) · klarnacdn.net: 2 · pricerunner.com: 11 (Google x7, Microsoft x2, 1 token sin identificar)
siguiente: DNSDumpster para cruzar estos datos y ver hosts e IP con su ASN
```

```
2026-11-02 10:57 · objetivo: klarna.com (in scope)
$ navegador: https://dnsdumpster.com → klarna.com → exportación .xlsx (generada 2026-11-02 09:57:58 UTC)
-> 1685 registros en su base de datos; la versión gratuita muestra 50 (30 de ellos son PTR de *.v4.byoip.klarna.com)
-> ASN propio: AS61162 KLARNA-BANK-AB, rango 185.133.68.0/24 (BYOIP en AWS, ubicado en Irlanda); resto: AWS (AS16509), Akamai (AS21342), Vercara/UltraDNS (AS12008), SendGrid (AS11377)
-> MX mxz1-4.klarna.com → EC2 de AWS (2 en eu-west-1 Irlanda, 2 en eu-central-1 Fráncfort); NO son de Proofpoint (Proofpoint solo aparece en el SPF, correo saliente)
-> NS: 4 de Akamai (NL/US) + 2 de Vercara (US); coincide con whois
-> APIs por región: api (EC2 Irlanda), api-global (AWS Global Accelerator, awselb/2.0), api-na/api-na-2 (EE. UU.), api-oc (EC2 Sídney); variantes -mtls en eu, na y oc (CloudFront)
-> app, app-api, app-link-bridge, auth-bp, business-survey → CloudFront; app-api-staging → entorno de pruebas expuesto
-> banca: xs2a.banking y eba.banking (EC2 Irlanda), xs2a-newsletter.banking y status.xs2a.banking (CloudFront)
-> brand.klarna.com → Vercel (hosting de terceros, dudoso: revisar si cuenta como "apunta a un tercero")
-> o4085.abmail.a.klarna.com → SendGrid (AS11377): operado por un tercero → FUERA de alcance aunque cuelgue del comodín
-> servicios: CloudFront 12, Vercel 2, awselb/2.0 1 · países: Irlanda 35, EE. UU. 19, Países Bajos 3, Alemania 2, Australia 1
siguiente: DNSDumpster de pricerunner.com
```

```
2026-11-02 11:05 · objetivo: pricerunner.com (in scope)
$ navegador: https://dnsdumpster.com → pricerunner.com → exportación .xlsx (generada 2026-11-02 10:05:04 UTC)
-> 34 registros (26 A, 4 MX, 4 NS), todos visibles en la versión gratuita
-> ASN: AWS (AS16509) 28, Squarespace (AS53831) 2, Level3 (AS3356) 1, Microsoft (AS8075) 1, Criteo (AS19750) 1 · países: EE. UU. 26, Irlanda 5, Alemania 3
-> web y CDN: www, de, dk, se, uk, research, images, images-eu/-us/-global → CloudFront; varios comparten las 3 IP de klarna.com (3.173.21-23.37) → CDN compartido confirmado
-> APIs: api, api-us, api-stage → CloudFront (sus rutas /swagger-ui.html están fuera de alcance); click y click-us → CloudFront
-> ftp.pricerunner.com → EC2 Fráncfort, banner "220 ProFTPD Server (Pricerunner Swing FTP Server)" → servicio FTP expuesto
-> vpn y pocvpn.pricerunner.com → misma IP, EC2 Irlanda, respuesta HTTP "ACME Access Only" → acceso VPN; "poc" sugiere prueba de concepto
-> entornos no productivos: api-stage, branch.nonprod y www.nonprod → CloudFront
-> MX → mxz1-4.klarna.com (mismos EC2 que klarna.com) · NS → Route 53 (coincide con whois)
-> terceros → FUERA de alcance: jobs (Level3, además excluido por el programa), design y www.design (Squarespace), pardko (Criteo), o29.ptr8851 (SendGrid); newsroom (Azure, Irlanda) dudoso
siguiente: técnica 3, subdominios completos de los 4 dominios con subfinder y crt.sh
```

```
2026-11-02 11:10 · objetivo: klarna.com, klarna.net, klarnacdn.net, pricerunner.com (in scope)
$ .\subfinder.exe -dL dominios.txt -silent -o subs_subfinder.txt   (subfinder v2.17.0, fuentes públicas por defecto)
-> 9733 subdominios: klarna.com 1550 · klarna.net 7790 · klarnacdn.net 176 · pricerunner.com 217
-> klarna.net sigue una nomenclatura interna <servicio>.<entorno>.<región>.<sistema>.klarna.net (ej. production.eu1.core-banking.klarna.net)
   entornos: production, staging, playground, nonprod · regiones: eu1, us1, ap1
   zonas más grandes: e2e 1036, fd-dev 746, c2c 500, cloud-automation-acmtest 397, fd 373, nonprod 263, mk8s 101, pgw-pci 86, logging 84
   → no son 7790 servicios, sino combinaciones servicio × entorno × región, muchas de pruebas
-> klarna.com: 684 de primer nivel; zonas: playground 205, nonprod 171, portal 67, byoip 35, card-issuing-us 25, locker 23, staging 15, openbanking 12
-> *.locker.klarna.com (23): cuelgan de locker.klarna.com, que está excluido → se tratan como FUERA de alcance
siguiente: crt.sh para cruzar con los certificados y juntar ambas listas
```

```
2026-11-02 11:17 · objetivo: klarna.com, klarna.net, klarnacdn.net, pricerunner.com (in scope)
$ Invoke-RestMethod "https://crt.sh/?q=%25.<dominio>&output=json" → name_value, quitando "*." y duplicados → subs_crtsh.txt
-> 2682 nombres en certificados: klarna.com 720 · klarna.net 1895 · klarnacdn.net 26 · pricerunner.com 36
-> 1264 nombres comodín (*.algo.klarna.*) en certificados → muchos hosts quedan ocultos tras certificados comodín
-> solo 23 subdominios nuevos respecto a subfinder (subfinder ya usa crt.sh entre sus fuentes)
siguiente: juntar ambas listas, quitar duplicados y exclusiones del programa (locker.klarna.com y *.locker.klarna.com, jobs.pricerunner.com)
```

```
2026-11-02 11:20 · objetivo: subs_subfinder.txt + subs_crtsh.txt (in scope salvo exclusiones)
$ unión de ambas listas, en minúsculas, sin duplicados; se separan locker.klarna.com, *.locker.klarna.com y jobs.pricerunner.com
-> 9756 subdominios únicos; 25 excluidos por el programa → subs_excluidos.txt
-> quedan 9731 → subs_todos.txt: klarna.com 1544 · klarna.net 7790 · klarnacdn.net 176 · pricerunner.com 216 (+5 dominios raíz)
siguiente: resolver los 9731 (A y CNAME) para saber cuáles existen hoy y cuáles apuntan a terceros
```

```
2026-11-02 11:22 · objetivo: subs_todos.txt, 9731 subdominios (in scope)
$ Resolve-DnsName <sub> -Type A -DnsOnly -QuickTimeout → CNAME + IP de cada uno → subs_resueltos.csv  (7 min)
-> resuelven 1921 de 9731 (≈20 %): klarna.com 281 · klarna.net 1608 · klarnacdn.net 6 · pricerunner.com 23 (+3 raíz)
-> el resto (≈80 %) solo existe en certificados o fuentes antiguas
-> destinos de CNAME: klarna.net 871 (los nombres públicos apuntan a la capa interna *.klarna.net), cloudfront.net 197, amazonaws.com 37, awsglobalaccelerator.com 7
-> terceros detectados por CNAME: freshdesk.com 6, signicat (.cloud/.com) 6, vercel-dns.com 3, stspg-customer.com 3, online-metrix.net 2, sendgrid.net 2, cloudflare.net 2,
   seondf.com, sardine.ai, outreach.io, myshopify.com, gpcloudservice.com, spgo.io, dnsdelegation.io y example.com (1 cada uno)
siguiente: listar los subdominios que apuntan a terceros para marcarlos como FUERA de alcance en el mapa
```

```
2026-11-02 11:33 · objetivo: subs_resueltos.csv, subdominios con CNAME (in scope salvo terceros)
$ filtrar CNAME cuyo destino final no es Klarna ni AWS/Akamai → subs_terceros.csv
-> 32 subdominios apuntan a terceros → FUERA de alcance según la política ("dig no debe apuntar a un tercero"):
   antifraude (huella de dispositivo, nombres *fp): tmfp.klarna.com y tm.production.eu1.tmfp.klarna.net (ThreatMetrix), eu.saifp.klarna.com (Sardine), snfp.klarna.com (SEON)
   identidad (eID/KYC): signicat, signicat-eid, signicat-eid-app(-yellow).klarna.com y 2 en klarna.net (Signicat)
   soporte: 6 subdominios de *.klarna.net hacia Freshdesk (3 activos y 3 sin destino, ver abajo)
   estado: status.klarna.com, status.openbanking.klarna.com, status.xs2a.banking.klarna.com (Atlassian Statuspage)
   web: brand, thecheckout y www.thecheckout.klarna.com (Vercel); l.klarna.com y test.nonprod.eu1.cfpoc.klarna.net (Cloudflare)
   correo y ventas: email.klarna.com y url4310.pricerunner.com (SendGrid), click.eu.mail.klarna.com (spgo.io), outreach.klarna.com (Outreach)
   otros: sase.klarna.net (Palo Alto GlobalProtect/Prisma Access, acceso remoto), shopify-test-store...integrationlayer.klarna.net (Shopify),
          pardko.pricerunner.com (Criteo, vía dnsdelegation.io), bouncer-dns-test.nonprod.klarna.net (CNAME a example.com, registro de prueba)
-> 3 CNAME colgantes: 3 subdominios de *.klarna.net apuntan a Freshdesk pero no resuelven → posible subdomain takeover; solo se anota, no se comprueba
   (nombres exactos omitidos en el repositorio público según la política del programa)
siguiente: técnica 4, huella tecnológica con Netcraft (www.klarna.com y www.pricerunner.com)
```

```
2026-11-02 11:38 · objetivo: www.klarna.com (in scope)
$ navegador: https://sitereport.netcraft.com/?url=https://www.klarna.com
-> hosting: AWS CloudFront (AS16509), IP 52.84.118.48, nodo lhr82 (Londres); sin IPv6
-> organización: Klarna Bank AB, Sveavägen 46, Stockholm (coincide con RDAP); contacto DNS: dns-admin@klarna.com (buzón de rol)
-> servidor: envoy (proxy de service mesh) · HTTP/2
-> TLS: certificado DV de Amazon (Amazon RSA 2048 M04, ACM), feb 2026 → mar 2027; TLSv1.3, RSA 2048, PFS, OCSP stapling
-> el certificado incluye un SAN interno: klarna.production.us1.one-web-platform.klarna.net → nombre del origen real, coincide con la zona one-web-platform vista con subfinder
-> trackers: 5, todos de Google (Analytics, Tag Manager, DoubleClick, AdSense, AdMob)
-> discrepancias con fuentes primarias: Netcraft dice "DNSSEC Enabled" y NS de MarkMonitor; whois de Verisign dice unsigned y NS de Akamai/UltraDNS → se da por bueno whois
-> Hosting History: no aparece en la versión gratuita
siguiente: Netcraft de www.pricerunner.com
```

```
2026-11-02 11:41 · objetivo: www.pricerunner.com (in scope)
$ navegador: https://sitereport.netcraft.com/?url=https://www.pricerunner.com
-> hosting: AWS CloudFront (AS16509), IP 54.230.114.97, nodo dub56 (Dublín); sin IPv6
-> organización: PriceRunner International AB, Sveavägen 46, Stockholm → misma dirección que Klarna Bank AB (sede compartida del grupo)
-> DNS admin: awsdns-hostmaster@amazon.com (valor por defecto de Route 53, coincide con los NS de whois)
-> trackers: los mismos 5 de Google que www.klarna.com (Analytics, Tag Manager, DoubleClick, AdSense, AdMob)
-> la sección SSL/TLS no aparece para este sitio en la versión gratuita
-> mismas discrepancias que en klarna.com ("DNSSEC Enabled", NS de MarkMonitor) → se da por bueno whois
siguiente: técnica 5, robots.txt y security.txt de www.klarna.com y www.pricerunner.com (con la cabecera X-Bug-Bounty)
```

```
2026-11-02 11:53 · objetivo: www.klarna.com, www.pricerunner.com (in scope) · 4 peticiones, cabecera X-Bug-Bounty: h1-lbaeutr, 2 s entre ellas
$ curl.exe -s -H "X-Bug-Bounty: h1-lbaeutr" -o <fichero> -w "%{http_code} %{redirect_url}" https://<host>/robots.txt | /.well-known/security.txt
-> www.klarna.com/robots.txt (200): 42 Disallow + 1 Allow + Sitemap (/sitemaps/sitemap-index.xml)
   - /*/shopping/... (track, checkout, login, forum, profile, gotostore, ct, 70081414…) → las mismas rutas que pricerunner.com: el comparador está integrado en klarna.com
   - nombres de APIs internas: search-compare-gateway, frontend-transition-page, search-edge-rest, product-information-edge-rest
   - también bloquea /*/auth/ y, curiosamente, /.well-known/security.txt
-> www.pricerunner.com/robots.txt (200): fechado "#PRUK 18/09/2023"; bloquea ~38 bots (scrapers y SEO) con Disallow: /; para el resto, mismas rutas que /*/shopping/ de klarna.com
-> security.txt: 404 en los dos, pese a tener programa de bug bounty; la respuesta es un error XML "NoSuchKey" de Amazon S3 → el origen web sirve desde un bucket S3 detrás de CloudFront
siguiente: técnica 6, servicios expuestos con InternetDB a partir de las IP de subs_resueltos.csv
```

```
2026-11-02 17:35 · objetivo: IP de los 1921 subdominios vivos (subs_resueltos.csv)
$ extraer IP únicas y clasificarlas: privadas (RFC 1918 + 100.64/10), CDN/terceros (CNAME a cloudfront.net o en subs_terceros.csv) y públicas propias
-> 3216 IP únicas → privadas 977 · CDN o terceros 392 · públicas a consultar 2115 (una IP puede caer en más de un grupo según el subdominio)
-> 480 subdominios públicos resuelven a IP privadas (10.x, 172.16-31.x, 192.168.x) → el DNS público publica direcciones de la red interna (fuga de información)
-> las IP privadas y de CDN no se consultan en InternetDB: no tienen datos útiles o son nodos compartidos de Amazon
siguiente: consultar en InternetDB las 2115 IP públicas (ips_objetivo.txt) y quedarse con las que exponen puertos distintos de 80/443
```

```
2026-11-02 17:38 · objetivo: 2115 IP públicas de subdominios en alcance (ips_objetivo.txt)
$ Invoke-RestMethod https://internetdb.shodan.io/<ip>  (300 ms entre consultas, 14 min) → internetdb.csv
-> 688 de 2115 IP con datos en Shodan; puertos: 80 (620), 443 (563); casi nada más → superficie expuesta muy contenida
-> engineering.klarna.com (162.159.152.4, .153.4) e investors.klarna.com (162.159.129.11): IP de Cloudflare sin CNAME;
   los puertos 2052-2096, 8080, 8443 y 8880 son los alternativos que Cloudflare abre en todos sus proxies, no servicios de Klarna → hosting de terceros (dudoso)
-> ob-de-modulith-us.production.c2c.klarna.net (100.61.34.31): 80, 443 y 8080, tag "cloud", 0 vulns → único puerto alternativo propio (8080)
-> nxdomain.klarna.net y cb-sta-account-lookup (nonprod/playground/production .eu1.klarna.net) resuelven a 127.0.0.1 → registros a localhost en DNS público
   (el puerto 5060 que da Shodan para 127.0.0.1 no tiene sentido y se descarta)
-> ftp.pricerunner.com (18.196.146.3) y vpn/pocvpn.pricerunner.com (99.80.232.166): InternetDB no tiene datos → el banner FTP solo consta en DNSDumpster
-> ninguna IP con CVE asociados en InternetDB
siguiente: técnica 7, Google dorks
```

```
2026-11-02 17:58 · objetivo: klarna.com, pricerunner.com (in scope) · búsquedas en Google (ventana de incógnito), sin abrir resultados
$ site:klarna.com -www -docs -developers
-> status.klarna.com (Statuspage), engineering.klarna.com (blog en Medium → explica las IP de Cloudflare), myshop.klarna.com (tiendas creadas por usuarios),
   creator.klarna.com (plataforma de creadores), brand.klarna.com (guías de marca, Vercel)
-> nuevo: drive-to-store-ads.klarna.com, indexado como "Klarna Partner Portal" (informes para socios comerciales)
$ site:klarna.com filetype:pdf
-> todos en owp.klarna.com (One Web Platform; rutas /assets/sites/AAAA/MM/ y /legacy/): informes anuales y ESG 2019-2022, suplemento de folleto 2022, formulario fiscal alemán → documentación corporativa pública
$ site:klarna.com (filetype:xlsx OR filetype:docx OR filetype:pptx OR filetype:csv)  → 0 resultados
$ site:klarna.com (inurl:login OR inurl:admin OR inurl:portal OR inurl:signin)  → 0; repetido como site:klarna.com inurl:login → 0
-> coherente con robots.txt (bloquea /*/auth/ y /*/shopping/login/): Klarna no deja indexar sus páginas de acceso
$ site:klarna.com inurl:playground  → 0 (205 subdominios playground según subfinder, ninguno indexado)
$ site:pricerunner.com -www
-> vpn.pricerunner.com y pocvpn.pricerunner.com indexados como "Please Login": "Token clock drift detected… Launch FortiClient. Single Sign-On"
   → portal SSL-VPN de Fortinet (FortiGate) con segundo factor por token y SSO; confirma el uso de la IP 99.80.232.166 vista en DNSDumpster
-> newsroom.pricerunner.com: notas de prensa (alojado en Azure)
siguiente: técnica 8, correos (Hunter.io y theHarvester)
```

```
2026-11-02 18:16 · objetivo: klarna.com, pricerunner.com (in scope) · solo lectura, sin contactar con nadie; no se anotan nombres ni correos personales
$ navegador: https://hunter.io/domain-search → klarna.com y pricerunner.com (cuenta gratuita propia)
-> klarna.com: 1161 correos (1086 personales, 143 directivos, 75 genéricos)
   por departamento: IT/Ingeniería 389, Management 125, Ventas 122, Data & Research 75, Marketing 61, Producto 45, Executive 33, Finanzas 29, Legal 29,
   Operaciones 25, Soporte 18, Diseño 18, Comunicación 12, otros <5 y 93 sin departamento → un tercio de ingeniería
-> genéricos klarna.com: feedback@, service@, hello@, usa@ y buzones con sufijo de país <función>.<país>@ (press.us@, dataprotection.ca@, datenschutz.ch@)
-> pricerunner.com: 18 correos (7 personales, 11 genéricos) → la mayoría del personal usa ya @klarna.com
   genéricos: info@, infose@, infouk@, complaints@, abuse@, annonsering@, skadeanmalan@, skadesanmeldelse@, listnings@ (errata de "listings")
-> ficha de empresa en Hunter: 1001-5000 empleados, Sveavägen, Stockholm (coincide con whois y Netcraft)
$ theHarvester 5.0.0 -d <dominio> -b duckduckgo,crtsh,hackertarget,rapiddns,otx -l 200 -f C:\kyt\harvester_<dominio>   (18:23)
-> 0 correos, 0 hosts, 0 IP en ambos dominios → incoherente con crt.sh (2682 nombres): las fuentes sin clave de API devuelven vacío; se descarta como fuente
$ Invoke-RestMethod https://api.hunter.io/v2/domain-search?domain=<dominio>&limit=1   (18:29, API de Hunter, clave propia)
-> patrón de correo personal: {first}.{last}@klarna.com y {first}.{last}@pricerunner.com
-> accept_all: False en ambos → el servidor rechaza direcciones inexistentes (permitiría validar correos; solo se anota)
siguiente: redactar mapa.md con todo lo recogido
```
