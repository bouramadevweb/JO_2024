document.addEventListener('DOMContentLoaded', function () {
        // Capturer le changement de sélection de la compétition
        document.getElementById('competition').addEventListener('change', function () {
            document.getElementById('choix-competition-form').submit();
        });

        // Mettre à jour le montant total lorsqu'une quantité change
        var quantiteInputs = document.querySelectorAll('.quantite-input');
        quantiteInputs.forEach(function (input) {
            input.addEventListener('change', function () {
                var quantite = parseInt(this.value);
                var prix = parseFloat(this.parentNode.querySelector('[name^=montant_total]').value);
                var montantTotalInput = this.parentNode.querySelector('[name^=montant_total]');
                var montantTotal = quantite * prix;
                montantTotalInput.value = montantTotal.toFixed(2); 
            });
        });

        // événement au clic sur le bouton "Ajouter au panier"
        document.getElementById('ajouter-panier-btn').addEventListener('click', function () {
            var form = document.getElementById('ajout-au-panier-form');
            var formData = new FormData(form);

            var xhr = new XMLHttpRequest();
            xhr.open(form.method, form.action, true);
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    window.location.reload();
                }
            };
            xhr.send(formData);
        });
    });