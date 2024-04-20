   window.addEventListener('load', function () {
            // Sélectionnez toutes les balises d'images sur la page
            var images = document.querySelectorAll('img');

            // Parcourez chaque image
            images.forEach(function (img) {
                // Vérifiez si l'attribut src contient une valeur
                if (img.src) {
                    // Préchargez l'image en créant un nouvel objet Image
                    var imageToLoad = new Image();
                    imageToLoad.src = img.src;
                    // Attendez que l'image soit chargée avant de l'afficher
                    imageToLoad.onload = function () {
                        img.classList.add('loaded'); 
                    };
                }
            });
        });