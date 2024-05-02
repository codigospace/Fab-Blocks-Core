# Definir la función lambda para convertir un número a la base especificada
change_base = lambda number, base_destiny: format(int(number), {"decimal": "d", "hexadecimal": "x", "octal": "o", "binario": "b"}[base_destiny])

# Ejemplo de uso de la función change_base
numero = "1010"  # Número en binario
base_destino = "octal"  # Convertir a formato octal
numero_convertido = change_base(numero, base_destino)
print("Número convertido a", base_destino, ":", numero_convertido)
