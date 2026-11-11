

# Informe de Reconocimiento Pasivo — klarna.com

## 1. Registro del dominio

| Campo | Valor | Fuente |
|-------|-------|--------|
| Dominio | KLARNA.COM | `(whois_dominio)` |
| Fecha de alta | 2008-12-12 | `(whois_dominio)` |
| Fecha de caducidad | 2027-12-12 | `(whois_dominio)` |
| Última modificación | 2026-10-29 | `(whois_dominio)` |
| Registrador | Entidad #299 (cómputo interno RDAP) | `(whois_dominio)` |
| Estado | `client transfer prohibited` | `(whois_dominio)` |
| Nameservers WHOIS | A1-74.AKAM.NET, A12-65.AKAM.NET, A20-66.AKAM.NET, A5-64.AKAM.NET, EDNS7.ULTRADNS.COM, EDNS7.ULTRADNS.ORG | `(whois_dominio)` |

---

## 2. DNS y postura de correo

### Registros DNS

**A** — `(dns_registros)`
- 3.173.21.37
- 3.173.22.37
- 3.173.23.37

**NS** — `(dns_registros)`
- a1-74.akam.net
- a12-65.akam.net
- a20-66.akam.net
- a5-64.akam.net
- edns7.ultradns.com
- edns7.ultradns.org

**MX** — `(dns_registros)`
- 10 mxz1.klarna.com
- 10 mxz2.klarna.com
- 10 mxz3.klarna.com
- 10 mxz4.klarna.com

**TXT** — `(dns_registros)`
- **SPF**: `v=spf1 include:sendgrid.net include:_spf.google.com include:_spf.atlassian.net include:spf-0098b101.pphosted.com ip4:18.159.145.12 ip4:18.156.64.82 ip4:54.77.2.88 ip4:54.72.124.243 -all`
- Múltiples registros de verificación de terceros: Google, Apple, Stripe (3), Atlassian, Amazon SES, Microsoft, Docusign, Facebook, Twilio, Adobe, Palo Alto Networks, Mixpanel (3), Notion, Loom, Eleventlabs, Anthropic (2), Miro, OneTrust, Cursor, Planet Scale, Docker, Jamf, H1 (3).

### Postura de correo — `(correo_postura)`

| Protocolo | Valor |
|-----------|-------|
| **SPF** | `v=spf1 include:sendgrid.net include:_spf.google.com include:_spf.atlassian.net include:spf-0098b101.pphosted.com ip4:18.159.145.12 ip4:18.156.64.82 ip4:54.77.2.88 ip4:54.72.124.243 -all` |
| **DMARC** | `v=DMARC1; p=reject; adkim=r; aspf=r; fo=1; rua=mailto:dmarc-reports@klarna.com` |
| **DNSSEC** | **Sin firmar** |
| **CAA** | `0 issue "quovadisglobal.com"`, `0 issue "e-szigno.hu"`, `0 issue "amazonaws.com"`, `0 issuewild "amazonaws.com"`, `0 issue "digicert.com"`, `0 issue "buypass.no"`, `0 issuewild "digicert.com"`, `0 iodef "mailto:dns-admin@klarna.com"` |

**Análisis de postura de correo:**
- SPF con `-all` (soft fail → hard reject) y múltiples includes de terceros (SendGrid, Google, Atlassian, Proofpoint) + IPs de AWS → **bien configurado**.
- DMARC con `p=reject` y políticas estrictas (`adkim=r`, `aspf=r`) → **postura fuerte**.
- DNSSEC **no implementado** en la zona.
- CAA restringe a 5 emisores de certificados; Amazon AWS y DigiCert con wildcard habilitado.

---

## 3. Subdominios (transparencia de certificados)

**`(subdominios_crtsh)`**

