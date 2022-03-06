# BAInternTest
Repositorio para mantener solución a test de programación.

---

La funcionalidad del código implementado se encuentra explicado en el jupyter notebook anexado, se incluye una versión
en html pre-ejecutado.  

Por otro lado, se ha montado una pequeña API con FLASK para consultar las series de tiempo construidas a partir de los 
datos. Previo a la ejecucción se deben instalar las dependencias del archivo `requirements.txt`, por ejemplo, mediante 
el comando:

```{bash}
pip install -qr requirements.txt
```

Luego, para ejectuar la aplicación de Flask, se debe agregar la variable de entorno `FLASK_APP=app`, y una vez hecho 
esto, se procede a ejecutar la aplicación con el comando:

```{bash}
flask run
```
