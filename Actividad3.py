#Diccionario con las notas y acordes válidos para cada tonalidad

escalas = {
    'C mayor': {
        'notas': {'C', 'D', 'E', 'F', 'G', 'A', 'B'},
        'acordes': {'C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim'},
        'septimas': {'Cmaj7', 'Dm7', 'Em7', 'Fmaj7', 'G7', 'Am7', 'Bm7b5'}
    },

    'C menor': {
        'notas': {'C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'},
        'acordes': {'Cm', 'Ddim', 'Eb', 'Fm', 'Gm', 'Ab', 'Bb'},
        'septimas': {'Cm7', 'Dm7b5', 'Ebmaj7', 'Fm7', 'Gm7', 'Abmaj7', 'Bb7'}
    },

    'D mayor': {
        'notas': {'D', 'E', 'F#', 'G', 'A', 'B', 'C#'},
        'acordes': {'D', 'Em', 'F#m', 'G', 'A', 'Bm', 'C#dim'},
        'septimas': {'Dmaj7', 'Em7', 'F#m7', 'Gmaj7', 'A7', 'Bm7', 'C#m7b5'}
    },

    'D menor': {
        'notas': {'D', 'E', 'F', 'G', 'A', 'Bb', 'C'},
        'acordes': {'Dm', 'Edim', 'F', 'Gm', 'Am', 'Bb', 'C'},
        'septimas': {'Dm7', 'Em7b5', 'Fmaj7', 'Gm7', 'Am7', 'Bbmaj7', 'C7'}
    },

    'E mayor': {
        'notas': {'E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'},
        'acordes': {'E', 'F#m', 'G#m', 'A', 'B', 'C#m', 'D#dim'},
        'septimas': {'Emaj7', 'F#m7', 'G#m7', 'Amaj7', 'B7', 'C#m7', 'D#m7b5'}
    },

    'E menor': {
        'notas': {'E', 'F#', 'G', 'A', 'B', 'C', 'D'},
        'acordes': {'Em', 'F#dim', 'G', 'Am', 'Bm', 'C', 'D'},
        'septimas': {'Em7', 'F#m7b5', 'Gmaj7', 'Am7', 'Bm7', 'Cmaj7', 'D7'}
    },

    'F mayor': {
        'notas': {'F', 'G', 'A', 'Bb', 'C', 'D', 'E'},
        'acordes': {'F', 'Gm', 'Am', 'Bb', 'C', 'Dm', 'Edim'},
        'septimas': {'Fmaj7', 'Gm7', 'Am7', 'Bbmaj7', 'C7', 'Dm7', 'Em7b5'}
    },

    'F menor': {
        'notas': {'F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb'},
        'acordes': {'Fm', 'Gdim', 'Ab', 'Bbm', 'Cm', 'Db', 'Eb'},
        'septimas': {'Fm7', 'Gm7b5', 'Abmaj7', 'Bbm7', 'Cm7', 'Dbmaj7', 'Eb7'}
    },

    'G mayor': {
        'notas': {'G', 'A', 'B', 'C', 'D', 'E', 'F#'},
        'acordes': {'G', 'Am', 'Bm', 'C', 'D', 'Em', 'F#dim'},
        'septimas': {'Gmaj7', 'Am7', 'Bm7', 'Cmaj7', 'D7', 'Em7', 'F#m7b5'}
    },

    'G menor': {
        'notas': {'G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'},
        'acordes': {'Gm', 'Adim', 'Bb', 'Cm', 'Dm', 'Eb', 'F'},
        'septimas': {'Gm7', 'Am7b5', 'Bbmaj7', 'Cm7', 'Dm7', 'Ebmaj7', 'F7'}
    },

    'A mayor': {
        'notas': {'A', 'B', 'C#', 'D', 'E', 'F#', 'G#'},
        'acordes': {'A', 'Bm', 'C#m', 'D', 'E', 'F#m', 'G#dim'},
        'septimas': {'Cmaj7', 'Dm7', 'Em7', 'Fmaj7', 'G7', 'Am7', 'Bm7b5'}
    },

    'A menor': {
        'notas': {'A', 'B', 'C', 'D', 'E', 'F', 'G'},
        'acordes': {'Am', 'Bdim', 'C', 'Dm', 'Em', 'F', 'G'},
        'septimas': {'Am7', 'Bm7b5', 'Cmaj7', 'Dm7', 'Em7', 'Fmaj7', 'G7'}
    },

    'B mayor': {
        'notas': {'B', 'C#', 'D', 'E', 'F#', 'G', 'A'},
        'acordes': {'B', 'C#m', 'D#m', 'E', 'F#', 'G#m', 'A#dim'},
        'septimas': {'Bmaj7', 'C#m7', 'D#m7', 'Emaj7', 'F#7', 'G#m7', 'A#m7b5'}
    },

    'B menor': {
        'notas': {'B', 'C#', 'D', 'E', 'F#', 'G', 'A'},
        'acordes': {'Bm', 'C#dim', 'D', 'Em', 'F#m', 'G', 'A'},
        'septimas': {'Bm7', 'C#m7b5', 'Dmaj7', 'Em7', 'F#m7', 'Gmaj7', 'A7'}
    },
}

#Función para validar secuencias de notas y/o acordes
def validar_secuencia(tonalidad, secuencia):
    #Se recibe la tonalidad, es decir la nota y el tipo de nota, si no es valida, o sea, que esté dentro de las contempladas, retorna que no es valida
    datos = escalas.get(tonalidad)
    if not datos:
        return False, "Tonalidad no válida"
    
    #A las notas validas llega el arreglo de todas las notas (segunda ramificación del automata)
    notas_validas = datos['notas']
    #A los acordes validos llega el arreglo de todas los acordes (primera ramificación del automata)
    acordes_validos = datos['acordes'].union(datos['septimas'])
    
    #Se lee la cantidad de caracteres que tiene cada elemento para diferenciar la rama
    es_validacion_notas = all(len(elemento) == 1 for elemento in secuencia)
    
    #Si son puras notas entra aquí
    if es_validacion_notas:
        for nota in secuencia:
            if nota not in notas_validas:
                return False, "Nota no válida: " + nota
        return True, "Secuencia de notas válida"
    #De lo contrario entra acá
    else:
        for acorde in secuencia:
            if acorde not in acordes_validos:
                return False, "Acorde no válido: " + acorde
        return True, "Secuencia de acordes válida"
    
#Captura de la tonalidad
print("Ingrese la nota seguida de su tonalidad a la que pertenece su secuencia, ejemplo: C mayor")
tonalidad = input()

#Captura de la secuencia
secuencia = []
print("Ahora ingrese la secuencia que desea evaluar. Cuando ya no quiera ingresar más acordes o notas, ingrese '0'.")
#Se crea un bucle para pdoer capturas las secuencias que quiera
while True:
    elemento = input("Ingrese una nota o acorde (o '0' para terminar): ")
    if elemento == '0':
        break
    #Se añade cada elemento que el usuario pone a la lista de secuencia
    secuencia.append(elemento)

#Validación de la secuencia
resultado, mensaje = validar_secuencia(tonalidad, secuencia)
print(mensaje)