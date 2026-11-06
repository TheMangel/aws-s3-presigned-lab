# AWS S3 + Lambda + API Gateway: subida de archivos con URL prefirmada

Proyecto de Computación en la nube. Una página web permite subir archivos a un bucket **privado** de S3 sin exponer credenciales: la página pide a una API una URL prefirmada y sube el archivo directamente a S3.

## Arquitectura

```
Navegador ──GET /generarURL?archivo=x──▶ API Gateway ──▶ Lambda (boto3)
    │                                                        │
    │◀────────────── URL prefirmada (5 min) ◀────────────────┘
    │
    └──PUT archivo──▶ S3 privado (miguel-privado0)
```

- **Bucket público** `mi-sitio-miguel`: aloja la página web (static website hosting).
- **Bucket privado** `miguel-privado0`: recibe los archivos subidos.

## Estructura

```
web/          Página (index.html con login demo y subida) y login-demo.html
lambda/       lambda_function.py (genera la URL prefirmada)
scripts/      s3_Menu.py (menú por consola: subir, descargar, eliminar, listar)
s3-config/    Política del bucket público y CORS del bucket privado
ec2/          user-data.sh (Apache "Hola TALENTOTECH") y crontab.txt (apagado automático)
```

## Pasos para montarlo

1. **Credenciales**: `aws configure` con un usuario IAM (nunca subas las llaves a GitHub).
2. **Buckets**:
   ```
   aws s3 mb s3://mi-sitio-miguel
   aws s3 mb s3://miguel-privado0
   ```
3. **Sitio público**: activar *Static website hosting*, desactivar *Block public access* y aplicar `s3-config/bucket-policy-publico.json`. Subir la página:
   ```
   aws s3 cp web/index.html s3://mi-sitio-miguel/
   ```
4. **CORS del bucket privado**: pegar `s3-config/cors-bucket-privado.json` en Permisos → CORS.
5. **Rol IAM de Lambda**: políticas `AWSLambdaBasicExecutionRole` y `AmazonS3FullAccess` (ojo: *no* `AmazonS3ExpressFullAccess`, da error 403).
6. **Lambda** (Python): pegar `lambda/lambda_function.py`.
7. **API Gateway** (REST): recurso `/generarURL`, método GET, integración Lambda proxy, desplegar en la etapa `prod`.
8. En `web/index.html` la variable `API_URL` ya apunta a la API de este proyecto (`x31uc0n5vk`); si creas otra API, cambia el ID.
9. Abrir el sitio con **http://** (el endpoint de S3 website no soporta HTTPS).

## Menú por consola

```
py scripts/s3_Menu.py
```
Usa el bucket `mi-sitio-miguel`; para cambiarlo: `set BUCKET_NAME=miguel-privado0` (Windows) antes de ejecutar.

## Apagado automático de EC2

Ver `ec2/crontab.txt`. La hora del servidor es UTC (Colombia + 5). La instancia necesita un rol IAM con permiso `ec2:StopInstances`.

## Notas de seguridad

- El login de la página es **solo una demo** (usuario/clave en el código del navegador). Cámbialo o usa autenticación real.
- La validación de archivos (máx. 10 MB, bloqueo de `.exe .bat .cmd .msi .sh`) se hace en el navegador y **se puede saltar**. Para algo real, valida también en la Lambda.
- Cualquiera que conozca la URL de la API puede pedir URLs de subida. Considera una API key, autenticación y restringir el origen en CORS.
- Si alguna vez publicaste una llave de acceso, **rótala** (crea una nueva y elimina la anterior).
