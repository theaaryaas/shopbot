// Chatbot elements
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const loadingIndicator = document.getElementById('loadingIndicator');

// Base URL for your Flask backend
const backendBaseUrl = 'http://127.0.0.1:5000'; // Make sure this matches your Flask server's address and port

// Function to add a message to the chat display
function addMessage(text, sender, product = null) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', sender);

    if (product && sender === 'bot') {
        // If it's a bot message with product info, format it
        // The HTML for product display is carefully crafted with Tailwind classes for responsiveness
        const productHtml = `
            <p>${text}</p>
            <div class="product-display bg-gray-700 p-3 rounded-lg mt-2 flex flex-col sm:flex-row items-center space-y-3 sm:space-y-0 sm:space-x-4">
                <img src="${product.imageUrl}" alt="${product.name}" onerror="this.onerror=null;this.src='https://placehold.co/60x60/cccccc/333333?text=N/A';" class="w-16 h-16 object-cover rounded-md flex-shrink-0">
                <div class="product-details flex-grow text-center sm:text-left">
                    <h4 class="font-bold text-lg text-white">${product.name}</h4>
                    <p class="text-sm text-gray-300">Category: ${product.category}</p>
                    <p class="text-md text-green-400 font-semibold">Price: ₹${product.price}</p>
                    <p class="text-xs text-gray-400 mt-1">${product.description}</p>
                </div>
                <div class="product-actions flex flex-col space-y-2 w-full sm:w-auto">
                    <button class="add-to-cart-btn bg-blue-500 hover:bg-blue-600 text-white text-sm font-bold py-2 px-3 rounded-md transition-colors duration-200 w-full" data-product-id="${product.id}">Add to Cart</button>
                    <button class="buy-now-btn bg-green-500 hover:bg-green-600 text-white text-sm font-bold py-2 px-3 rounded-md transition-colors duration-200 w-full" data-product-id="${product.id}">Buy Now</button>
                </div>
            </div>
        `;
        messageDiv.innerHTML = productHtml;

        // Add event listeners for the new buttons
        // These are mock actions, in a real app they'd send data to a backend
        messageDiv.querySelector('.add-to-cart-btn').addEventListener('click', () => {
            console.log(`Product ${product.name} (ID: ${product.id}) added to cart.`);
            addMessage(`Excellent choice! "${product.name}" has been added to your cart. Ready to checkout, or looking for anything else?`, 'bot');
        });
        messageDiv.querySelector('.buy-now-btn').addEventListener('click', () => {
            console.log(`Initiating purchase for Product ${product.name} (ID: ${product.id}).`);
            addMessage(`Great! Proceeding with the purchase of "${product.name}"! What's your delivery address? (This is a demo, no actual purchase will be made)`, 'bot');
        });

    } else {
        messageDiv.textContent = text;
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
}

