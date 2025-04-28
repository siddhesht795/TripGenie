// --------- Mobile Menu Toggle --------- //
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}

// --------- Account Dropdown Toggle --------- //
function toggleDropdown(event) {
    event.preventDefault();
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.classList.toggle('show');
}

// Close dropdown if clicked outside
window.onclick = function (event) {
    const dropdown = document.getElementById('dropdownMenu');
    if (!event.target.matches('.auth-btn')) {
        if (dropdown && dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
        }
    }
};

// --------- Sign Up / Sign In Functionality --------- //
// Store user (Sign Up)
function signupUser() {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    if (!email || !password) {
        alert('Please fill all fields');
        return;
    }
    localStorage.setItem(email, password);
    alert('Account created successfully!');
    window.location.href = 'signin.html'; // Redirect to Sign In
}

// Sign in user
function signinUser() {
    const email = document.getElementById('signin-email').value;
    const password = document.getElementById('signin-password').value;
    const storedPassword = localStorage.getItem(email);
    if (storedPassword && storedPassword === password) {
        alert('Sign in successful!');
        localStorage.setItem('currentUser', email); // Store session
        window.location.href = '../index.html'; // Redirect to Home
    } else {
        alert('Invalid email or password');
    }
}

// Attach signup/signin button listeners
document.addEventListener('DOMContentLoaded', () => {
    const signupBtn = document.getElementById('signup-btn');
    if (signupBtn) signupBtn.addEventListener('click', signupUser);

    const signinBtn = document.getElementById('signin-btn');
    if (signinBtn) signinBtn.addEventListener('click', signinUser);
});

// --------- Reveal Elements on Scroll --------- //
window.addEventListener('scroll', function () {
    const reveals = document.querySelectorAll('.reveal');
    for (let i = 0; i < reveals.length; i++) {
        const windowHeight = window.innerHeight;
        const elementTop = reveals[i].getBoundingClientRect().top;
        const elementVisible = 150;
        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add('active');
        }
    }
});

// --------- Handle "Get Suggestions" Button --------- //
document.getElementById("getSuggestions")?.addEventListener("click", async () => {
    const source = document.querySelector('.source-input').value;
    const destination = document.querySelector('.destination-input').value;
    const style = document.querySelector('select[name="travelStyle"]').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    if (!source || !destination || !style || !startDate || !endDate) {
        alert('Please fill in all fields to get suggestions!');
        return;
    }

    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
        alert('Please sign in to get AI suggestions!');
        window.location.href = 'auth/signin.html';
        return;
    }

    localStorage.setItem('tripData', JSON.stringify({ source, destination, style, startDate, endDate }));
    window.location.href = 'itinerary.html'; // Redirect to itinerary page
});

