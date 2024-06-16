# Serialización

Es el proceso de codificar los datos que manejan los programas (enteros, cadenas, imágenes, etc.) en secuencias de bytes susceptibles de ser almacenadas en un fichero o enviadas a través de la red.

## Tipos multibyte y ordenamiento

1\. Escriba un programa Python que determine el tipo de ordenamiento que utiliza el computador que lo ejecuta.
----
**Método 1**
```python
import sys
# Python ofrece una forma específica de conocer el ordenamiento:
print(sys.byteorder)
```

**Método 2**
```python
import struct
# Detectar el orden de los bytes con struct, según el empaquetado con un entero de 16 bits sin signo
print("big endian") if struct.pack('H', 1) == b'\x00\x01' else print("little endian")
```

2\. Escriba la versión C del ejercicio anterior.
----
```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
	unsigned int value = 0x1;
	char *r = (char *) &value;
	
        char *line = (*r == 1) ? "Little Endian" : "Big Endian";

	fprintf(stdout, "Your sistem is... %s\n", line);
	return EXIT_SUCCESS;
}
```
<div align="center">

|   |`struct`: especificación de ordenamiento|
|:-:|:---------------------------------------|
|$@$| ordenamiento nativo del computador (realiza alineamiento)|
|$=$| ordenamiento nativo|
|$<$| _little endian_|
|$>$| _big endian_|
|$!$| ordenamiento de la red (_big-endian_)|

</div>

<div align="center">

|Formato|Significado|Tipo de dato Python|Tipo de dato C|Tamaño estándar|
|:-----:|:----------|:------------------|:-------------|:--------------|
|`x`|De relleno, alineado al siguiente dato|Sin valor|_pad value_|-|
|`c`|Carácter|`bytes` de longitud 1|`char`|1|
|`b`|Byte con signo (`integer`)|`integer`|`signed char`|1|
|`B`|Byte sin signo (`integer`)|`integer`|`unsigned char`|1|
|`?`|_Booleano_ o char (según C99)|`bool`|`_Bool`|1|
|`h`|Entero de 16 bits con signo|`integer`|`short`|2|
|`H`|Entero de 16 bits sin signo|`integer`|`unsigned short`|2|
|`i`|Entero de 32 bits con signo|`integer`|`int`|4|
|`I`|Entero de 32 bits sin signo|`integer`|`unsigned int`|4|
|`l`|Entero largo con signo|`integer`|`long`|4|
|`L`|Entero largo sin signo|`integer`|`unsigned long`|4|
|`q`|Entero de 64 bits con signo|`integer`|`long long`|8|
|`Q`|Entero de 64 bits sin signo|`integer`|`unsigned long long`|8|
|`n`|Nativo|`integer`|`ssize_t`|-|
|`N`|Nativo|`integer`|`size_t`|-|
|`e`|"Media-Precisión" de IEEE 754|`float`|No soportado|2|
|`f`|Coma flotante|`float`|`float`|4|
|`d`|Precisión doble|`float`|`double`|8|
|`s`|Cadena de caracteres (un número previo "$x$" indica tamaño)|`bytes`|`char[]`|$x$|
|`p`|"_Pascal string_" (cadena de longitud variable almacenada en un número fijo de _bytes_)|`bytes`|`char[]`|-|
|`P`|Entero que puede almacenar una dirección de memoria|`integer`|`void*`|-|

<h3><code>struct</code>: especificación de formato</h3>

</div>