document.addEventListener('DOMContentLoaded', function () {
    const atividadeRows = document.querySelectorAll('.atividade-row');
    const detalhesRows = document.querySelectorAll('.detalhes-row');
    const filtroTurma = document.getElementById('filtroTurma');
    const botoesExcluir = document.querySelectorAll('.btn-excluir');

    // Alternar visibilidade dos detalhes
    atividadeRows.forEach(row => {
        row.addEventListener('click', function () {
            const detalhesRow = this.nextElementSibling;

            detalhesRows.forEach(dRow => {
                if (dRow !== detalhesRow) {
                    dRow.classList.remove('active');
                }
            });

            detalhesRow.classList.toggle('active');
        });
    });

    // Filtro por turma
    if (filtroTurma) {
        filtroTurma.addEventListener('change', () => {
            const turmaSelecionada = filtroTurma.value;

            atividadeRows.forEach(row => {
                const detalhesRow = row.nextElementSibling;
                const turmaTexto = row.querySelector('.turma').innerText;
                const turma = turmaTexto.replace('Turma:', '').trim();

                if (turmaSelecionada === 'todas' || turma === turmaSelecionada) {
                    row.style.display = '';
                    detalhesRow.style.display = '';
                } else {
                    row.style.display = 'none';
                    detalhesRow.style.display = 'none';
                }
            });
        });
    }



    atividadeRows.forEach((row, i) => {
        const btnExcluir = botoesExcluir[i];
        if (!btnExcluir) return;

        btnExcluir.style.display = 'none';

        row.addEventListener('click', (e) => {
            e.stopPropagation();

            botoesExcluir.forEach(b => b.style.display = 'none');

            if (btnExcluir.style.display === 'none' || btnExcluir.style.display === '') {
                btnExcluir.style.display = 'inline-block';
            } else {
                btnExcluir.style.display = 'none';
            }
        });

        btnExcluir.addEventListener('click', (e) => {
            e.stopPropagation(); // para não acionar o toggle do row
            const atividadeId = btnExcluir.getAttribute('data-id');
            const confirmar = confirm('Tem certeza que deseja excluir esta atividade?');
            if (confirmar) {
                fetch(`/atividades/${atividadeId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error || 'Erro ao excluir.');
        }
    })
    .catch(() => alert('Erro na requisição.'));
            }
        });
    });

    // Clicar fora esconde todos os botões excluir
    document.body.addEventListener('click', () => {
        botoesExcluir.forEach(b => b.style.display = 'none');
    });
});
