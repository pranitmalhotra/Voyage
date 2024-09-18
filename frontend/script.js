const options = {
    "Good For Groups": "goodForGroups",
    "Live Music": "liveMusic",
    "Serves Cocktails": "servesCocktails",
    "Serves Wine": "servesWine",
    "Allows Dogs": "allowsDogs",
    "Good For Children": "goodForChildren",
    "Good for Watching Sports": "goodForWatchingSports",
    "Outdoor Seating": "outdoorSeating",
    "Serves Beer": "servesBeer",
    "Serves Vegetarian Food": "servesVegetarianFood"
};

const option1 = document.getElementById('option1');
const option2 = document.getElementById('option2');
const option3 = document.getElementById('option3');
const emailInput = document.getElementById('email');

function populateDropdown(dropdown) {
    for (const displayText in options) {
        const opt = document.createElement('option');
        opt.value = options[displayText];
        opt.text = displayText;
        dropdown.appendChild(opt);
    }
}

populateDropdown(option1);
populateDropdown(option2);
populateDropdown(option3);

function updateDropdowns() {
    const selectedOptions = [
        option1.value, 
        option2.value, 
        option3.value
    ];

    [option1, option2, option3].forEach(dropdown => {
        const currentValue = dropdown.value;
        dropdown.innerHTML = '<option value="" disabled>Select an option</option>';
        
        for (const displayText in options) {
            if (!selectedOptions.includes(options[displayText]) || options[displayText] === currentValue) {
                const opt = document.createElement('option');
                opt.value = options[displayText];
                opt.text = displayText;
                if (options[displayText] === currentValue) opt.selected = true;
                dropdown.appendChild(opt);
            }
        }
    });
}

[option1, option2, option3].forEach(dropdown => {
    dropdown.addEventListener('change', updateDropdowns);
});

function submitForm() {
    const option1Value = option1.value;
    const option2Value = option2.value;
    const option3Value = option3.value;
    const emailValue = emailInput.value || 'none';

    const destination = sessionStorage.getItem("destination");
    const duration = sessionStorage.getItem("duration");
    const budget = sessionStorage.getItem("budget");
    const hotel = sessionStorage.getItem("hotel");
    const breakfast = sessionStorage.getItem("breakfast");

    const data = {
        destination: destination,
        duration: parseInt(duration),
        budget: budget,
        hotel: hotel,
        breakfast: breakfast,
        email: emailValue,
        preferences: {
            [option1Value]: true, 
            [option2Value]: true, 
            [option3Value]: true
        }
    };

    fetch('http://localhost:8000/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.status === 422) {
            return response.json().then(errData => {
                alert("Error 422: " + (errData.message || "Unprocessable Entity"));
            });
        } else if (!response.ok) {
            throw new Error('Something went wrong');
        } else {
            return response.json();
        }
    })
    .then(result => {
        console.log('Success:', result);
        alert('Form submitted successfully!');
        sessionStorage.setItem('daily_itineraries', JSON.stringify(result.daily_itineraries));
        window.location.href = 'itinerary.html';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}