// --------- Itinerary Page Logic --------- //
if (
    window.location.pathname.endsWith('itinerary.html') ||
    window.location.pathname.endsWith('/itinerary.html')
) {
    document.addEventListener('DOMContentLoaded', async function () {

        async function fetchItineraryDataIfNeeded() {
            if (localStorage.getItem('itineraryData')) return;

            const tripData = JSON.parse(localStorage.getItem('tripData'));
            if (!tripData) return;

            const payload = {
                source: tripData.source,
                destination: tripData.destination,
                days: Math.ceil(
                    (new Date(tripData.endDate) - new Date(tripData.startDate)) /
                    (1000 * 60 * 60 * 24)
                ),
                adults: 1,
                children: 0,
                childAges: [],
                startDate: tripData.startDate,
                endDate: tripData.endDate
            };

            try {
                const response = await fetch('http://localhost:5000/api/trip', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('itineraryData', JSON.stringify(data));
                    if (data.pdf_filename) {
                        localStorage.setItem('pdf_filename', data.pdf_filename);
                    }
                }
            } catch (e) {
                console.error('Failed to fetch itinerary from backend:', e);
            }
        }

        await fetchItineraryDataIfNeeded();

        const itineraryData = JSON.parse(localStorage.getItem('itineraryData'));
        if (!itineraryData) {
            window.location.href = 'index.html';
            return;
        }

        // Display Flights
        const flightsContainer = document.querySelector('.flights-container');
        if (flightsContainer) {
            if (itineraryData.flights?.length > 0) {
                flightsContainer.innerHTML = itineraryData.flights.map(flight => `
                    <div class="flight-card">
                        <div class="flight-header">
                            ${flight.airline ? `<span class="airline">${flight.airline}</span>` : ''}
                            ${flight.price ? `<span class="price">$${flight.price}</span>` : ''}
                        </div>
                        <div class="flight-timeline">
                            <div class="departure">
                                ${flight.departureTime ? `<time>${flight.departureTime}</time>` : ''}
                                ${flight.departure ? `<p>${flight.departure}</p>` : ''}
                            </div>
                            <div class="flight-path">
                                ${flight.duration ? `<div class="duration">${flight.duration}</div>` : ''}
                                ${flight.layovers?.length ? `
                                    <div class="layovers">
                                        ${flight.layovers.map(layover => `
                                            <div class="layover">
                                                ${layover.city ? `<span class="layover-city">${layover.city}</span>` : ''}
                                                ${layover.duration ? `<span class="layover-duration">${layover.duration}</span>` : ''}
                                            </div>
                                        `).join('')}
                                    </div>
                                ` : '<div class="direct-flight">Direct Flight</div>'}
                            </div>
                            <div class="arrival">
                                ${flight.arrivalTime ? `<time>${flight.arrivalTime}</time>` : ''}
                                ${flight.arrival ? `<p>${flight.arrival}</p>` : ''}
                            </div>
                        </div>
                    </div>
                `).join('');
            } else {
                flightsContainer.innerHTML = '<p>No flight details available.</p>';
            }
        }

        // Display Hotels
        const hotelsContainer = document.querySelector('.hotels-container');
        if (hotelsContainer) {
            if (itineraryData.hotels?.length > 0) {
                hotelsContainer.innerHTML = itineraryData.hotels.map(hotel => `
                    <div class="hotel-card">
                        ${hotel.image ? `<img src="${hotel.image}" alt="${hotel.name || ''}">` : ''}
                        <div class="hotel-info">
                            <h3>${hotel.name || ''}</h3>
                            <div class="rating">${hotel.rating ? '⭐'.repeat(hotel.rating) : ''}</div>
                            <p class="address">${hotel.address || ''}</p>
                            <p class="price">${hotel.price ? '' + hotel.price + '/night' : ''}</p>
                        </div>
                    </div>
                `).join('');
            } else {
                hotelsContainer.innerHTML = '<p>No hotel details available.</p>';
            }
        }

        // Display Weather
        const weatherSummary = document.querySelector('.weather-summary');
        if (weatherSummary) {
            weatherSummary.innerHTML = itineraryData.weather?.trim()
                ? `<p>${itineraryData.weather}</p>`
                : '<p>No weather details available.</p>';
        }

        // Display Activities
        const activitiesList = document.querySelector('.activities-list');
        if (activitiesList) {
            const allActivities = itineraryData.activities?.flatMap(day => day.activities || []) || [];
            const filteredActivities = allActivities.filter(activity =>
                activity && (activity.time || activity.name || activity.description || activity.location)
            );
            if (filteredActivities.length > 0) {
                activitiesList.innerHTML = filteredActivities.map(activity => `
                    <li class="activity-item">
                        ${activity.time ? `<span class="activity-time">${activity.time}</span>` : ''}
                        ${activity.name ? `<strong>${activity.name}</strong>` : ''}
                        ${activity.description ? `<span>${activity.description}</span>` : ''}
                        ${activity.location ? `<span class="activity-location">📍 ${activity.location}</span>` : ''}
                    </li>
                `).join('');
            } else {
                activitiesList.innerHTML = '<li>No activities available.</li>';
            }
        }

        // Accordion setup
        document.querySelectorAll('.accordion-content').forEach(content => {
            content.style.display = "none";
        });
        document.querySelectorAll('.accordion-header').forEach(header => {
            header.addEventListener('click', function () {
                const content = this.nextElementSibling;
                const icon = this.querySelector('.toggle-icon');
                if (content.style.display === "block" || content.style.maxHeight) {
                    content.style.display = "none";
                    content.style.maxHeight = null;
                    if (icon) icon.classList.remove('open');
                } else {
                    content.style.display = "block";
                    content.style.maxHeight = content.scrollHeight + "px";
                    if (icon) icon.classList.add('open');
                }
            });
        });

        // Download PDF button logic
        const downloadBtn = document.getElementById('downloadPdfBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', async function () {
                const tripData = JSON.parse(localStorage.getItem('tripData'));
                if (!tripData) {
                    alert('Trip data not found.');
                    return;
                }
                downloadBtn.disabled = true;
                downloadBtn.textContent = "Preparing PDF...";
                try {
                    const response = await fetch('http://localhost:5000/api/trip/pdf', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            source: tripData.source,
                            destination: tripData.destination,
                            days: Math.ceil(
                                (new Date(tripData.endDate) - new Date(tripData.startDate)) /
                                (1000 * 60 * 60 * 24)
                            ),
                            adults: 1,
                            children: 0,
                            childAges: [],
                            startDate: tripData.startDate,
                            endDate: tripData.endDate
                        })
                    });
                    if (!response.ok) throw new Error('Failed to download PDF');
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    // Use destination in filename, fallback if not present
                    const dest = tripData.destination ? tripData.destination.replace(/[^a-z0-9]/gi, '_').toLowerCase() : 'trip';
                    a.href = url;
                    a.download = `TripGenie_Itinerary_${dest}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                } catch (err) {
                    alert('Could not download PDF. Please try again.');
                }
                downloadBtn.disabled = false;
                downloadBtn.textContent = "⬇️ Download PDF";
            });
        }

    });
}
