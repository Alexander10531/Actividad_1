from pathlib import Path
import pandas as pd

# ==============================================================================
# 1. Definición del diccionario de correcciones
# ==============================================================================
correcciones_utf8_a_latin1_error = {
    'í¡': 'á',
    'í©': 'é',
    'í­': 'í',
    'í³': 'ó',
    'íº': 'ú',
    'í±': 'ñ',
    'í§': 'ç',
    'í¼': 'ü',
    'í²': 'ó',
    'í¨': 'é',
    'í¨n': 'ión',
    'í²r': 'ór',
    'íti': 'íti',
    'ías': 'ías',
    'ían': 'ían',
    'ía': 'ía',
    'Ã‚Â': '¿',
    'Ã¢Â€Âœ': '"',
    'Ã¢Â€Â"': '"',
    'Ã¢Â€Â™': "'",
    'Ã¨': 'è',
    'Ã¯': 'ï',
    'Ã«': 'ë',
    'nÃ‚Âº': 'nº',
    'Ã‚Â·': '·',
    'Ã': '', 
    'Â': '',
    'a r-': 'ar-',
    '€': '€', 
}

# ==============================================================================
# 2. Función para aplicar correcciones del diccionario
# ==============================================================================
def eliminar_caracteres_control(texto):
    """Elimina caracteres de control Unicode problemáticos."""
    # Caracteres de control comunes que causan problemas (U+0080 a U+009F)
    caracteres_control = [chr(i) for i in range(0x0080, 0x00A0) if i not in [0x00A0]]  # Mantener espacio no separador
    for char in caracteres_control:
        texto = texto.replace(char, '')
    return texto

def aplicar_correcciones_diccionario(s):
    """Aplica las correcciones del diccionario a un texto."""
    if not isinstance(s, str):
        return s
    
    # Primero eliminar caracteres de control
    texto_corregido = eliminar_caracteres_control(s)
    
    # Luego aplicar correcciones del diccionario (ordenar por longitud descendente para evitar reemplazos parciales)
    items_ordenados = sorted(correcciones_utf8_a_latin1_error.items(), key=lambda x: len(x[0]), reverse=True)
    for caracter_incorrecto, caracter_correcto in items_ordenados:
        texto_corregido = texto_corregido.replace(caracter_incorrecto, caracter_correcto)
    
    return texto_corregido

# ==============================================================================
# 3. Procesar archivo CSV
# ==============================================================================
input_path = Path("comentarios_limpio_utf8.csv")
output_path = Path("comentarios_limpio_utf8_definitivo.csv")

print(f"Leyendo archivo: {input_path}")
df = pd.read_csv(input_path, sep=";", encoding="utf-8")

# Aplicar correcciones solo a la columna de contenido
columna_texto = "CONTENIDO A ANALIZAR"
print(f"Aplicando correcciones del diccionario a la columna '{columna_texto}'...")
if columna_texto in df.columns:
    df[columna_texto] = df[columna_texto].apply(aplicar_correcciones_diccionario)
    print(f"Correcciones aplicadas a {len(df)} filas")
else:
    print(f"Error: La columna '{columna_texto}' no existe en el archivo")
    print(f"Columnas disponibles: {list(df.columns)}")

# Guardar archivo corregido
df.to_csv(output_path, sep=";", index=False, encoding="utf-8")
print(f"Archivo corregido guardado como: {output_path}")
