from flask import Flask, redirect, render_template, request

app = Flask(__name__)

produtos = []


@app.route("/")
def inicio():
  valor_total = sum(
      produto["quantidade"] * produto["preco"] for produto in produtos
  )
  return render_template(
      "index.html", produtos=produtos, valor_total=valor_total
  )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
  nome = request.form.get("nome")
  quantidade_str = request.form.get("quantidade")
  preco_str = request.form.get("preco")

  if not nome or not quantidade_str or not preco_str:
    return redirect("/")

  try:
    quantidade = int(quantidade_str)
    preco = float(preco_str.replace(",", "."))
  except ValueError:
    return redirect("/")

  produto = {"nome": nome, "quantidade": quantidade, "preco": preco}
  produtos.append(produto)

  return redirect("/")


@app.route("/atualizar/<int:indice>", methods=["POST"])
def atualizar(indice):
  if 0 <= indice < len(produtos):
    try:
      nova_quantidade = int(request.form.get("quantidade", 0))
      produtos[indice]["quantidade"] = nova_quantidade
    except ValueError:
      pass

  return redirect("/")


@app.route("/excluir/<int:indice>")
def excluir(indice):
  if 0 <= indice < len(produtos):
    produtos.pop(indice)

  return redirect("/")


if __name__ == "__main__":
  app.run(debug=True)
