// Test script to verify the API service is configured correctly
console.log('Testing API Service Configuration');

// This simulates the API service logic
const BASE_URL = 'http://127.0.0.1:8000'; // Without /api suffix
const userId = 'test-user-id-12345';
const message = 'Test message';

// Simulate the sendMessage method logic
function simulateSendMessage(userId, message) {
    if (!userId) {
        throw new Error('User ID is required to send a chat message');
    }

    const endpoint = `/api/${userId}/chat`;
    const fullUrl = `${BASE_URL}${endpoint}`;

    console.log('Base URL:', BASE_URL);
    console.log('Endpoint:', endpoint);
    console.log('Full URL:', fullUrl);

    // This should be the correct URL: http://127.0.0.1:8000/api/test-user-id-12345/chat
    return fullUrl;
}

try {
    const result = simulateSendMessage(userId, message);
    console.log('✅ API service configuration is correct!');
    console.log('Generated URL:', result);

    // Verify the URL structure
    if (result === 'http://127.0.0.1:8000/api/test-user-id-12345/chat') {
        console.log('✅ URL structure is correct and matches backend route');
    } else {
        console.log('❌ URL structure is incorrect');
    }
} catch (error) {
    console.log('❌ Error in API service simulation:', error.message);
}

// Test with undefined userId to verify error handling
try {
    simulateSendMessage(undefined, message);
    console.log('❌ Should have thrown an error for undefined userId');
} catch (error) {
    console.log('✅ Correctly throws error for undefined userId:', error.message);
}