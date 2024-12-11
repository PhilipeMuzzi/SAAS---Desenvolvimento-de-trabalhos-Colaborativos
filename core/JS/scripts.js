


       // olha ai pra nao dar erro no convite


        function aceitarConvite(id) {
            fetch(`/aceitar-convite/${id}/`, { method: 'POST', headers: { 'X-CSRFToken': '{{ csrf_token }}' } })
                .then(response => response.json())
                .then(data => alert(data.mensagem))
                .then(() => location.reload());
        }
        function recusarConvite(id) {
            fetch(`/recusar-convite/${id}/`, { method: 'POST', headers: { 'X-CSRFToken': '{{ csrf_token }}' } })
                .then(response => response.json())
                .then(data => alert(data.mensagem))
                .then(() => location.reload());
        }
