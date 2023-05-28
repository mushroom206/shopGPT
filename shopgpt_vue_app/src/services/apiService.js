// apiService.js

import axios from 'axios';
import { API_URL } from '@/config'

async function searchItems(payload) {
  try {
    console.log('Sending axios request with payload: ', payload);
    const response = await axios.post(`${API_URL}search`, payload);
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
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

async function saveEmail(email) {
  try {
    const response = await axios.post(`${API_URL}saveEmail`, { email });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

export default {
  searchItems,
  refineSearchItems,
  askItemDetails,
  saveEmail
}
