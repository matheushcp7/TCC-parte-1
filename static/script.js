const form = document.getElementById("mensagemForm");
const mensagemSucesso = document.getElementById("mensagemSucesso");
const lista = document.getElementById("listaMensagens");

// Função para adicionar uma mensagem na lista HTML
function adicionarMensagemNaLista(msg) {
  const li = document.createElement("li");
  li.innerHTML = `<strong>${msg.titulo}</strong>: ${msg.conteudo} ${
    msg.publicada ? "[Publicada]" : "[Não publicada]"
  }`;
  lista.appendChild(li);
}

// Evento de envio do formulário
form.addEventListener("submit", async (e) => {
  e.preventDefault(); // evita recarregar a página
  // Captura os dados do formulário
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  data.publicada = formData.has("publicada"); // checkbox
  // Envia para a API via POST
  const response = await fetch("/mensagens", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (response.ok) {
    // Apenas adiciona a nova mensagem na lista, sem limpar o restante
    adicionarMensagemNaLista(data);
    // Exibe mensagem de sucesso
    mensagemSucesso.textContent = `Mensagem '${data.titulo}' criada com sucesso!`;
    // Limpa o formulário
    form.reset();
  } else {
    mensagemSucesso.textContent = "Erro ao criar a mensagem!";
    mensagemSucesso.style.color = "red";
  }
});
