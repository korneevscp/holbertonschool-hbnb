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
        const response = await fetch('/api/v1/auth/login', {
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