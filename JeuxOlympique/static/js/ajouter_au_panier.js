// document.addEventListener('DOMContentLoaded', function() {
//     var formulaireChoisirTicket = document.getElementById('choisir-ticket-form');

//     formulaireChoisirTicket.addEventListener('submit', function(event) {
//         event.preventDefault();

//         // Récupérer les données du formulaire
//         var competitionId = formulaireChoisirTicket.competitions.value;
//         var offreId = formulaireChoisirTicket.querySelector('.offre-checkbox:checked').value;

//         // Requête AJAX pour ajouter l'offre au panier
//         fetch('/ajouter_au_panier/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',  // Modifier le type de contenu selon vos besoins
//                 'X-CSRFToken': getCookie('csrftoken')
//             },
//             body: JSON.stringify({
//                 competition_id: competitionId,
//                 offre_id: offreId
//             })
//         })
//         .then(response => {
//             if (response.ok) {
//                 alert('L\'offre a été ajoutée au panier avec succès!');
//             } else {
//                 console.error('Erreur lors de la requête AJAX:', response.statusText);
//             }
//         })
//         .catch(error => {
//             console.error('Erreur lors de la requête AJAX:', error);
//         });
//     });

//     // Fonction pour obtenir le jeton CSRF
//     function getCookie(name) {
//         var cookieValue = null;
//         if (document.cookie && document.cookie !== '') {
//             var cookies = document.cookie.split(';');
//             for (var i = 0; i < cookies.length; i++) {
//                 var cookie = cookies[i].trim();
//                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                     break;
//                 }
//             }
//         }
//         return cookieValue;
//     }
// });
// document.addEventListener('DOMContentLoaded', function() {
//     var voirOffresBtn = document.getElementById('voir-offres-btn');
//     var offresContainer = document.getElementById('offres-container');

//     voirOffresBtn.addEventListener('click', function(event) {
//         offresContainer.style.display = 'block';
//     });
// });
