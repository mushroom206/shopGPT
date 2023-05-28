const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://shopgpt.firebaseapp.com/api/' 
  : 'http://localhost:5000/api/';

module.exports = { API_URL };

