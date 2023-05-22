// apiService.js

import axios from 'axios';

const API_URL = 'http://localhost:5000/api/';

async function searchItems(item_query) {
  try {
    console.log('Sending axios request with item_query: ', item_query);
    const response = await axios.post(`${API_URL}search`, { item_query });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

async function refineSearchItems(queryObject) {
  try {
    const response = await axios.post(`${API_URL}refineSearch`, queryObject);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

export default {
  searchItems,
  refineSearchItems
}
