# Alcance · Klarna

## El programa

El objetivo de este proyecto es el programa de bug bounty de **Klarna** en HackerOne (https://hackerone.com/klarna). Klarna es una fintech sueca conocida por los pagos aplazados, el "compra ahora y paga después", y también es dueña del comparador de precios PriceRunner, que entra en el alcance.

Consulté la política el **1 de noviembre de 2026**. La versión vigente en ese momento era la del 15 de septiembre de 2026.

Es un programa **público, activo y con recompensa**, gestionado por HackerOne y con *Gold Standard Safe Harbor*. Esto último significa que Klarna se compromete a no emprender acciones legales contra quien investigue respetando sus reglas.

Hay un detalle que conviene aclarar: para *enviar* informes, HackerOne pide tener una reputación mínima (*Signal* de 1.0) o empezar con informes de prueba. Eso solo afecta a quien reporta vulnerabilidades. Leer la política y hacer reconocimiento pasivo no tiene ninguna restricción.

## Qué puedo investigar

El alcance gira en torno a cuatro comodines, que cubren todos los subdominios de estos dominios:

- `*.klarna.com`, el dominio principal. Aquí entra también `app.klarna.com`, la API de la app, que el programa menciona por separado.
- `*.klarna.net`
- `*.klarnacdn.net`, su red de distribución de contenidos.
- `*.pricerunner.com`, el comparador del grupo.

Además, el programa incluye el **Merchant Portal**, pero solo en su entorno de pruebas (`portal.playground.klarna.com`), y las **apps móviles** de Android e iOS. Las apps no las voy a usar en este proyecto, porque el trabajo es de reconocimiento de infraestructura.

## Qué queda fuera

Klarna excluye de forma explícita tres hosts: `locker.klarna.com`, `jobs.pricerunner.com` y `nuji.com`.

También excluye algunas **rutas concretas** dentro de hosts que sí están permitidos. Son `https://app.klarna.com/us/api/connected_card_bff/` y la página `swagger-ui.html` de `api.pricerunner.com`, `api-us.pricerunner.com` y `api-stage.pricerunner.com`. Es decir, el host se puede investigar, pero esas rutas no.

Queda fuera, además, todo lo relacionado con **Kustom**.

La exclusión más delicada es la de los **subdominios operados por terceros**. Aunque un subdominio cuelgue de un comodín, por ejemplo `algo.klarna.com`, si en realidad lo gestiona otra empresa no forma parte del programa. La propia política explica cómo comprobarlo:

- que el `whois` del dominio diga que la organización registrante es Klarna;
- que el `dig` no apunte a infraestructura de un tercero.

Por eso, en el mapa, cada subdominio pasará esa comprobación antes de darlo por bueno.

Por último, todo lo que no aparezca en la lista de arriba está fuera. Por ejemplo, `klarna.de` o `klarna.es`: son de Klarna, pero el programa no incluye esos dominios.

## Las reglas y cómo me afectan

El enunciado pide revisar cuatro cosas concretas. Esto es lo que dice la política sobre cada una.

**¿Permite herramientas automáticas?** No, y lo dice claramente, el uso de escáneres y herramientas automáticas está *estrictamente prohibido*. Encaja con la regla del proyecto, que es trabajar solo con técnicas pasivas. Herramientas como subfinder, crt.sh, Shodan, InternetDB, DNSDumpster o Netcraft no tocan los servidores de Klarna: consultan bases de datos públicas de terceros. Lo único que toca directamente a Klarna es leer `robots.txt` y `security.txt`, y eso lo hago a mano, con una sola petición.

**¿Hay límite de peticiones?** No fija un número concreto, pero pide no degradar ni interrumpir el servicio, y la denegación de servicio está prohibida. Como además no se permiten herramientas automáticas, mis peticiones directas a Klarna serán puntuales.

**¿Prohíbe contactar con empleados?** Sí. La ingeniería social (phishing y similares) contra empleados, clientes o contratistas está prohibida. En este proyecto no contacto con nadie: LinkedIn y Hunter.io los consulto solo en modo lectura, para entender la organización y el patrón de correo.

**¿Hay algún requisito de identificación?** Sí, y es importante. Toda la actividad tiene que poder atribuirse a un investigador, así que cada petición debe llevar la cabecera `X-Bug-Bounty: h1-lbaeutr`. También pide usar el alias `<handle>@wearehackerone.com` para cualquier registro o formulario. Como en este proyecto no se crean cuentas ni se rellenan formularios, lo que me afecta es la cabecera: la llevarán tanto mis peticiones con `curl` como las herramientas del agente.

Hay otras reglas del programa que también tengo en cuenta:

- **Privacidad.** Si me encontrara datos de clientes o información sensible, no la copiaría ni la publicaría. La anotaría sin el dato, avisaría al profesor y, si hiciera falta, se informaría por HackerOne.
- **Confidencialidad.** La política dice que la información obtenida es confidencial para Klarna. Como este repositorio es público, en el cuaderno y en el mapa solo aparece información que ya es pública, nunca nada sensible.
- **No ir más allá de lo necesario.** El programa prohíbe pivotar o explorar sistemas más de lo mínimo. En una fase pasiva no aplica, pero es la misma filosofía.

## Decisiones que he tomado al escribir el `scope.txt`

**He añadido los dominios raíz.** El scope-guard del agente interpreta `*.klarna.com` como "solo subdominios", así que `klarna.com` a secas quedaría fuera. Lo mismo pasa en la batería de ejemplo del enunciado, donde `empresa.com` sale como "Fuera". He añadido `klarna.com`, `klarna.net`, `klarnacdn.net` y `pricerunner.com` por dos motivos:

- la técnica de "registro del dominio" (whois) se hace precisamente sobre el dominio raíz;
- la propia política pide hacer `whois` y `dig` de los dominios para comprobar que son de Klarna.

**Algunas exclusiones no caben en el `scope.txt`.** Ese fichero solo distingue por host o por IP, así que no puede bloquear una ruta concreta ni saber si un subdominio lo opera un tercero. Esas exclusiones las dejo comentadas en el propio `scope.txt` y las respeto a mano. 

**He excluido `nuji.com` de forma explícita.** En realidad ya quedaría fuera porque no encaja con ningún comodín, pero prefiero que se vea claramente que sé que está excluido.