// Function to get bot response
async function getBotResponse(userMessage) {
    loadingIndicator.classList.add('show'); // Show loading indicator
    sendButton.disabled = true; // Disable button while loading

    try {
        let chatHistory = [];
        let botPrompt;

        // --- Step 1: Try to search products from the mock backend ---
        let productsFound = [];
        let backendIssueOccurred = false; // Flag to track backend connectivity issues

        try {
            const productSearchResponse = await fetch(`${backendBaseUrl}/products/search?query=${encodeURIComponent(userMessage)}`);
            if (!productSearchResponse.ok) {
                backendIssueOccurred = true;
                addMessage("I'm having trouble connecting to the product database right now. Please ensure the backend server is running and accessible.", 'bot');
                console.error("Backend error:", productSearchResponse.status, productSearchResponse.statusText);
            } else {
                productsFound = await productSearchResponse.json();
                console.log("Backend product search results:", productsFound); // Debugging
            }
        } catch (error) {
            backendIssueOccurred = true;
            addMessage("It looks like I can't reach the product database server. Please make sure it's running and accessible.", 'bot');
            console.error("Network error connecting to backend:", error);
        }

        // Only proceed with Gemini if there was NO backend issue.
        if (backendIssueOccurred) {
            return; // Exit the function as the user has been notified about the backend issue
        }

        if (productsFound.length > 0) {
            // If products are found by the backend, use Gemini to formulate a conversational response
            const productInfoForGemini = productsFound.slice(0, 3).map(p =>
                `Name: ${p.name}, Category: ${p.category}, Price: ₹${p.price}, Description: ${p.description}`
            ).join('\n');

            botPrompt = `You are SHOPBOT, a smart, friendly, and helpful e-commerce sales assistant. Your goal is to guide the user through their shopping experience, just like a real sales agent. The user searched for "${userMessage}". You found these products in the database:\n${productInfoForGemini}\n\nPlease provide a welcoming and helpful response. Highlight the key features of the first product found. If there are multiple results, mention that you found more and suggest they can ask for more specifics or browse other options. Encourage them to use the 'Add to Cart' or 'Buy Now' buttons if they like an item. Keep your response concise, engaging, and in a friendly sales agent tone.`;
            
            chatHistory.push({ role: "user", parts: [{ text: botPrompt + "\n\nUser's message: " + userMessage }] });

            const payload = { contents: chatHistory };
            const apiKey = ""; // Canvas will provide this
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            // *** IMPORTANT CORRECTION HERE ***
            // Check for the full path to the text content before trying to access it
            if (result && result.candidates && result.candidates.length > 0 &&
                result.candidates[0].content && result.candidates[0].content.parts &&
                result.candidates[0].content.parts.length > 0 &&
                result.candidates[0].content.parts[0].text) {
                const botResponse = result.candidates[0].content.parts[0].text;
                addMessage(botResponse, 'bot', productsFound[0]); // Display the first product with Gemini's response
            } else {
                addMessage("I found products in our inventory, but I'm having a little trouble formulating a detailed response right now. Please try asking in a different way or check product details below!", 'bot', productsFound[0]); // Fallback with product
                console.error("Gemini API response structure unexpected for product query:", result);
            }

        } else {
            // --- Step 2: If no products found by backend, use Gemini API for general response ---
            console.log("No products found by backend, falling back to Gemini API for general conversation."); // Debugging
            botPrompt = `You are SHOPBOT, a friendly and helpful shopping assistant. The user asked "${userMessage}" but no specific products were found in the database. Please respond conversationally, suggesting they try different keywords, ask about categories like 'phones', 'laptops', 'headphones', or ask general shopping questions. Emphasize your role as a helpful assistant.`;
            
            chatHistory.push({ role: "user", parts: [{ text: botPrompt + "\n\nUser's message: " + userMessage }] });

            const payload = { contents: chatHistory };
            const apiKey = ""; // Canvas will provide this
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            // *** IMPORTANT CORRECTION HERE ***
            // Check for the full path to the text content before trying to access it
            if (result && result.candidates && result.candidates.length > 0 &&
                result.candidates[0].content && result.candidates[0].content.parts &&
                result.candidates[0].content.parts.length > 0 &&
                result.candidates[0].content.parts[0].text) {
                const botResponse = result.candidates[0].content.parts[0].text;
                addMessage(botResponse, 'bot');
            } else {
                addMessage("Oops! I couldn't get a general response from the assistant. Please try again or ask a different question.", 'bot');
                console.error("Gemini API response structure unexpected for general query:", result);
            }
        }
    } catch (error) {
        // This catch block handles unexpected errors within the getBotResponse function
        console.error('General error in chatbot response generation:', error);
        addMessage("Sorry, I'm having trouble processing your request right now. Please try again later.", 'bot');
    } finally {
        loadingIndicator.classList.remove('show'); // Hide loading indicator
        sendButton.disabled = false; // Re-enable button
    }
}

// Event listener for send button click
sendButton.addEventListener('click', () => {
    const message = chatInput.value.trim();
    if (message) {
        addMessage(message, 'user');
        chatInput.value = ''; // Clear input field
        getBotResponse(message); // Get bot response
    }
});

// Event listener for Enter key press in input field
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click(); // Trigger send button click
    }
});
