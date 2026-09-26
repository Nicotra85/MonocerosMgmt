# Auditoría y refuerzo de seguridad — Monoceros

Fecha: 26 de septiembre de 2026.

**Resultado:** se reforzó una copia local del sitio estático y se verificó su funcionamiento. No se modificaron GitHub, Vercel, Yardi, DNS ni la web publicada. Ninguna auditoría garantiza que un sitio sea imposible de atacar.

## Alcance y arquitectura encontrados

Se revisó la opción original del código de Monoceros disponible: 20 páginas de contenido bilingüe, recursos estáticos y marcadores para el futuro portal Yardi. Se añadieron entrada y página 404. No hay servidor de aplicación, panel administrador, base de datos, cuentas de usuarios, sesiones, archivos privados, formularios de subida, cobros ni webhooks. No se encontró un manifiesto de dependencias de aplicación que actualizar.

No se inspeccionaron el historial Git, los miembros del repositorio, los secretos de las cuentas, los despliegues existentes, otros proyectos del dominio ni la configuración privada del proveedor. El escaneo local de patrones de claves no encontró coincidencias; no demuestra que nunca haya habido una filtración.

## Estado de las medidas solicitadas

| Medida | Estado comprobado y trabajo pendiente |
|---|---|
| Revisar permisos | Flujo CI preparado con `contents: read` y credenciales no persistentes. Pendiente revisar colaboradores, roles, tokens, aplicaciones conectadas y reglas de ramas en GitHub/Vercel. |
| Proteger panel administrador | No existe panel en este código. Los paneles de GitHub/Vercel son externos: activar MFA, revisar miembros y eliminar accesos innecesarios. |
| Separar datos entre clientes | No se almacenan datos de clientes. Antes de activar informes, verificar en Yardi que cada usuario solo acceda a sus entidades y documentos; probar con dos cuentas de clientes diferentes y una sin permisos. |
| Blindar base de datos | No hay base de datos. Si se añade, requiere permisos mínimos, aislamiento de red, cifrado y autorización por cliente en servidor; no queda resuelto por este paquete. |
| Ocultar claves privadas | No se detectaron claves de los formatos revisados en archivos públicos. Se añadieron exclusiones y comprobaciones. Los secretos futuros deben permanecer en el servidor/proveedor, nunca en HTML/JS. Revisar y rotar cualquier clave expuesta anteriormente. |
| Asegurar inicio de sesión | Los botones son marcadores y no recogen contraseñas. Login futuro en el portal oficial de Yardi con autenticación gestionada por ese servicio. |
| Caducar sesiones | El sitio no crea sesiones. Expiración, revocación y cierre de sesiones deben configurarse y probarse en los proveedores. |
| Doble factor | No activado desde los archivos. Activar MFA/passkeys en GitHub, Vercel, correo de recuperación y las cuentas de Yardi que lo admitan. Guardar códigos de recuperación fuera del repositorio. |
| Bloquear inyección SQL | No hay consultas SQL ni backend expuesto. Si se añade, usar consultas parametrizadas y permisos mínimos; no afirmar que el control existe ahora. |
| Evitar código malicioso | Implementado: scripts locales separados, CSP sin `unsafe-inline` ni `unsafe-eval`, bloqueo de handlers inline, objetos incrustados y framing. Intento de inyección inline bloqueado en prueba real de navegador. Es defensa adicional, no una garantía contra quien controle el repositorio. |
| Proteger acciones sensibles | No existen operaciones con efectos de negocio. Futuros cambios de cuentas, informes o pagos necesitan autorización en servidor, reautenticación y protección CSRF cuando proceda. |
| Validar archivos subidos | No se aceptan subidas. Si se añade esa función, implementar controles de tamaño, tipo real, nombres, análisis y almacenamiento privado separado antes de habilitarla. |
| Bloquear accesos internos | Sin endpoints de servidor ni solicitudes a URLs aportadas por visitantes. `connect-src 'none'` restringe conexiones iniciadas por el navegador; no es una protección de red interna o SSRF de un futuro servidor. |
| Verificar webhooks | No existen. Antes de añadirlos, validar firmas, antigüedad y reenvíos en el servidor. |
| Evitar pagos duplicados | No se procesan pagos. Los pagos de residentes deben ir al portal autorizado; cualquier futura integración necesita idempotencia y restricciones transaccionales en servidor. |
| Limitar solicitudes excesivas | Pendiente configuración WAF/rate limiting en Vercel, observando tráfico real. No se añadió un contador de JavaScript que se pueda eludir. Ajustar reglas sin bloquear la reproducción de videos o visitantes legítimos. |
| Actualizar dependencias vulnerables | No hay paquetes de aplicación instalables en el sitio. El nuevo checkout de CI queda fijado a un commit de v7.0.1 verificado en el repositorio oficial; Dependabot semanal preparado para Actions. No se ejecutó un escaneo de la infraestructura administrada del proveedor. |
| Cerrar paneles expuestos | No se encontraron rutas de panel en los archivos. `/admin`, `/api`, `/.env`, `/.git/config` y `/backup.zip` devuelven 404 en el servidor local de prueba. Falta comprobar dominio real, subdominios y despliegues antiguos. |
| Detectar accesos sospechosos | Pendiente habilitar/revisar registros, alertas y destinatarios en los proveedores. No hay un servicio de vigilancia continuo instalado en este sitio estático. |
| Probar restauración de backups | Probada copia y restauración local de los archivos con SHA-256 y nueva ejecución del auditor. No se probó una recuperación de base de datos ni de cuentas; no se configuraron backups externos periódicos. |

