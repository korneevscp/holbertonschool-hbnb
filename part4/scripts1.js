// Fonction pour récupérer le cookie (token)
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Vérifie si l'utilisateur est connecté
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  
  if (!token) {
    loginLink.textContent = 'Connexion';
    loginLink.href = 'login.html';
    // Même sans token, on charge les lieux publics
    fetchPlaces();
  } else {
    loginLink.textContent = 'Déconnexion';
    loginLink.href = '#';
    loginLink.addEventListener('click', (e) => {
      e.preventDefault();
      // Suppression du cookie pour la déconnexion
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.reload();
    });
    
    fetchPlaces(token);
  }
}

// Fonction pour récupérer la liste des lieux avec Fetch API
async function fetchPlaces(token = null) {
  try {
    // Préparation des en-têtes
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };
    
    // Ajout du token si disponible
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Afficher un indicateur de chargement
    const placesContainer = document.getElementById('places-list');
    placesContainer.innerHTML = '<p class="loading">Chargement des lieux...</p>';
    
    // Envoi de la requête GET
    const response = await fetch('https://api.exemple.com/lieux', {
      method: 'GET',
      headers: headers
    });
    
    // Vérification si la requête a réussi
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    
    // Conversion de la réponse en JSON
    const places = await response.json();
    
    // Affichage des lieux récupérés
    displayPlaces(places);
    
  } catch (error) {
    console.error('Erreur lors de la récupération des lieux:', error);
    
    // Affichage d'un message d'erreur
    const placesContainer = document.getElementById('places-list');
    placesContainer.innerHTML = `
      <p class="error-message">
        Impossible de charger les lieux: ${error.message}
      </p>
    `;
    
    // En cas d'erreur, on peut afficher des données de test pour le développement
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.log('Mode développement - Chargement des données de test');
      const testPlaces = [
        { id: 1, name: "Cabane en bois", price: 45, location: "Forêt" },
        { id: 2, name: "Studio urbain", price: 80, location: "Paris" },
        { id: 3, name: "Appartement de luxe", price: 120, location: "Nice" },
        { id: 4, name: "Tente safari", price: 10, location: "Nature" }
      ];
      displayPlaces(testPlaces);
    }
  }
}

// Fonction pour afficher les lieux
function displayPlaces(places) {
  const placesContainer = document.getElementById('places-list');
  placesContainer.innerHTML = '';
  
  if (!places || places.length === 0) {
    placesContainer.innerHTML = '<p class="no-places">Aucun lieu disponible pour le moment.</p>';
    return;
  }
  
  // Création d'un élément pour chaque lieu
  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);
    
    card.innerHTML = `
      <h2>${place.name}</h2>
      <p>Prix : ${place.price}€/nuit</p>
      <p>Lieu : ${place.location}</p>
      <a href="place.html?id=${place.id}" class="details-button">Voir les détails</a>
    `;
    
    placesContainer.appendChild(card);
  });
}

// Filtrage par prix
function setupPriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  
  priceFilter.addEventListener('change', function() {
    const value = this.value;
    const cards = document.querySelectorAll('.place-card');
    
    let visibleCount = 0;
    
    cards.forEach(card => {
      const price = parseInt(card.getAttribute('data-price'));
      
      if (value === 'all' || price <= parseInt(value)) {
        card.style.display = 'block';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });
    
    // Si aucun lieu ne correspond au filtre
    const placesContainer = document.getElementById('places-list');
    const noResultsMessage = placesContainer.querySelector('.no-results');
    
    if (visibleCount === 0 && !noResultsMessage) {
      const message = document.createElement('p');
      message.className = 'no-results';
      message.textContent = 'Aucun lieu ne correspond à ce filtre.';
      placesContainer.appendChild(message);
    } else if (visibleCount > 0 && noResultsMessage) {
      noResultsMessage.remove();
    }
  });
}

// Initialisation
window.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  setupPriceFilter();
});
