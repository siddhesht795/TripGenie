document.addEventListener('DOMContentLoaded', () => {
    try {
        const itineraryData = JSON.parse(localStorage.getItem('itineraryData'));
        const tripData = JSON.parse(localStorage.getItem('tripData'));

        if (!itineraryData || !tripData) {
            window.location.href = './index.html';
            return;
        }

        // Update user info and trip route
        const userName = document.getElementById('userName');
        const currentUser = localStorage.getItem('currentUser');
        if (currentUser) {
            const userData = JSON.parse(localStorage.getItem(currentUser));
            userName.textContent = `${userData.firstname} ${userData.lastname}`;
        }

        document.getElementById('tripRoute').textContent =
            `${tripData.source} ✈️ ${tripData.destination}`;

        // Render sections
        renderFlights(itineraryData.flights);
        renderHotels(itineraryData.hotels);
        renderWeather(itineraryData.weather);
        renderActivities(itineraryData.activities);

    } catch (error) {
        console.error('Error loading itinerary:', error);
        window.location.href = './index.html';
    }
});

function renderFlights(flights) {
    const container = document.querySelector('.flights-container');
    if (!container || !flights?.length) return;

    container.innerHTML = flights.map(flight => `
        <div class="flight-detail">
            <p><strong>Airline:</strong> ${flight.airline}</p>
            <p><strong>From:</strong> ${flight.departure} (${flight.departureTime})</p>
            <p><strong>To:</strong> ${flight.arrival} (${flight.arrivalTime})</p>
            <p><strong>Duration:</strong> ${flight.duration}</p>
            <p><strong>Price:</strong> $${flight.price}</p>
        </div>
    `).join('');
}

// Add similar render functions for hotels, weather, and activities...

function renderHotels(hotels) {
    const container = document.querySelector('.hotels-container');
    if (!container || !hotels?.length) return;

    container.innerHTML = hotels.map(hotel => `
        <div class="hotel-detail">
            <p><strong>Name:</strong> ${hotel.name}</p>
            <p><strong>Address:</strong> ${hotel.address}</p>
            <p><strong>Price:</strong> $${hotel.price}</p>
        </div>
    `).join('');
}

function renderWeather(weather) {
    const container = document.querySelector('.weather-container');
    if (!container || !weather) return;

    container.innerHTML = `<p>${weather}</p>`;
}

function renderActivities(activities) {
    const container = document.querySelector('.activities-container');
    if (!container || !activities?.length) return;

    container.innerHTML = activities.map(activity => `
        <div class="activity-detail">
            <p><strong>Day:</strong> ${activity.day}</p>
            <p><strong>Activities:</strong> ${activity.activities.map(act => act.name).join(', ')}</p>
        </div>
    `).join('');
}

// Add accordion functionality
function toggleAccordion(header) {
    const content = header.nextElementSibling;
    const isActive = header.classList.contains('active');

    // Close all accordions
    document.querySelectorAll('.accordion-header').forEach(h => {
        h.classList.remove('active');
        h.nextElementSibling.style.display = 'none';
    });

    // Open clicked accordion if it wasn't active
    if (!isActive) {
        header.classList.add('active');
        content.style.display = 'block';
    }
}

// Add click handlers to all accordion headers
document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => toggleAccordion(header));
});

// Open first accordion by default
const firstAccordion = document.querySelector('.accordion-header');
if (firstAccordion) {
    toggleAccordion(firstAccordion);
}
