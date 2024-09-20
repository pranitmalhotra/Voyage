const storedData = sessionStorage.getItem('daily_itineraries');

if (storedData) {
    const itineraries = JSON.parse(storedData);
    const itineraryContainer = document.getElementById('itinerary-container');
    const ifbreakFast = sessionStorage.getItem('breakfast');

    if(ifbreakFast=='yes'){
        if (Array.isArray(itineraries)) {
            itineraries.forEach((day, dayIndex) => {
                const dayElement = document.createElement('div');
                dayElement.classList.add('itinerary');
                dayElement.innerHTML = `<h2>Day ${dayIndex + 1}</h2>`;
                console.log("attractions",day.attractions.length);
                console.log("restaurants",day.restaurants.length);
                console.log("restaurants",day.restaurants);
                if (Array.isArray(day.attractions) && day.attractions.length > 0) {
                    const attractionsSection = document.createElement('div');
                    attractionsSection.innerHTML = `<h3>Attractions 1:</h3>`;
                    const attraction=day.attractions[0];
                        const attractionElement = document.createElement('div');
                        attractionElement.setAttribute("id",`${String(attraction.displayName.text)}`);
                        attractionElement.classList.add('attraction');
                        attractionElement.innerHTML = `
                            <h4>${attraction.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${attraction.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${attraction.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${attraction.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${attraction.rating || 'No rating available'} (${attraction.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${attraction.websiteUri || '#'}" target="_blank">${attraction.websiteUri || 'N/A'}</a></p>

                        `;
                        attractionsSection.appendChild(attractionElement);
                    dayElement.appendChild(attractionsSection);
                }
                if (Array.isArray(day.restaurants) && day.restaurants.length > 0) {
                    const restaurantsSection = document.createElement('div');
                    restaurantsSection.innerHTML = `<h3>Lunch :</h3>`;
                    const restaurant=day.restaurants[0];
                        const restaurantElement = document.createElement('div');
                        if(restaurant.displayName.text=='none'){
                            restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                            restaurantElement.classList.add('restaurant');
                            restaurantElement.innerHTML =`
                            <p>No restaurant found that could qualify the given preferences and budget</p>
                            `
                            restaurantsSection.appendChild(restaurantElement);
                        }else{
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML = `
                            <h4>${restaurant.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${restaurant.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${restaurant.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${restaurant.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${restaurant.rating || 'No rating available'} (${restaurant.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${restaurant.websiteUri || '#'}" target="_blank">${restaurant.websiteUri || 'N/A'}</a></p>
                            
                        `;
                        restaurantsSection.appendChild(restaurantElement);
                    }
                    dayElement.appendChild(restaurantsSection);
                }
                if (Array.isArray(day.attractions) && day.attractions.length > 1) {
                    const attractionsSection = document.createElement('div');
                    attractionsSection.innerHTML = `<h3>Attractions 2:</h3>`;
                    const attraction=day.attractions[1];
                        const attractionElement = document.createElement('div');
                        attractionElement.setAttribute("id",`${String(attraction.displayName.text)}`);
                        attractionElement.classList.add('attraction');
                        attractionElement.innerHTML = `
                            <h4>${attraction.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${attraction.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${attraction.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${attraction.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${attraction.rating || 'No rating available'} (${attraction.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${attraction.websiteUri || '#'}" target="_blank">${attraction.websiteUri || 'N/A'}</a></p>

                        `;
                        attractionsSection.appendChild(attractionElement);
                    dayElement.appendChild(attractionsSection);
                }
                if (Array.isArray(day.attractions) && day.attractions.length > 2) {
                    const attractionsSection = document.createElement('div');
                    attractionsSection.innerHTML = `<h3>Attractions 3:</h3>`;
                    const attraction=day.attractions[2];
                        const attractionElement = document.createElement('div');
                        attractionElement.setAttribute("id",`${String(attraction.displayName.text)}`);
                        attractionElement.classList.add('attraction');
                        attractionElement.innerHTML = `
                            <h4>${attraction.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${attraction.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${attraction.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${attraction.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${attraction.rating || 'No rating available'} (${attraction.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${attraction.websiteUri || '#'}" target="_blank">${attraction.websiteUri || 'N/A'}</a></p>

                        `;
                        attractionsSection.appendChild(attractionElement);
                    dayElement.appendChild(attractionsSection);
                }
                if (Array.isArray(day.restaurants) && day.restaurants.length > 1 && day.restaurants[1]!=null) {
                    const restaurantsSection = document.createElement('div');
                    restaurantsSection.innerHTML = `<h3>Dinner :</h3>`;
                    const restaurant=day.restaurants[1];          
                        const restaurantElement = document.createElement('div');
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML = `
                            <h4>${restaurant.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${restaurant.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${restaurant.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${restaurant.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${restaurant.rating || 'No rating available'} (${restaurant.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${restaurant.websiteUri || '#'}" target="_blank">${restaurant.websiteUri || 'N/A'}</a></p>
                            
                        `;
                        restaurantsSection.appendChild(restaurantElement);
                    
                    dayElement.appendChild(restaurantsSection);
                }

                itineraryContainer.appendChild(dayElement);
                if(Array.isArray(day.attractions) && day.attractions.length > 0){
                    day.attractions.forEach(attraction => {
    
                        if(!attraction.googleMapsUri){
                           var mapLinks= document.getElementById(`${attraction.displayName.text}`).getElementsByClassName("map-link")
                           if (mapLinks.length > 0) {
                            // Access the first element in the collection
                            mapLinks[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!attraction.websiteUri){
                           var Website= document.getElementById(`${attraction.displayName.text}`).getElementsByClassName("web-site")
                           if (Website.length > 0) {
                            // Access the first element in the collection
                                Website[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!attraction.internationalPhoneNumber){
                            var phoneNumber = document.getElementById(`${attraction.displayName.text}`).getElementsByClassName("phone-number")
                            if (phoneNumber.length > 0) {
                                // Access the first element in the collection
                                phoneNumber[0].style.display = "none"; // Set the display property
                                } 
                        }
                    });
                }
                if(Array.isArray(day.restaurants) && day.restaurants.length > 0){
                    day.restaurants.forEach(restaurant => {
                        if(!restaurant.googleMapsUri){
                           var mapLinks= document.getElementById(`${restaurant.displayName.text}`).getElementsByClassName("map-link")
                           if (mapLinks.length > 0) {
                            // Access the first element in the collection
                            mapLinks[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!restaurant.websiteUri){
                           var Website= document.getElementById(`${restaurant.displayName.text}`).getElementsByClassName("web-site")
                           if (Website.length > 0) {
                            // Access the first element in the collection
                                Website[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!restaurant.internationalPhoneNumber){
                            var phoneNumber = document.getElementById(`${restaurant.displayName.text}`).getElementsByClassName("phone-number")
                            if (phoneNumber.length > 0) {
                                // Access the first element in the collection
                                phoneNumber[0].style.display = "none"; // Set the display property
                                } 
                        }
                    });
                }
            });
            
        } else {
            itineraryContainer.innerHTML = '<p>No valid itinerary data found.</p>';
        }
    }else if(ifbreakFast=='no')
        {
        
        if (Array.isArray(itineraries)) {
            itineraries.forEach((day, dayIndex) => {
                console.log(day.restaurants.length);
                console.log(day.attractions.length);
                const dayElement = document.createElement('div');
                dayElement.classList.add('itinerary');
                dayElement.innerHTML = `<h2>Day ${dayIndex + 1}</h2>`;
    
                if (Array.isArray(day.restaurants) && day.restaurants.length > 0) {
                    const restaurantsSection = document.createElement('div');
                    restaurantsSection.innerHTML = `<h3>Breakfast:</h3>`;
                    const restaurant=day.restaurants[0];
                    if(restaurant.displayName.text=='none'){
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML =`
                        <p>No restaurant found that could qualify the given preferences and budget</p>
                        `
                        restaurantsSection.appendChild(restaurantElement);
                    }else{
                        const restaurantElement = document.createElement('div');
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML = `
                            <h4>${restaurant.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${restaurant.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${restaurant.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${restaurant.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${restaurant.rating || 'No rating available'} (${restaurant.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${restaurant.websiteUri || '#'}" target="_blank">${restaurant.websiteUri || 'N/A'}</a></p>
                            
                        `;
                        restaurantsSection.appendChild(restaurantElement);
                    }
                    dayElement.appendChild(restaurantsSection);
                }
                if (Array.isArray(day.attractions) && day.attractions.length > 0) {
                    const attractionsSection = document.createElement('div');
                    attractionsSection.innerHTML = `<h3>Attractions 1:</h3>`;
                    const attraction=day.attractions[0];
                        const attractionElement = document.createElement('div');
                        attractionElement.setAttribute("id",`${String(attraction.displayName.text)}`);
                        attractionElement.classList.add('attraction');
                        attractionElement.innerHTML = `
                            <h4>${attraction.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${attraction.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${attraction.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${attraction.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${attraction.rating || 'No rating available'} (${attraction.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${attraction.websiteUri || '#'}" target="_blank">${attraction.websiteUri || 'N/A'}</a></p>

                        `;
                        attractionsSection.appendChild(attractionElement);
                    dayElement.appendChild(attractionsSection);
                }
                if (Array.isArray(day.restaurants) && day.restaurants.length > 1) {
                    const restaurantsSection = document.createElement('div');
                    restaurantsSection.innerHTML = `<h3>Lunch:</h3>`;
                    const restaurant=day.restaurants[1];
                    if(restaurant.displayName.text=='none'){
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML =`
                        <p>No restaurant found that could qualify the given preferences and budget</p>
                        `
                        restaurantsSection.appendChild(restaurantElement);
                    }else{
                        const restaurantElement = document.createElement('div');
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML = `
                            <h4>${restaurant.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${restaurant.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${restaurant.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${restaurant.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${restaurant.rating || 'No rating available'} (${restaurant.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${restaurant.websiteUri || '#'}" target="_blank">${restaurant.websiteUri || 'N/A'}</a></p>
                            
                        `;
                        restaurantsSection.appendChild(restaurantElement);
                    }
                    dayElement.appendChild(restaurantsSection);
                }
                if (Array.isArray(day.attractions) && day.attractions.length > 1) {
                    const attractionsSection = document.createElement('div');
                    attractionsSection.innerHTML = `<h3>Attractions 2:</h3>`;
                    const attraction=day.attractions[1];
                        const attractionElement = document.createElement('div');
                        attractionElement.setAttribute("id",`${String(attraction.displayName.text)}`);
                        attractionElement.classList.add('attraction');
                        attractionElement.innerHTML = `
                            <h4>${attraction.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${attraction.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${attraction.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${attraction.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${attraction.rating || 'No rating available'} (${attraction.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${attraction.websiteUri || '#'}" target="_blank">${attraction.websiteUri || 'N/A'}</a></p>

                        `;
                        attractionsSection.appendChild(attractionElement);
                    dayElement.appendChild(attractionsSection);
                }
                if (Array.isArray(day.attractions) && day.attractions.length > 2) {
                    const attractionsSection = document.createElement('div');
                    attractionsSection.innerHTML = `<h3>Attractions 3:</h3>`;
                    const attraction=day.attractions[2];
                        const attractionElement = document.createElement('div');
                        attractionElement.setAttribute("id",`${String(attraction.displayName.text)}`);
                        attractionElement.classList.add('attraction');
                        attractionElement.innerHTML = `
                            <h4>${attraction.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${attraction.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${attraction.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${attraction.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${attraction.rating || 'No rating available'} (${attraction.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${attraction.websiteUri || '#'}" target="_blank">${attraction.websiteUri || 'N/A'}</a></p>

                        `;
                        attractionsSection.appendChild(attractionElement);
                    dayElement.appendChild(attractionsSection);
                }
                if (Array.isArray(day.restaurants) && day.restaurants.length > 2) {
                    const restaurantsSection = document.createElement('div');
                    restaurantsSection.innerHTML = `<h3>Dinner:</h3>`;
                    const restaurant=day.restaurants[2];
                    if(restaurant.displayName.text=='none'){
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML =`
                        <p>No restaurant found that could qualify the given preferences and budget</p>
                        `
                        restaurantsSection.appendChild(restaurantElement);
                    }else{
                        const restaurantElement = document.createElement('div');
                        restaurantElement.setAttribute("id",`${String(restaurant.displayName.text)}`);
                        restaurantElement.classList.add('restaurant');
                        restaurantElement.innerHTML = `
                            <h4>${restaurant.displayName?.text || 'No name available'}</h4>
                            <p><strong>Address:</strong> ${restaurant.formattedAddress || 'No address available'}</p>
                            <p class="map-link" ><strong>Google Maps:</strong> <a href="${restaurant.googleMapsUri || '#'}" target="_blank">Link</a></p>
                            <p class="phone-number" ><strong>Phone:</strong> ${restaurant.internationalPhoneNumber || 'N/A'}</p>
                            <p><strong>Rating:</strong> ${restaurant.rating || 'No rating available'} (${restaurant.userRatingCount || 0} reviews)</p>
                            <p class="web-site" ><strong>Website:</strong> <a href="${restaurant.websiteUri || '#'}" target="_blank">${restaurant.websiteUri || 'N/A'}</a></p>
                            
                        `;
                        restaurantsSection.appendChild(restaurantElement);
                    }
                    dayElement.appendChild(restaurantsSection);
                }

                itineraryContainer.appendChild(dayElement);
                if(Array.isArray(day.attractions) && day.attractions.length > 0){
                    day.attractions.forEach(attraction => {
    
                        if(!attraction.googleMapsUri){
                           var mapLinks= document.getElementById(`${attraction.displayName.text}`).getElementsByClassName("map-link")
                           if (mapLinks.length > 0) {
                            // Access the first element in the collection
                            mapLinks[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!attraction.websiteUri){
                           var Website= document.getElementById(`${attraction.displayName.text}`).getElementsByClassName("web-site")
                           if (Website.length > 0) {
                            // Access the first element in the collection
                                Website[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!attraction.internationalPhoneNumber){
                            var phoneNumber = document.getElementById(`${attraction.displayName.text}`).getElementsByClassName("phone-number")
                            if (phoneNumber.length > 0) {
                                // Access the first element in the collection
                                phoneNumber[0].style.display = "none"; // Set the display property
                                } 
                        }
                    });
                }
                if(Array.isArray(day.restaurants) && day.restaurants.length > 0){
                    day.restaurants.forEach(restaurant => {
                        if(!restaurant.googleMapsUri){
                           var mapLinks= document.getElementById(`${restaurant.displayName.text}`).getElementsByClassName("map-link")
                           if (mapLinks.length > 0) {
                            // Access the first element in the collection
                                mapLinks[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!restaurant.websiteUri){
                           var Website= document.getElementById(`${restaurant.displayName.text}`).getElementsByClassName("web-site")
                           if (Website.length > 0) {
                            // Access the first element in the collection
                                Website[0].style.display = "none"; // Set the display property
                            } 
                        }
                        if(!restaurant.internationalPhoneNumber){
                            var phoneNumber = document.getElementById(`${restaurant.displayName.text}`).getElementsByClassName("phone-number")
                            if (phoneNumber.length > 0) {
                                // Access the first element in the collection
                                    phoneNumber[0].style.display = "none"; // Set the display property
                                } 
                        }
                    });
                }
            });
            
        } else {
            itineraryContainer.innerHTML = '<p>No valid itinerary data found.</p>';
        }
    }

    
} else {
    document.getElementById('itinerary-container').innerHTML = '<p>No itinerary data found in session storage.</p>';
}