## Cambios aplicados en los archivos

- Política CSP restrictiva con autorización por hash únicamente para los bloques SEO JSON-LD; el código ejecutable está en recursos locales.
- Cabeceras contra framing y detección ambigua del tipo de archivo; política de referer y restricciones de cámara, micrófono, geolocalización, pagos y otras capacidades innecesarias.
- HSTS preparado para el dominio que sirva el sitio, sin extenderlo a subdominios ajenos. Su efecto debe comprobarse después del despliegue HTTPS.
- Carpeta pública separada de pruebas, configuración y documentación.
- Conservación de `noindex` mientras el sitio siga siendo una vista previa. No equivale a autenticación.
- Comprobaciones de archivos inesperados, enlaces simbólicos, recursos de scripts/estilos, patrones de secretos y superficies activas nuevas.
- CI sin permisos de escritura, sin secretos propios, checkout fijado por SHA y actualización periódica preparada.

**Excepción externa:** se mantienen Manrope y Syne mediante Google Fonts, autorizando únicamente sus dominios de estilos y fuentes. La descarga para alojarlas localmente no estuvo disponible en este entorno. Las pruebas de navegador excluyeron esas solicitudes externas y usaron las fuentes de reserva; los archivos de imágenes, videos, CSS del sitio y JavaScript sí se probaron localmente. No se incorporaron scripts de terceros.

## Pruebas y límites

Se verificaron las 20 páginas, JavaScript sin errores de ejecución, recursos locales, filtros 5/4/9, marcador de Yardi, vista móvil sin desbordamiento, movimiento reducido y los dos videos de la portada reproduciéndose con autoplay, muted y loop. La navegación normal no produjo violaciones CSP; la inyección deliberada sí se bloqueó. La sintaxis de los archivos JS pasó la comprobación de Node.

La revisión independiente no encontró bloqueos actuales; sus dos mejoras sobre enlaces simbólicos y dependencias CSS se incorporaron al auditor. Es una revisión de código y pruebas funcionales/defensivas, no un pentest completo del entorno publicado. Los resultados concretos están en `EVIDENCIA.json`.

## Pendientes prioritarios de las cuentas

1. Activar protección real de acceso para todas las URLs privadas antes de subir a una rama con despliegue automático. Verificar en incógnito y con un usuario no autorizado. La cobertura de producción debe comprobarse según el plan; no asumir que proteger solo las previews protege el dominio principal.
2. Activar MFA/passkeys, revisar usuarios, accesos de aplicaciones y tokens; retirar los que no correspondan. Configurar revisión obligatoria antes de integrar y exigir el check de seguridad, cuando la cuenta lo permita.
3. Verificar WAF/rate limiting y alertas. Revisar intentos bloqueados y acceso administrativo. Documentar responsable y respuesta ante incidentes.
4. Mantener una copia versionada externa, con acceso restringido, de código, recursos y configuración recuperable. Probar periódicamente la restauración en un despliegue protegido; acordar pérdida máxima de datos y tiempo de recuperación tolerables.
5. Antes de conectar Yardi, validar URLs oficiales, roles, separación de clientes, MFA disponible, expiración y revocación de sesiones con cuentas de prueba. No añadir informes al directorio público.

Para completar esas verificaciones hace falta acceso autorizado a las cuentas o configuración compartida sin secretos, más la URL exacta del sitio. No envíes contraseñas ni claves privadas por chat.

## Referencias oficiales consultadas

- Vercel Deployment Protection: https://vercel.com/docs/deployment-protection
- Vercel Authentication: https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication
- Configuración `vercel.json`: https://vercel.com/docs/project-configuration/vercel-json
- Vercel WAF / rate limiting: https://vercel.com/docs/vercel-firewall/vercel-waf/rate-limiting
- Seguridad de GitHub: https://docs.github.com/en/code-security/getting-started/github-security-features
- Release checkout y commit fijado: https://github.com/actions/checkout/commit/3d3c42e5aac5ba805825da76410c181273ba90b1
- CSP: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
