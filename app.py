<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Roteiro de Entregas</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    body {
      font-family: Arial;
      margin: 0;
      background: linear-gradient(180deg, #ff6a00, #ff8c42);
    }

    header {
      background: #ff6a00;
      color: white;
      padding: 18px;
      text-align: center;
      font-weight: bold;
    }

    .container {
      padding: 15px;
    }

    input {
      width: 100%;
      padding: 14px;
      border-radius: 12px;
      border: none;
      margin-bottom: 15px;
      font-size: 16px;
    }

    .card {
      background: white;
      padding: 15px;
      margin-bottom: 15px;
      border-radius: 14px;
    }

    .btn {
      display:block;
      margin-top:10px;
      padding:12px;
      border-radius:10px;
      text-align:center;
      font-weight:bold;
      text-decoration:none;
    }

    .maps { background:#ff6a00; color:white; }
    .rota { background:white; color:#ff6a00; margin-bottom:15px; }

    .vazio {
      color:white;
      text-align:center;
    }
  </style>
</head>

<body>

<header>🚚 Roteiro de Entregas</header>

<div class="container">
  <input type="text" id="idMotorista" placeholder="Digite seu ID...">
  <div id="resultado"></div>
</div>

<script>
const url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTLptCJKIUDiCVR440Z6ZaJxzvRB1WJeCV36OJfnTQ2nBLECWjlZOqslbedcybCY-4cUQSDmNOCEx0U/pub?output=csv&gid=465492226";

let dados = [];

// função simples de CSV (não quebra fácil)
function parseCSV(texto) {
  const linhas = texto.split("\n");
  const headers = linhas[0].split(";"); // 👈 importante: usa ;

  return linhas.slice(1).map(linha => {
    const colunas = linha.split(";");
    let obj = {};
    headers.forEach((h, i) => obj[h.trim()] = colunas[i]);
    return obj;
  });
}

async function carregarDados() {
  try {
    const res = await fetch(url);
    const texto = await res.text();
    dados = parseCSV(texto);
  } catch (erro) {
    document.getElementById("resultado").innerHTML =
      "<p class='vazio'>Erro ao carregar dados</p>";
  }
}

function montarRota(lista) {
  const enderecos = lista.map(r =>
    `${r["ENDEREÇO"]} ${r["NUMERO"]}, ${r["BAIRRO"]}, ${r["CEP"]}`
  );

  const origem = encodeURIComponent(enderecos[0]);
  const destino = encodeURIComponent(enderecos[enderecos.length - 1]);

  const waypoints = enderecos.slice(1, -1)
    .map(e => encodeURIComponent(e))
    .join("|");

  return `https://www.google.com/maps/dir/?api=1&origin=${origem}&destination=${destino}&waypoints=${waypoints}`;
}

function buscar() {
  const id = document.getElementById("idMotorista").value.trim();
  const div = document.getElementById("resultado");

  if (!id) {
    div.innerHTML = "<p class='vazio'>Digite seu ID</p>";
    return;
  }

  const filtrado = dados.filter(d => d["ID do motorista"] === id);

  if (filtrado.length === 0) {
    div.innerHTML = "<p class='vazio'>Nenhum resultado</p>";
    return;
  }

  let html = "";

  const rota = montarRota(filtrado);
  html += `<a href="${rota}" target="_blank" class="btn rota">🚀 Iniciar rota completa</a>`;

  filtrado.forEach(r => {
    const endereco = `${r["ENDEREÇO"]} ${r["NUMERO"]}, ${r["BAIRRO"]}, ${r["CEP"]}`;
    const maps = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(endereco)}`;

    html += `
      <div class="card">
        <b>${r["Nome da Loja"]}</b><br>
        Rota: ${r["Código da sua Rota"]}<br>
        ${endereco}<br>
        <a class="btn maps" href="${maps}" target="_blank">📍 Abrir no Maps</a>
      </div>
    `;
  });

  div.innerHTML = html;
}

document.getElementById("idMotorista").addEventListener("input", buscar);

carregarDados();
</script>

</body>
</html>
