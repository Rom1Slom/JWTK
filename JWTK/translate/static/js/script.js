document.addEventListener('DOMContentLoaded', (event) => {
    let currentPhraseNumber = 1; // Assurez-vous que cette valeur est initialisée correctement
    
    function changerPhrase(direction) {
        console.log("Direction choisie:", direction);
        if (direction !== "next" && direction !== "previous") {
            console.error("Direction invalide", direction);
            return;
        }
        const newPhraseNumber = direction === "next" ? currentPhraseNumber -1  : currentPhraseNumber + 1;
        console.log("Numéro de la nouvelle phrase:", newPhraseNumber);  // Affiche la valeur de newPhraseNumber
    
        if (newPhraseNumber < 1) {
            alert("Vous êtes déjà à la première phrase.");
            return;
        }    

        console.log(`Changer de phrase : direction=${direction}, numéro=${newPhraseNumber}`);
        fetch(`/traduction/?current_phrase_number=${newPhraseNumber}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newPhrase = doc.querySelector('#phrase');
                const newTraduction = doc.querySelector('#traduction');

                if (newPhrase && newTraduction) {
                    document.getElementById('phrase').innerText = newPhrase.innerText;
                    document.getElementById('traduction').innerText = newTraduction.innerText;
                    currentPhraseNumber = parseInt(newPhrase.dataset.phraseNumber, 10) || newPhraseNumber;
                    console.log(`Numéro de notre nouvelle phrase : ${currentPhraseNumber}`);
                } else {
                    console.error("Erreur : éléments HTML manquants dans la réponse.");
                }
            })
            .catch(error => {
                console.error(`Erreur lors de la récupération de la phrase (${direction}):`, error);
                alert(`Erreur: ${error.message}`);
            });
    }

    function afficherTraduction(phrase_id) {
        if (!phrase_id) {
            phrase_id = currentPhraseNumber; // Utiliser la valeur actuelle si non spécifiée
        }

        console.log("Fonction afficherTraduction appelée avec phrase ID:", phrase_id);
        fetch(`/traduction/${phrase_id}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Données reçues :", data);
                document.getElementById("traduction").innerText = data.traduction;
            })
            .catch(error => {
                console.error("Erreur lors de la récupération de la traduction:", error);
                alert(`Erreur: ${error.message}`);
            });
    }



    function phraseSuivante() {
        changerPhrase("next");
    }

    function phrasePrecedente() {
        console.log("Appel de la fonction phrasePrecedente"); // Log pour confirmer l'appel
        changerPhrase("previous");
    }

    // Rendez les fonctions globalement accessibles
    window.afficherTraduction = afficherTraduction;
    window.phraseSuivante = phraseSuivante;
    window.phrasePrecedente = phrasePrecedente;
});

