from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Funções do algoritmo de alinhamento (mesmo código fornecido anteriormente)
def inicializar_matriz(n, m, gap):
    matriz = [[0 for _ in range(m+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        matriz[i][0] = i * gap
    for j in range(1, m+1):
        matriz[0][j] = j * gap
    return matriz

def calcular_pontuacao(seq1, seq2, match=1, mismatch=-1, gap=-1):
    n = len(seq1)
    m = len(seq2)
    matriz = inicializar_matriz(n, m, gap)
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            if seq1[i-1] == seq2[j-1]:
                score_diagonal = matriz[i-1][j-1] + match
            else:
                score_diagonal = matriz[i-1][j-1] + mismatch
            score_up = matriz[i-1][j] + gap
            score_left = matriz[i][j-1] + gap
            matriz[i][j] = max(score_diagonal, score_up, score_left)
    
    return matriz

def reconstruir_alinhamento(matriz, seq1, seq2, gap=-1, gap_char="-"):
    alinhamento1 = ""
    alinhamento2 = ""
    i, j = len(seq1), len(seq2)
    
    while i > 0 or j > 0:
        current_score = matriz[i][j]
        if i > 0 and j > 0 and (current_score == matriz[i-1][j-1] + (1 if seq1[i-1] == seq2[j-1] else -1)):
            alinhamento1 = seq1[i-1] + alinhamento1
            alinhamento2 = seq2[j-1] + alinhamento2
            i -= 1
            j -= 1
        elif i > 0 and (current_score == matriz[i-1][j] + gap):
            alinhamento1 = seq1[i-1] + alinhamento1
            alinhamento2 = gap_char + alinhamento2
            i -= 1
        else:
            alinhamento1 = gap_char + alinhamento1
            alinhamento2 = seq2[j-1] + alinhamento2
            j -= 1
    
    return alinhamento1, alinhamento2

def limpar_sequencia(seq):
    return "".join(c for c in seq if c.upper() in "ATCG")

# Rota principal
@app.route("/")
def index():
    return render_template("index.html")

# Rota para processar o alinhamento
@app.route("/alinhar", methods=["POST"])
def alinhar():
    data = request.json
    seq1 = limpar_sequencia(data["seq1"])
    seq2 = limpar_sequencia(data["seq2"])
    
    if not seq1 or not seq2:
        return jsonify({"error": "Sequências inválidas ou vazias."}), 400
    
    matriz = calcular_pontuacao(seq1, seq2)
    alinhamento1, alinhamento2 = reconstruir_alinhamento(matriz, seq1, seq2)
    
    return jsonify({
        "alinhamento1": alinhamento1,
        "alinhamento2": alinhamento2
    })

if __name__ == "__main__":
    app.run(debug=True)