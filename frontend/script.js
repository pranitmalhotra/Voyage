const options = {
    "Good For Groups": "goodForGroups",
    "Live Music": "liveMusic",
    "Serves Cocktails": "servesCocktails",
    "Serves Wine": "servesWine",
    "Allows Dogs": "allowsDogs",
    "Good For Children": "goodForChildren",
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

// function updateDropdowns() {
//     const selectedOptions = [
//         option1,
//         option2,
//         option3,
//     ];
    // if((option1==option2)||(option1==option3)||(option2==option3)){
    //     alert("Please select different preference");
    //     return ;
    // }
// }

// [option1, option2, option3].forEach(dropdown => {
//     dropdown.addEventListener('change', updateDropdowns);
// });

function submitForm() {
    const option1Value = option1.value;
    const option2Value = option2.value;
    const option3Value = option3.value;
    const emailValue = emailInput.value;

    if (!option1Value || !option2Value || !option3Value) {
        alert("Please select an option from all dropdowns.");
        return;
    }
    if((option1Value==option2Value)||(option1Value==option3Value)||(option2Value==option3Value)){
        alert("Please select unique preferences");
        return ;
    }
    if (!validateEmail(emailValue)) {
        alert("Please enter a valid email address.");
        return;
    }

    const destination = sessionStorage.getItem("destination");
    const duration = sessionStorage.getItem("duration");
    const startDate = sessionStorage.getItem("start_date");
    const budget = sessionStorage.getItem("budget");
    const hotel = sessionStorage.getItem("hotel");
    const breakfast = sessionStorage.getItem("breakfast");

    if (!destination || !duration || !startDate || !budget || !hotel || !breakfast) {
        alert("Some required data is missing.");
        return;
    }

    const data = {
        destination: destination,
        duration: parseInt(duration, 10),
        startDate: startDate,
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

    fetch('https://voyage.up.railway.app/submit', {
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

function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}
