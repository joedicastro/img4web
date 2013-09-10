# img4web

Un script python para optimizar imágenes
[.jpg](http://es.wikipedia.org/wiki/Joint_Photographic_Experts_Group) y
[.png](http://es.wikipedia.org/wiki/Portable_Network_Graphics) para la web.

Sigue los consejos de **"Yahoo Best Practices for Speeding Up Your Web Site"**
sobre la [optimización de imágenes](http://developer.yahoo.com/performance/rules.html#opt_images).

Después de ejecutarlo, tienes una optimización sin perdida para las imágenes.
Un pequeño ahorro de espacio por imagen, pero que acelera la carga de las
paginas web y reduce el consumo de ancho de banda para un sitio web.


## Requisitos previos y Dependencias

Lógicamente, lo primero que necesitamos para ejecutarlo es
[python](http://www.python.org/). Si estamos en Linux o en Mac, normalmente
viene instalado por defecto y no es un problema. Si nos encontramos en Windows,
entonces nos lo podemos bajar de [aquí.](http://www.python.org/download/)

La versión de python necesaria para ejecutar este script es la 2.6

img4web.py solo emplea módulos de la biblioteca estándar de python, por lo que
no necesita ningún otro modulo.

### Programas externos

Emplea el programa [pngcrush](http://pmt.sourceforge.net/pngcrush/) y el comando
**jpegtran** de la [biblioteca libjpeg](http://www.ijg.org/)

En linux están normalmente disponibles en los repositorios de las distribuciones
más populares, e.g.:
En debian, Ubuntu como estos paquetes en sus repositorios: pngcrush & libjpeg-progs

Para instalarlos:

    sudo aptitude install pngcrush
    sudo aptitude install libjpeg-progs

En Windows pngcrush puede ser descargado desde
[aquí](http://sourceforge.net/projects/pmt/files/pngcrush-executables/) y
libjpeg puede ser descargado (como gnuwin32) desde
[aquí](http://gnuwin32.sourceforge.net/downlinks/jpeg.php)

Esto ha sido probado en linux y Windows. Lo siento, no tengo un Mac.

## Instrucciones

Necesitas ejecutar este script dentro de la carpeta donde están las imágenes
que quieres optimizar.

Ejecutarlo es muy sencillo,

_en linux_

    python img4web.py

_en windows_

    (la ruta donde hayas instalado python)\python.exe img4web.py

Al final, tienes una nueva carpeta llamada **processed** donde están guardadas
las nuevas imágenes procesadas.

¡Eso es todo! Sencillo, bonito y rápido!

## Características

Después de la ejecución se muestra un pequeño informe con el ahorro de espacio
de las imágenes por tipo.

Luce así

    ============================================================================
                                        Summary
    ============================================================================
             Original            Processed           Save

    .jpgs:   ( 31)  2.12 MiB     ( 31)  1.82 MiB     301.28 KiB
    .pngs:   ( 10)489.46 KiB     ( 10)368.93 KiB     120.53 KiB
    ----------------------------------------------------------------------------
    Total:   ( 41)  2.60 MiB     ( 41)  2.19 MiB     421.81 KiB


## Como obtenerlo

El código está alojado en un repositorio Git en GitHub, emplea este comando para
poder clonarlo:

    git clone git://github.com/joedicastro/img4web.git

## Contribuciones

Las contribuciones y las ideas son bienvenidas. Para contribuir a la mejora y
evolución de este script, puedes enviar sugerencias o errores a través de el
sistema de issues.

## Licencia

Este script están sujeto a la [Licencia GPLv3 ](http://www.gnu.org/licenses/gpl.html)
