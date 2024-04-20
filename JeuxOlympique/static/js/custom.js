 $(document).ready(function () {
        // Gérer l'envoi du formulaire d'ajout
        $('#add-user-submit').click(function () {
            // Récupérer les données du formulaire
            var username = $('#add-username').val();
            var email = $('#add-email').val();

            // Envoyer les données via AJAX
            $.ajax({
                url: '/add_user/', // Modifier l'URL en fonction de votre configuration
                type: 'POST',
                data: {
                    'username': username,
                    'email': email,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // Inclure le jeton CSRF
                },
                success: function (data) {
                    // Réussite : actualiser la page pour afficher le nouvel utilisateur
                    location.reload();
                },
                error: function () {
                    // Erreur : afficher un message d'erreur
                    alert('Failed to add user.');
                }
            });
        });
    });