- **720 subdominios** identificados en alcance (2 filtrados por estar fuera).
- **Patrones detectados:**
  - **Producción:** `api.klarna.com`, `app.klarna.com`, `auth-bp.klarna.com`, `boost.klarna.com`, `banktransfer.klarna.com`, `about.klarna.com`, `blog.klarna.com`, `articles.klarna.com`...
  - **APIs:** `api-eu.klarna.com`, `api-na.klarna.com`, `api-na-2.klarna.com`, `api-naz.klarna.com`, `api-oc.klarna.com`, `api-global.klarna.com`, `api-production.core-banking.klarna.com`, `api.kosma.klarna.com`, `api.savings.klarna.com`, `api.topup.klarna.com`, `api.ident.klarna.com`...
  - **Portales:** `api.eu.portal.klarna.com`, `api.us.portal.klarna.com`, `auth.eu.portal.klarna.com`, `auth.us.portal.klarna.com`, `apps-config.eu.portal.klarna.com`, `apps-config.us.portal.klarna.com`...
  - **Entornos no-producción:** `*.nonprod.klarna.com`, `*.playground.klarna.com`, `*.staging-e.klarna.com`, `*.test.klarna.com`...
  - **CI/CD e internal:** `*.jenkins.nonprod.klarna.com`, `bastion.nonprod.klarna.com`, `bastion-staging.klarna.com`...
  - **Mobile:** `*.m.klarna.com`, `ablink.m.klarna.com`
  - **Migración/legacy:** `agera.klarna.com` (Adyen Agera)
  - **Financiera:** `application.treasury-automation.klarna.com`, `api.topup.klarna.com`, `api.savings.klarna.com`

**Subdominios filtrados (fuera de alcance):** 2

---

## 4. Infraestructura de IP

### klarna.com — `(infraestructura_ip)`

| IP | ASN / Dueño | PTR | Tipo |
|----|-------------|-----|------|
| 3.173.21.37 | AS16509 AMAZON-02 — Amazon.com, Inc., US | — | **Nube (AWS)** |
| 3.173.22.37 | AS16509 AMAZON-02 — Amazon.com, Inc., US | — | **Nube (AWS)** |
| 3.173.23.37 | AS16509 AMAZON-02 — Amazon.com, Inc., US | — | **Nube (AWS)** |

Los nombreservers de Akamai (`a*-akam.net`) y UltraDNS (`edns7.ultradns.com/org`) gestionan la resolución DNS (CDN/WAF de nivel DNS), pero la capa de aplicación (A records) apunta directamente a infraestructura AWS.

### Servidores de correo MX — `(infraestructura_ip)`

| Host | IP | ASN / Dueño | PTR | Tipo |
|------|----|-------------|-----|------|
| mxz1.klarna.com | 52.30.236.203 | AS16509 AMAZON-02 — Amazon.com, Inc., US | ec2-52-30-236-203.eu-west-1.compute.amazonaws.com | **Nube (AWS)** |
| mxz2.klarna.com | 54.73.174.245 | AS16509 AMAZON-02 — Amazon.com, Inc., US | ec2-54-73-174-245.eu-west-1.compute.amazonaws.com | **Nube (AWS)** |
| mxz3.klarna.com | 3.73.181.240 | AS16509 AMAZON-02 — Amazon.com, Inc., US | ec2-3-73-181-240.eu-central-1.compute.amazonaws.com | **Nube (AWS)** |
| mxz4.klarna.com | 35.156.176.213 | AS16509 AMAZON-02 — Amazon.com, Inc., US | ec2-35-156-176-213.eu-central-1.compute.amazonaws.com | **Nube (AWS)** |

Los MX están distribuidos en al menos dos regiones de AWS (eu-west-1 e eu-central-1), lo que indica alta disponibilidad y resiliencia geográfica.

---

## 5. Observaciones y superficie de ataque

1. **CDN/WAF DNS vs. aplicación:** El DNS se resuelve vía Akamai + UltraDNS (DNS managed), pero la aplicación corre directamente sobre AWS EC2. Esto sugiere que el WAF/CDN de Akamai podría estar en capas superiores (no visible en el registro A de `klarna.com` directamente, posiblemente gestionado a nivel de Load Balancer o CloudFront).

2. **Exposición masiva:** 720 subdominios en alcance es una superficie considerable. Los patrones `*.playground.*`, `*.nonprod.*`, `*.staging.*` y `*.jenkins.*` son candidatos a activos menos protegidos y de mayor riesgo.

3. **Dependencia de terceros:** El SPF incluye SendGrid, Google Workspace, Atlassian y Proofpoint. Cada uno añade IPs y políticas de correo externas que amplían la superficie de phishing/spoofing.

4. **DNSSEC ausente:** La zona no está firmada, lo que deja abierta la posibilidad de ataques de intercepción DNS (cache poisoning, etc.).

5. **Infraestructura:** 100% AWS para la capa de aplicación y correo. Ninguna IP de CDN/WAF visible en la resolución A directa, ni de proveedores alternativos de nube.