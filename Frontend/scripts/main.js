function toggleChildAgeInputs() {
    const childrenCount = document.querySelector('.children-input').value;
    const childAgeContainer = document.getElementById('child-age-container');
    childAgeContainer.style.display = childrenCount > 0 ? 'block' : 'none';
}

async function getSuggestions() {
    const tripData = {
        source: document.querySelector('.source-input').value,
        destination: document.querySelector('.destination-input').value,
        days: document.querySelector('.days-input').value,
        startDate: document.getElementById('start-date').value,
        adults: document.querySelector('.adults-input').value,
        children: document.querySelector('.children-input').value,
        childAges: document.getElementById('child-ages')?.value?.split(',').map(age => age.trim()) || []
    };

    if (!tripData.source || !tripData.destination || !tripData.days || !tripData.startDate || !tripData.adults) {
        alert('Please fill in all required fields');
        return;
    }

    // Show loading modal
    const loadingModal = document.getElementById('loadingModal');
    loadingModal.style.display = 'flex';
    loadingModal.style.opacity = '1';

    try {
        // Update initial status
        updateStatus('flight');

        const response = await fetch('http://localhost:5000/api/trip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(tripData)
        });

        const data = await response.json();

        // Simulate progress updates
        await new Promise(resolve => setTimeout(resolve, 1000));
        updateStatus('flight', true);

        await new Promise(resolve => setTimeout(resolve, 1000));
        updateStatus('hotel', true);

        await new Promise(resolve => setTimeout(resolve, 1000));
        updateStatus('weather', true);

        await new Promise(resolve => setTimeout(resolve, 1000));
        updateStatus('activity', true);

        localStorage.setItem('tripData', JSON.stringify(tripData));
        localStorage.setItem('itineraryData', JSON.stringify(data));

        // Generate and download PDF
        try {
            const pdfResponse = await fetch('http://localhost:5000/api/trip/pdf', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(tripData)
            });

            if (pdfResponse.ok) {
                const blob = await pdfResponse.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                const dest = tripData.destination.replace(/[^a-z0-9]/gi, '_').toLowerCase();
                a.href = url;
                a.download = `TripGenie_Itinerary_${dest}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            }
        } catch (pdfError) {
            console.error('PDF generation failed:', pdfError);
        }

        // Delay redirect to show completion
        setTimeout(() => {
            loadingModal.style.opacity = '0';
            setTimeout(() => {
                loadingModal.style.display = 'none';
                window.location.href = './itinerary.html';
            }, 500);
        }, 1000);

    } catch (error) {
        console.error('Error:', error);
        loadingModal.style.display = 'none';
    }
}

async function simulateProgress() {
    const stages = ['flight', 'hotel', 'weather', 'activity'];
    for (const stage of stages) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        updateStatus(stage, true);
    }
}

async function handlePdfDownload(tripData) {
    try {
        const pdfResponse = await fetch('http://localhost:5000/api/trip/pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(tripData)
        });
        if (pdfResponse.ok) {
            const blob = await pdfResponse.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            const dest = tripData.destination.replace(/[^a-z0-9]/gi, '_').toLowerCase();
            a.href = url;
            a.download = `TripGenie_Itinerary_${dest}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        }
    } catch (error) {
        console.error('PDF download failed:', error);
    }
}

function updateStatus(stage, isComplete = false) {
    const statusElement = document.getElementById(`${stage}Status`);
    if (statusElement) {
        if (isComplete) {
            statusElement.classList.add('completed');
            const textElement = statusElement.querySelector('.status-text');
            textElement.textContent = textElement.textContent.replace('...', ' ✓');
        }
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
});
