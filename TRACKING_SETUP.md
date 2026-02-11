# Guía de Instalación de Tracking Scripts

Este documento detalla cómo instalar correctamente los scripts de seguimiento (Meta Pixel y UTMify) en el proyecto.

## 1. Meta Pixel (Facebook)

El Meta Pixel debe instalarse en la sección `<head>` de tu archivo HTML (`index.html`).

**Código a insertar:**

```html
<!-- Meta Pixel - Reemplaza con tu ID si es necesario -->
<script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '1536230360782560'); 
    fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
    src="https://www.facebook.com/tr?id=1536230360782560&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
```

**Ubicación:** Pegar justo antes de la etiqueta de cierre `</head>`.

---

## 2. UTMify (Rastreo de Ventas)

El script de UTMify ayuda a rastrear el origen de las ventas y debe cargarse en todas las páginas.

**Link del Script:**
`https://cdn.utmify.com.br/scripts/utms/latest.js`

**Código a insertar:**

```html
<script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-subids async defer></script>
```

**Ubicación:** Se recomienda colocarlo dentro de la etiqueta `<head>`, después del Pixel de Meta, o al inicio del `<body>`.

---

## Resumen de Ubicación en `index.html`

```html
<head>
    ...
    <!-- Meta Pixel -->
    <script>...</script>
    
    <!-- UTMify -->
    <script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-subids async defer></script>
</head>
<body>
    ...
</body>
```
