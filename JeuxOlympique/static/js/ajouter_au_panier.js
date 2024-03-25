function calculerTotal() {
    var total = 0;
    var offresSelectionnees = document.querySelectorAll('input[name="offre_id"]:checked');
    offresSelectionnees.forEach(function(offre) {
        var quantite = document.getElementById('quantite_' + offre.value).value;
        var prixUnitaire = offre.getAttribute('data-prix');
        total += parseFloat(quantite) * parseFloat(prixUnitaire);
    });
    document.getElementById('total').textContent = total.toFixed(2);
}

