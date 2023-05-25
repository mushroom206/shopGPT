// apiService.js

import axios from 'axios';
import { API_URL } from '@/config'

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

async function askItemDetails(choice, question) {
  try {
    const response = await axios.post(`${API_URL}ask`, { choice, question });
    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

export default {
  searchItems,
  refineSearchItems,
  askItemDetails
}
