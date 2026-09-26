# Monoceros — versión con seguridad reforzada

Preparada el 26 de septiembre de 2026. Este paquete contiene la opción original azul/naranja, en inglés y español, con las imágenes y películas existentes. No se ha publicado ni se han cambiado tus cuentas. Mantiene los botones de Yardi como marcadores; no solicita credenciales ni contiene informes privados.

## Qué hacer con el ZIP

1. Descarga y descomprime el ZIP. Guarda una copia del repositorio actual antes de reemplazar archivos.
2. Antes de subirlo a una rama conectada a Vercel, protege los despliegues del proyecto. Confirma que también queden cubiertos el dominio principal, las vistas previas y sus URLs alternativas. La protección disponible depende de tu configuración y plan. Prueba las URLs en una ventana sin iniciar sesión. `noindex` y la etiqueta “Private preview” no restringen acceso.
3. Sube el contenido descomprimido al repositorio: `public`, `vercel.json`, `scripts`, `.github`, `.gitignore` y esta documentación. No subas el ZIP dentro de `public`. Si no ves `.github` o `.gitignore`, activa la visualización de archivos ocultos.
4. En Vercel, la raíz del proyecto debe ser la carpeta que contiene `vercel.json`; la carpeta de salida es `public`. Es un sitio estático, sin framework ni instalación de paquetes. No combines este paquete con configuraciones antiguas de rutas o funciones sin revisarlas. Conserva una rama/copia anterior para volver atrás.
5. La carga a una rama conectada puede iniciar un despliegue automáticamente. No lo hagas hasta haber revisado la protección del punto 2. Después comprueba las cabeceras en el dominio real y prueba los accesos, videos e idioma. Las pruebas incluidas se ejecutaron localmente, no en tu cuenta Vercel.

El flujo de GitHub Actions incluido ejecutará comprobaciones si Actions está habilitado. Tiene permiso de solo lectura y no conserva credenciales. No es por sí mismo un bloqueo de despliegue: exigir que pase antes de integrar cambios o publicar requiere configurar las reglas del repositorio y del proyecto.

## Archivos importantes

- `vercel.json`: cabeceras de seguridad y carpeta pública.
- `public/en.html`, `public/es.html`: páginas principales.
- `public/en/insights/`, `public/es/insights/`: artículos.
- `public/assets/js/`, `public/assets/css/`: código y estilos separados para permitir una política estricta.
- `scripts/security_check.py`: guardas para detectar regresiones habituales, recursos inesperados y algunos patrones de secretos.
- `scripts/restore_test.py`: comprueba una copia y restauración temporal de todos los archivos del paquete.
- `SEGURIDAD.md`: estado de cada medida solicitada y pendientes externos.
- `EVIDENCIA.json`: resultados de las pruebas realizadas.

## Comprobaciones locales

Con Python 3.10 o superior:

```sh
python3 scripts/security_check.py
python3 scripts/restore_test.py
```

No hacen cambios en Vercel, no necesitan claves y no prueban bases de datos. La segunda crea y elimina una copia temporal de prueba; no programa backups ni guarda una copia externa permanente.

Los recursos usan rutas absolutas: para revisar el sitio, usa un servidor local o un despliegue protegido, no doble clic en el HTML. Abrir el HTML directamente tampoco aplica las cabeceras HTTP de `vercel.json`.

## Al editar más adelante

Los scripts nuevos van en archivos `.js`, no pegados directamente dentro del HTML. No agregues `unsafe-inline` o `unsafe-eval` para resolver un error. Los datos SEO JSON-LD tienen hashes autorizados en la política; si cambian, hay que recalcularlos y revisar la política. El comprobador detecta hashes desactualizados. Cambiar texto visible normal no requiere cambiar esos hashes.

No guardes contraseñas, claves de API, informes de inversores, archivos de residentes, backups o bases de datos en `public`. Todo lo que esté allí puede ser descargado por quien tenga acceso al sitio. `.gitignore` solo evita ciertas incorporaciones futuras: no elimina secretos que ya se hayan subido al historial de GitHub.

Para activar Yardi, usa enlaces al portal oficial verificado. La autenticación, permisos por cliente, sesiones y MFA deben quedar en Yardi; no construyas un formulario que capture su contraseña en este sitio.
