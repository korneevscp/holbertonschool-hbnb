async function fetchPlaces(token) {
  try {
    // Vérifier si le token est fourni
    if (!token) {
      throw new Error('Token d\'authentification requis');
    }
    
    // Configuration de la requête avec l'en-tête d'autorisation
    const requestOptions = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    };
    
    // URL de l'API (à remplacer par votre URL réelle)
    const apiUrl = 'https://api.example.com/places';
    
    // Envoi de la requête
    const response = await fetch(apiUrl, requestOptions);
    
    // Vérification de la réponse
    if (!response.ok) {
      // Gestion des erreurs HTTP
      if (response.status === 401) {
        throw new Error('Non autorisé: token invalide ou expiré');
      } else if (response.status === 404) {
        throw new Error('Ressource non trouvée');
      } else {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }
    }
    
    // Analyser la réponse JSON
    const placesData = await response.json();
    
    // Retourner les données des lieux
    return placesData;
  } catch (error) {
    console.error('Erreur lors de la récupération des lieux:', error);
    throw error; // Propager l'erreur pour la gestion en amont
  }
}

// Exemple d'utilisation:
/*
async function displayPlaces() {
  try {
    // Récupérer le token depuis le stockage ou l'état de l'application
    const token = localStorage.getItem('auth_token');
    
    // Appeler fetchPlaces avec le token
    const places = await fetchPlaces(token);
    
    // Traiter et afficher les données
    console.log('Lieux récupérés:', places);
    
    // Ici, vous pourriez ajouter le code pour afficher les lieux dans l'interface
    // ...
    
  } catch (error) {
    console.error('Erreur:', error.message);
    // Afficher un message d'erreur à l'utilisateur
  }
}
*/
