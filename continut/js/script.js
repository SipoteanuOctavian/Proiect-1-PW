// Afișează data și timpul curent
function showDateTime() {
    const currentDate = new Date();
    document.getElementById('dateTime').innerHTML = currentDate.toLocaleString();
}

// Afișează informații despre browser și sistemul de operare
function showBrowserInfo() {
    let osName = "Necunoscut";

    if (navigator.platform.toUpperCase().indexOf("WIN") != -1) osName = "Windows";
    if (navigator.platform.toUpperCase().indexOf("MAC") != -1) osName = "MacOS";
    if (navigator.platform.toUpperCase().indexOf("LINUX") != -1) osName = "Linux";

    let browserName = "Necunoscut";

    if (navigator.userAgent.includes("Chrome")) {
        browserName = "Chrome";
    } else if (navigator.userAgent.includes("Firefox")) {
        browserName = "Firefox";
    } else if (navigator.userAgent.includes("Safari")) {
        browserName = "Safari";
    } else if (navigator.userAgent.includes("Edg")) {
        browserName = "Edge";
    } else if (navigator.userAgent.includes("Opera")) {
        browserName = "Opera";
    }

    const browserInfo = `
        Numele browser-ului: ${browserName}<br>
        Versiunea browser-ului: ${navigator.userAgent.match(/(Chrome|Firefox|Edg|Opera|Safari)\/(\S+)/)[2]}<br>
        Sistemul de operare: ${osName}
    `;

    document.getElementById('browserInfo').innerHTML = browserInfo;
}

// Afișează adresa URL și locația curentă
function showLocation() {
    fetch('https://geolocation-db.com/json/')
        .then(response => response.json())
        .then(data => {
            const locationInfo = `
                Adresa URL: ${window.location.href}<br>
                Locația curentă: ${data.city}, ${data.country_name}
            `;
            document.getElementById('locationInfo').innerHTML = locationInfo;
        })
        .catch(error => {
            console.error('Eroare la obținerea locației:', error);
            document.getElementById('locationInfo').innerHTML = 'Eroare la obținerea locației.';
        });
}

// Funcție de actualizare a timpului în timp real
function updateTime() {
    const currentTime = new Date();
    document.getElementById('realTime').innerHTML = currentTime.toLocaleTimeString();
}

// Variabile pentru canvas și contextul său
let canvas;
let ctx;
let isDrawing = false;
let startX, startY;

function initCanvas() {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    // Setare dimensiuni canvas
    canvas.width = 800;
    canvas.height = 400;

    // Evenimente mouse pentru desenare
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        startX = e.offsetX;
        startY = e.offsetY;
    });

    canvas.addEventListener('mouseup', (e) => {
        if (isDrawing) {
            const endX = e.offsetX;
            const endY = e.offsetY;
            
            const width = endX - startX;
            const height = endY - startY;

            ctx.strokeStyle = document.getElementById('strokeColor').value;
            ctx.fillStyle = document.getElementById('fillColor').value;

            ctx.beginPath();
            ctx.rect(startX, startY, width, height);
            ctx.fill();
            ctx.stroke();

            isDrawing = false;
        }
    });

    canvas.addEventListener('mousemove', (e) => {
        if (isDrawing) {
            const endX = e.offsetX;
            const endY = e.offsetY;
            
            const width = endX - startX;
            const height = endY - startY;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.strokeStyle = document.getElementById('strokeColor').value;
            ctx.fillStyle = document.getElementById('fillColor').value;

            ctx.beginPath();
            ctx.rect(startX, startY, width, height);
            ctx.fill();
            ctx.stroke();
        }
    });
}

function insertRow() {
    const position = document.getElementById('position').value;
    const bgColor = document.getElementById('bgColor').value;
    
    const table = document.getElementById('myTable');
    const rowPos = parseInt(position.split('/')[0], 10);
    
    if (rowPos <= table.rows.length) {
        const newRow = table.insertRow(rowPos);
        
        for (let i = 0; i < table.rows[0].cells.length; i++) {
            const cell = newRow.insertCell(i);
            cell.innerHTML = `Rând Nou ${rowPos}, Celulă ${i + 1}`;
            cell.style.backgroundColor = bgColor;
        }
    } else {
        alert('Poziția specificată este în afara intervalului tabelului!');
    }
}

function insertColumn() {
    const position = document.getElementById('position').value;
    const bgColor = document.getElementById('bgColor').value;
    
    const table = document.getElementById('myTable');
    const colPos = parseInt(position.split('/')[1], 10);
    
    if (colPos <= table.rows[0].cells.length) {
        for (let i = 0; i < table.rows.length; i++) {
            const cell = table.rows[i].insertCell(colPos);
            cell.innerHTML = `Coloană Nouă ${colPos}, Celulă ${i + 1}`;
            cell.style.backgroundColor = bgColor;
        }
    } else {
        alert('Poziția specificată este în afara intervalului tabelului!');
    }
}

// Setare evenimente pentru afișarea informațiilor
window.onload = function () {
    showDateTime();
    showBrowserInfo();
    showLocation();
    setInterval(updateTime, 1000); // Actualizează timpul în fiecare secundă

    // Inițializare canvas
    initCanvas();
};
