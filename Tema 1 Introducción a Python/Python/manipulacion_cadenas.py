'''
---------MANIPULACION CON CADENAS---------
'''

# Se almacena en una variable una cadena en la que se incluye cierto formato. Por ejemplo, se almacenan los saltos de línea:
cadena_larga = """Los sistemas operativos inspirados en Unix, como Linux, ofrecen una gran variedad de métodos de
entrada/salida. En particular, el método de descriptores de archivos permite asociar dinámicamente
números enteros con canales de datos, de modo que un proceso pueda hacer referencia a ellos como
sus flujos de datos de entrada/salida."""

print(cadena_larga)
# Demostración: Un String = array de chars
c = cadena_larga[1]
# Debería imprimirse un solo caracter
print(c)
# Recorrer una cadena letra a letra
for i in "palabra":
    # NOTA: Lo de la derecha es para anular el salto de linea, indicando el fin de linea como nulo:
    print(i, end="")
# Longitud de una cadena
print("\nEl texto tiene en total", len(cadena_larga), "palabras")
# Concatenación de cadenas. Saltos de línea, arrays, palabras... lo que sea
cadena_concatenada = "\n" + cadena_larga[2] + cadena_larga[5] + 'milar'
print(cadena_concatenada)
