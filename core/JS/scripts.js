


       // olha ai pra nao dar erro no convite


function exibirMensagem(texto) {
    const mensagemDiv = document.getElementById('mensagem');
    mensagemDiv.textContent = texto;
    mensagemDiv.style.display = 'block';

    setTimeout(() => {
        mensagemDiv.style.display = 'none';
    }, 3000);
}

function aceitarConvite(conviteId) {
    const conviteElemento = document.getElementById(`convite-${conviteId}`);
    conviteElemento.remove();
    exibirMensagem('Convite aceito');
}

function recusarConvite(conviteId) {
    const conviteElemento = document.getElementById(`convite-${conviteId}`);
    conviteElemento.remove();
    exibirMensagem('Convite recusado');
}
