import re

tokens = []
index = 0

def tokenize(expression):
    token_spec = [
        ("NUMBER", r'\d+'),         # Números
        ("IDENTIFIER", r'[a-zA-Z][a-zA-Z0-9_]*'), # Identificadores
        ("ASSIGN", r'='),           # Operador de asignación
        ("PLUS", r'\+'),            # Suma
        ("TIMES", r'\*'),           # Multiplicación
        ("DIVIDE", r'/'),           # División
        ("LPAREN", r'\('),          # Paréntesis izquierdo
        ("RPAREN", r'\)'),          # Paréntesis derecho
        ("SEMICOLON", r';'),        # Punto y coma
        ("SKIP", r'[ \t\n]+'),      # Espacios y saltos de línea (ignorar)
        ("MISMATCH", r'.')          # Cualquier otro carácter no válido
    ]
    
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_spec)
    
    for match in re.finditer(token_regex, expression):
        kind = match.lastgroup
        value = match.group()
        if kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"Token inesperado: {value}")
        tokens.append((kind, value))

def match(expected_type):
    global index
    if index < len(tokens) and tokens[index][0] == expected_type:
        index += 1
        return True
    return False

def factor():
    if match("NUMBER") or match("IDENTIFIER"):
        return True
    elif match("LPAREN"):
        if expression():
            return match("RPAREN")
    return False

def term():
    if factor():
        while match("TIMES") or match("DIVIDE"):
            if not factor():
                return False
        return True
    return False

def expression():
    if term():
        while match("PLUS"):
            if not term():
                return False
        return True
    return False

def assignment():
    if match("IDENTIFIER") and match("ASSIGN") and expression() and match("SEMICOLON"):
        return True
    return False

def parse(code):
    global tokens, index
    tokens = []
    index = 0
    tokenize(code)
    return assignment() and index == len(tokens)

# Pruebas
examples = ["x = 5;", "y = x + 3;", "z = (y * 2) / 4;", "y = z + y;"]
for example in examples:
    print(f"{example} -> {'Válido' if parse(example) else 'Inválido'}")
