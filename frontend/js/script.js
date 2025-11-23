document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const imageUpload = document.getElementById('imageUpload');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingElement = document.getElementById('loading');
    const resultsSection = document.querySelector('.results-section');
    const undertoneResult = document.getElementById('undertoneResult');
    const colorPalette = document.getElementById('colorPalette');
    const fashionResults = document.getElementById('fashionResults');

    // Handle upload area click
    uploadArea.addEventListener('click', function() {
        imageUpload.click();
    });

    // Handle file selection
    imageUpload.addEventListener('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                // Create a preview of the uploaded image
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.maxWidth = '100%';
                img.style.maxHeight = '200px';
                img.style.marginBottom = '15px';
                
                // Clear previous content and add the image
                uploadArea.innerHTML = '';
                uploadArea.appendChild(img);
                
                // Enable the analyze button
                analyzeBtn.disabled = false;
            };
            
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    // ... (previous code remains the same)

// Handle analyze button click
analyzeBtn.addEventListener('click', function() {
    if (!imageUpload.files[0]) return;
    
    // Show loading state
    loadingElement.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    
    // Create FormData to send the image
    const formData = new FormData();
    formData.append('image', imageUpload.files[0]);
    
    // Send the image to the FastAPI backend for processing
    axios.post('http://localhost:8000/api/analyze', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    .then(response => {
        // Hide loading state
        loadingElement.classList.add('hidden');
        
        // Display results
        displayResults(response.data);
        resultsSection.classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        loadingElement.classList.add('hidden');
        alert('An error occurred during analysis. Please try again.');
    });
});

// ... (rest of the code remains the same)
       

    // Function to display results
    function displayResults(data) {
        // Display undertone result
        undertoneResult.innerHTML = `
            <p>Your undertone is: <strong>${data.undertone}</strong></p>
        `;
        
        // Display color palette
        colorPalette.innerHTML = '<h3>Recommended Colors:</h3><div class="color-palette"></div>';
        const paletteContainer = colorPalette.querySelector('.color-palette');
        
        data.palette.forEach(color => {
            const colorBox = document.createElement('div');
            colorBox.className = 'color-box';
            colorBox.style.backgroundColor = color;
            colorBox.title = color;
            paletteContainer.appendChild(colorBox);
        });
        
        // Display fashion recommendations
        fashionResults.innerHTML = '<div class="fashion-results"></div>';
        const fashionContainer = fashionResults.querySelector('.fashion-results');
        
        if (data.fashionItems && data.fashionItems.length > 0) {
            data.fashionItems.forEach(item => {
                const fashionItem = document.createElement('div');
                fashionItem.className = 'fashion-item';
                fashionItem.innerHTML = `
                    <img src="${item.image}" alt="${item.title}">
                    <p>${item.title}</p>
                    <a href="${item.link}" target="_blank">View Product</a>
                `;
                fashionContainer.appendChild(fashionItem);
            });
        } else {
            fashionContainer.innerHTML = '<p>No fashion items found for your undertone.</p>';
        }
    }
});