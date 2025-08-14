// Variáveis globais para elementos
const diasContainer = document.getElementById('dias');
const mesDisplay = document.getElementById('mes');
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');

const modal = document.getElementById('modal');
const modalConteudo = document.getElementById('modal-conteudo');
const modalFechar = document.getElementById('modal-fechar');

let dataAtualGlobal = new Date();

// Função para buscar eventos via API Flask para uma data específica
async function buscarEventosPorDia(dataStr) {
    try {
        const resposta = await fetch(`/calendario/eventos/${dataStr}`);
        if (resposta.ok) {
            return await resposta.json();
        } else {
            console.error('Erro ao buscar eventos:', resposta.statusText);
            return [];
        }
    } catch (erro) {
        console.error('Erro na requisição:', erro);
        return [];
    }
}

// Função que desenha o calendário e adiciona eventos
async function carregarCalendario(data) {
    const mesAtual = data.getMonth();
    const anoAtual = data.getFullYear();

    mesDisplay.innerText = data.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
    diasContainer.innerHTML = '';

    const primeiroDiaDoMes = new Date(anoAtual, mesAtual, 1);
    const primeiroDiaDaSemana = primeiroDiaDoMes.getDay();
    const diasDoMes = new Date(anoAtual, mesAtual + 1, 0).getDate();

    // Preenche espaços vazios antes do primeiro dia do mês
    for (let i = 0; i < primeiroDiaDaSemana; i++) {
        const divVazia = document.createElement('div');
        diasContainer.appendChild(divVazia);
    }

    for (let dia = 1; dia <= diasDoMes; dia++) {
        const diaDiv = document.createElement('div');
        diaDiv.innerText = dia;
        diaDiv.style.border = '1px solid #ccc';
        diaDiv.style.padding = '5px';
        diaDiv.style.cursor = 'pointer';
        diaDiv.style.minHeight = '50px';

        const chaveData = `${anoAtual}-${String(mesAtual + 1).padStart(2, '0')}-${String(dia).padStart(2, '0')}`;

        // Destaca o dia atual
        const hoje = new Date();
        if (dia === hoje.getDate() && mesAtual === hoje.getMonth() && anoAtual === hoje.getFullYear()) {
            diaDiv.style.backgroundColor = '#ffeb3b';
        }

        // Busca eventos do dia e adiciona tema resumido
        const eventos = await buscarEventosPorDia(chaveData);
        eventos.forEach(e => {
            e.programacao.forEach(p => {
                const eventoDiv = document.createElement('div');
                eventoDiv.innerText = p.tema;
                eventoDiv.classList.add('evento');
                eventoDiv.style.fontSize = '0.8em';
                eventoDiv.style.marginTop = '2px';
                eventoDiv.style.backgroundColor = '#d1e7dd';
                eventoDiv.style.borderRadius = '3px';
                eventoDiv.style.padding = '2px 4px';
                diaDiv.appendChild(eventoDiv);
            });
        });

        // Clique abre modal com programação detalhada
        diaDiv.addEventListener('click', () => {
            carregarProgramacaoDoDia(chaveData);
        });

        diasContainer.appendChild(diaDiv);
    }
}

// Função que carrega a programação detalhada no modal
async function carregarProgramacaoDoDia(dataStr) {
    modalConteudo.innerHTML = '<p>Carregando...</p>';
    modal.style.display = 'block';

    try {
        const resposta = await fetch(`/calendario/eventos/${dataStr}`);
        if (!resposta.ok) {
            modalConteudo.innerHTML = `<p>Erro ao carregar programação.</p>`;
            return;
        }
        const eventos = await resposta.json();

        if (eventos.length === 0) {
            modalConteudo.innerHTML = `<p>Não há programação para este dia.</p>`;
        } else {
            let html = '';
            eventos.forEach(evento => {
                html += `<h3>${evento.evento.titulo}</h3><p>${evento.evento.descricao}</p>`;
                evento.programacao.forEach(p => {
                    html += `<p><strong>${p.inicio} - ${p.fim}:</strong> ${p.tema} <br> Organizador: ${p.organizador} <br> ${p.descricao}</p>`;
                });
            });
            modalConteudo.innerHTML = html;
        }
    } catch (erro) {
        modalConteudo.innerHTML = `<p>Erro na requisição: ${erro}</p>`;
    }
}

// Fecha o modal ao clicar no "X"
modalFechar.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Fecha o modal ao clicar fora da caixa do conteúdo
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Inicializa calendário com o mês atual
carregarCalendario(dataAtualGlobal);

// Botões para navegar entre os meses
prevButton.addEventListener('click', () => {
    dataAtualGlobal.setMonth(dataAtualGlobal.getMonth() - 1);
    carregarCalendario(dataAtualGlobal);
});

nextButton.addEventListener('click', () => {
    dataAtualGlobal.setMonth(dataAtualGlobal.getMonth() + 1);
    carregarCalendario(dataAtualGlobal);
});
