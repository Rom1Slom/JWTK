document.addEventListener('DOMContentLoaded', (event) => {
   
    function afficherTraduction(phrase_id) {
        console.log("Fonction afficherTraduction appelée avec phrase ID:", phrase_id); // Message de débogage
        fetch(`/traduction/${phrase_id}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Données reçues :", data); // Vérifiez ce que contient data
                document.getElementById("traduction").innerText = data.traduction;
            })
            .catch(error => {
                console.error("Erreur lors de la récupération de la traduction:", error);
                alert(`Erreur: ${error.message}`);
            });
    }

    function phraseSuivante() {
        console.log("Fonction phraseSuivante appelée, numéro actuel:", currentPhraseNumber); // Message de débogage
        fetch(`/traduction/?current_phrase_number=${currentPhraseNumber}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                console.log("HTML reçu :", html); // Vérifiez le contenu HTML reçu
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newPhrase = doc.querySelector('#phrase');
                const newTraduction = doc.querySelector('#traduction');
                document.getElementById('phrase').innerText = newPhrase.innerText;
                document.getElementById('traduction').innerText = newTraduction.innerText;
                const newPhraseNumber = newPhrase.dataset.phraseNumber;
                console.log("New Phrase Number:", newPhraseNumber); // Vérifiez la valeur
                if (newPhraseNumber) {
                    currentPhraseNumber = newPhraseNumber;
                } else {
                    console.error("data-phrase-number is not defined");
                }
            })
            .catch(error => {
                console.error("Erreur lors de la récupération de la nouvelle phrase:", error);
                alert(`Erreur: ${error.message}`);
            });
    }

    function phrasePrecedente() {
        if (currentPhraseNumber > 1) {
            console.log("Fonction phrasePrecedente appelée, numéro actuel:", currentPhraseNumber); // Debug
            currentPhraseNumber -= 1;

            fetch(`/traduction/?current_phrase_number=${currentPhraseNumber}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(html => {
                    console.log("HTML reçu :", html);
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newPhrase = doc.querySelector('#phrase');
                    const newTraduction = doc.querySelector('#traduction');
                    document.getElementById('phrase').innerText = newPhrase.innerText;
                    document.getElementById('traduction').innerText = newTraduction.innerText;
                    const newPhraseNumber = newPhrase.dataset.phraseNumber;
                    if (newPhraseNumber) {
                        currentPhraseNumber = newPhraseNumber;
                    } else {
                        console.error("data-phrase-number is not defined");
                    }
                })
                .catch(error => {
                    console.error("Erreur lors de la récupération de la phrase précédente:", error);
                    alert(`Erreur: ${error.message}`);
                });
        } else {
            alert("Vous êtes déjà à la première phrase.");
        }
    }

    // Make functions globally accessible
    window.afficherTraduction = afficherTraduction;
    window.phraseSuivante = phraseSuivante;
    window.phrasePrecedente = phrasePrecedente;
});
