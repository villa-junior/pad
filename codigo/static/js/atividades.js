document.addEventListener('DOMContentLoaded', function() {
    const atividadeRows = document.querySelectorAll('.atividade-row');
    
    atividadeRows.forEach(row => {
        row.addEventListener('click', function() {
            
            const detalhesRow = this.nextElementSibling;
            
            
            document.querySelectorAll('.detalhes-row').forEach(dRow => {
                if (dRow !== detalhesRow) {
                    dRow.classList.remove('active');
                }
            });
            
            
            detalhesRow.classList.toggle('active');
        });
    });
});