/**
 * Initialize the login page when DOM is fully loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessageElement = document.getElementById('error-message') || createErrorElement();

    // Check if we're already logged in
    if (getCookie('token')) {
        // Already logged in, redirect to main page
        window.location.href = 'index.html';
        return;
    }

    // Set up login form event listener if the form exists
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form inputs
            const emailInput = document.getElementById('email');
            const passwordInput = document.getElementById('password');
            
            // Validate inputs
            if (!emailInput.value.trim() || !passwordInput.value.trim()) {
                displayErrorMessage('Please enter both email and password');
                return;
            }
            
            // Show loading state
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';
            
            try {
                // Attempt to login
                await loginUser(emailInput.value.trim(), passwordInput.value.trim());
            } catch (error) {
                // Handle login error
                displayErrorMessage(error.message || 'Login failed. Please try again.');
                
                // Reset button state
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            }
        });
    }
    
    /**
     * Creates an error message element if it doesn't exist
     * @return {HTMLElement} The error message element
     */
    function createErrorElement() {
        const errorElement = document.createElement('div');
        errorElement.id = 'error-message';
        errorElement.className = 'error-message';
        errorElement.style.color = 'red';
        errorElement.style.marginBottom = '15px';
        errorElement.style.display = 'none';
        
        // Insert before the form
        loginForm.parentNode.insertBefore(errorElement, loginForm);
        
        return errorElement;
    }
    
    /**
     * Displays an error message to the user
     * @param {string} message - The error message to display
     */
    function displayErrorMessage(message) {
        const errorElement = document.getElementById('error-message');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            
            // Automatically hide the message after 5 seconds
            setTimeout(() => {
                errorElement.style.display = 'none';
            }, 5000);
        }
    }
});

/**
 * Attempts to log in a user by sending credentials to the API
 * @param {string} email - User's email
 * @param {string} password - User's password
 * @return {Promise} Promise that resolves on successful login
 */
async function loginUser(email, password) {
    try {
        // Connect to the auth/login endpoint
        const response = await fetch('http://localhost:5050/hbnb/app/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        // Process the response
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || errorData.message || `Login failed: ${response.statusText}`);
        }
        
        // Extract and store the token
        const data = await response.json();
        
        // Your API returns an access_token
        if (!data.access_token) {
            throw new Error('Invalid server response: No token provided');
        }
        
        // Store the token
        const token = data.access_token;
        
        // Set cookie with a 7-day expiration
        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + 7);
        document.cookie = `token=${token}; path=/; expires=${expirationDate.toUTCString()}; SameSite=Strict`;
        
        // Redirect to the main page
        window.location.href = 'index.html';
        
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

/**
 * Gets a cookie value by its name
 * @param {string} name - The name of the cookie to retrieve
 * @return {string|null} The cookie value or null if not found
 */
function getCookie(name) {
    const cookieString = document.cookie;
    const cookies = cookieString.split('; ');
    
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName === name) {
            return decodeURIComponent(cookieValue);
        }
    }
    
    return null;
}

// Function to get a cookie value by its name
function getCookie(name) {
    const cookieString = document.cookie;
    const cookies = cookieString.split('; ');
    
    for (const cookie of cookies) {
      const [cookieName, cookieValue] = cookie.split('=');
      if (cookieName === name) {
        return cookieValue;
      }
    }
    
    return null;
  }
  
  // Check user authentication
  function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
  
    if (!token) {
      loginLink.style.display = 'block';
      // Even if not authenticated, still fetch places
      fetchPlaces(null);
    } else {
      loginLink.style.display = 'none';
      // Fetch places data with the authentication token
      fetchPlaces(token);
    }
  }
  
  // Fetch places data from the API
  async function fetchPlaces(token) {
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add authorization header if token exists
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch('http://localhost:5050/hbnb/app/api/v1/places', {
        method: 'GET',
        headers: headers
      });
      
      if (!response.ok) {
        throw new Error(`Error fetching places: ${response.statusText}`);
      }
      
      const places = await response.json();
      // Store the places data globally so we can filter it
      window.placesData = places;
      displayPlaces(places);
      
      // Initialize price filter
      setupPriceFilter();
    } catch (error) {
      console.error('Failed to fetch places:', error);
      document.getElementById('places-list').innerHTML = 
        '<div class="error-message">Failed to load places. Please try again later.</div>';
    }
  }
  
  // Display places in the DOM
  function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    // Clear current content
    placesList.innerHTML = '';
    
    if (places.length === 0) {
      placesList.innerHTML = '<div class="no-places">No places found matching your criteria.</div>';
      return;
    }
    
    // Create and append place cards
    places.forEach(place => {
      const placeCard = document.createElement('div');
      placeCard.className = 'place-card';
      placeCard.dataset.price = place.price; // Store price for filtering
      
      placeCard.innerHTML = `
        <h3>${place.name}</h3>
        <p class="location"><i class="fa fa-map-marker"></i> ${place.location}</p>
        <p class="description">${place.description}</p>
        <div class="price-tag">$${place.price}</div>
      `;
      
      placesList.appendChild(placeCard);
    });
  }
  
  // Setup price filter functionality
  function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    
    // Clear existing options
    priceFilter.innerHTML = '';
    
    // Add price filter options
    const options = [
      { value: '10', text: '$0 - $10' },
      { value: '50', text: '$0 - $50' },
      { value: '100', text: '$0 - $100' },
      { value: 'All', text: 'All Prices' }
    ];
    
    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option.value;
      optionElement.textContent = option.text;
      priceFilter.appendChild(optionElement);
    });
    
    // Add event listener for price filter changes
    priceFilter.addEventListener('change', filterPlacesByPrice);
  }
  
  // Filter places based on selected price
  function filterPlacesByPrice(event) {
    const selectedPrice = event.target.value;
    const places = window.placesData || [];
    
    let filteredPlaces;
    
    if (selectedPrice === 'All') {
      filteredPlaces = places;
    } else {
      const maxPrice = parseInt(selectedPrice, 10);
      filteredPlaces = places.filter(place => place.price <= maxPrice);
    }
    
    displayPlaces(filteredPlaces);
  }
  
  // Initialize the page
  document.addEventListener('DOMContentLoaded', () => {
    // Check authentication status when page loads
    checkAuthentication();
  });
