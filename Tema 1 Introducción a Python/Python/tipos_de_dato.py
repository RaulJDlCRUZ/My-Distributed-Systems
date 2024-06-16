'''
-------TIPOS DE DATO BASE EN PYTHON----------
Texto:	        str
Numericos:	    int, float, complex
Secuenciales:	list, tuple, range
Mapping:	    dict
Conjuntos:	    set, frozenset
Booleano:	    bool
Binarios:	    bytes, bytearray, memoryview
Nulo:	        NoneType
'''

_nueva_cadena = str("Hola mundo!")

_nuevo_entero = int(30)
_nuevo_decimal = float(20.5)
# Es en este caso 0 + 1j (0 en la parte real, 1 en la imaginaria)
_nuevo_complejo = complex(1j)

_nueva_lista = list(("Seat", "Mazda", "Volvo"))
# Una lista pero no se puede modificar
_nuevo_tuple = tuple(("Manzana", "Plátano", "Cereza"))
# Secuencia de números. Por defecto se empieza por el cero hasta n-1, y va de 1 en 1
_nuevo_rango = range(6)

_nuevo_diccionario = dict(nombre="John", edad=36)  # Duplas clave-valor.

_nuevo_conjunto = set(("LC2", "XJR-9 LM", "R90CK"))
_conjunto_final = frozenset(
    ("Samsung", "Oneplus", "Realme"))  # Conjunto inmutable

# Variable booleana. Evalúa el contenido del paréntesis. En este caso ¿5>0?
_nuevo_booleano = bool(5)

_nuevo_bytes = bytes(5)  # Crea un conjunto de N bytes inmutable
# Como el anterior pero sí puede modificarse. En este caso
_nuevo_array_de_bytes = bytearray("5", 'utf-8')
# Se reserva un segmento de memoria
_nueva_vista_a_memoria = memoryview(bytes(5))

_nuevo_vacio = None  # Objeto nulo

'''
Entonces cómo saco el tipo de dato de una variable? Así:
'''
mivar = 1
print("Sacando el tipo de dato de x... ", type(mivar))

"""
Dos cosas:
    1. Con la coma hacemos la concatenación
    2. Sale algo tipo <class ' EL TIPO DE DATO '>
"""

_mi_entero, _mi_decimal, _mi_caracter = int(50), float(100), str(10)
print(_mi_entero, _mi_decimal, _mi_caracter)  # Ejemplo de concatenación
