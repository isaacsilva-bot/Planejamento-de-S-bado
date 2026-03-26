<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Roteiro de Entregas</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background: linear-gradient(180deg, #ff6a00, #ff8c42);
    }

    header {
      background: #ff6a00;
      color: white;
      padding: 18px;
      text-align: center;
      font-size: 20px;
      font-weight: bold;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
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
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }

    .card {
      background: white;
      padding: 15px;
      margin-bottom: 15px;
      border-radius: 14px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      animation: fadeIn 0.3s ease;
    }

    .card h3 {
      margin: 0 0 10px 0;
      color: #ff6a00;
    }

    .info {
      font-size: 14px;
      margin-bottom: 5px;
      color: #444;
    }

    .btn-maps {
      display: inline-block;
      margin-top: 10px;
      padding: 10px;
      background: #ff6a00;
      color: white;
      text-decoration: none;
      border-radius: 10px;
      font-size: 14px;
      width: 100%;
      text-align: center;
      font-weight: bold;
    }

    .btn-rota {
      display:block;
      background:white;
      color:#ff6a00;
      padding:15px;
      border-radius:12px;
      text-align:center;
      margin-bottom:15px;
      font-weight:bold;
      text-decoration:none;
      box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }

    .vazio {
      text-align: center;
      color: white;
      margin-top: 30px;
      font-weight: bold;
    }

    @keyframes fadeIn {
      from {opacity:0; transform: translateY(10px);}
      to {opacity:1; transform: translateY(0);}
    }
  </style>
</head>
<body>

<header>
  🚚 Roteiro de Entregas
</header>

<div class="container">

  <input type="text" id="idMotorista" placeholder="Digite seu ID...">

  <div id="resultado"></div>

</div>

<script>
const url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTLptCJKIUDiCVR440Z6ZaJxzvRB1WJeCV36OJfnTQ2nBLECWjlZOqslbedcybCY-4cUQSDmNOCEx0U/pub?output=csv&gid=465492226";

let dados = [];

async function carregarDados() {
  const res = await fetch(url);
  const texto = await res.text();

  const linhas = texto.split("\n").map(l => l.split(","));
  const headers = linhas[0];

  dados = linhas.slice(1).map(linha => {
    let obj = {};
    headers.forEach((h, i) => obj[h.trim()] = linha[i]);
    return obj;
  });
}

function montarRota(resultados) {
  if (resultados.length === 0) return "";

  const enderecos = resultados.map(r => 
    `${r["ENDEREÇO"]} ${r["NUMERO"]}, ${r["BAIRRO"]}, ${r["CEP"]}`
  );

  const origem = encodeURIComponent(enderecos[0]);
  const destino = encodeURIComponent(enderecos[enderecos.length - 1]);

  const waypoints = enderecos.slice(1, -1)
    .map(e => encodeURIComponent(e))
    .join("|");

  return `https://www.google.com/maps/dir/?api=1&origin=${origem}&destination=${destino}&waypoints=${waypoints}&travelmode=driving`;
}

function buscar() {
  const id = document.getElementById("idMotorista").value.trim();
  const div = document.getElementById("resultado");

  if (!id) {
    div.innerHTML = "<p class='vazio'>Digite seu ID para ver o roteiro</p>";
    return;
  }

  const resultados = dados.filter(d => d["ID do motorista"] === id);

  div.innerHTML = "";

  if (resultados.length === 0) {
    div.innerHTML = "<p class='vazio'>Nenhum roteiro encontrado</p>";
    return;
  }

  // BOTÃO ROTA COMPLETA
  const rotaLink = montarRota(resultados);

  div.innerHTML += `
    <a href="${rotaLink}" target="_blank" class="btn-rota">
      🚀 Iniciar navegação (rota completa)
    </a>
  `;

  resultados.forEach(r => {
    const enderecoCompleto = `${r["ENDEREÇO"]} ${r["NUMERO"]}, ${r["BAIRRO"]}, ${r["CEP"]}`;
    const linkMaps = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(enderecoCompleto)}`;

    div.innerHTML += `
      <div class="card">
        <h3>${r["Nome da Loja"]}</h3>

        <div class="info"><b>Rota:</b> ${r["Código da sua Rota"]}</div>
        <div class="info"><b>Endereço:</b> ${r["ENDEREÇO"]}, ${r["NUMERO"]}</div>
        <div class="info"><b>Bairro:</b> ${r["BAIRRO"]}</div>
        <div class="info"><b>CEP:</b> ${r["CEP"]}</div>
        <div class="info"><b>Complemento:</b> ${r["COMPLEMENTO"]}</div>

        <a class="btn-maps" href="${linkMaps}" target="_blank">
          📍 Abrir no Google Maps
        </a>
      </div>
    `;
  });
}

// busca automática
document.getElementById("idMotorista").addEventListener("input", buscar);

// carregar dados ao abrir
carregarDados();
</script>

</body>
</html>
