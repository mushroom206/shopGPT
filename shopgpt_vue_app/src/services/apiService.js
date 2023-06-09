// apiService.js

import axios from 'axios';
import { API_URL } from '@/config'
import { ElMessageBox } from 'element-plus'

async function generateList(payload) {
  try {
    console.log('Sending axios request with payload: ', payload);
    const response = await axios.post(`${API_URL}generateList`, payload);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    ElMessageBox.alert('generateList network error, please try again', 'Info', {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: 'OK'
    })
  }
}

async function searchItems(payload) {
  try {
    console.log('Sending axios request with payload: ', payload);
    const response = await axios.post(`${API_URL}search`, payload);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    ElMessageBox.alert('searchItems network error, please try again', 'Info', {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: 'OK'
    })
  }
}

async function searchProperties(payload) {
  try {
    console.log('Sending axios request with payload: ', payload);
    const response = await axios.post(`${API_URL}searchProperties`, payload);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    ElMessageBox.alert('searchProperties network error, please try again', 'Info', {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: 'OK'
    })
  }
}

async function refineSearchItems(queryObject) {
  try {
    const response = await axios.post(`${API_URL}refineSearch`, queryObject);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    ElMessageBox.alert('refineSearchItems network error, please try again', 'Info', {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: 'OK'
    })
  }
}

async function askItemDetails(queryObject) {
  try {
    const response = await axios.post(`${API_URL}ask`, { queryObject });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    ElMessageBox.alert('askItemDetails network error, please try again', 'Info', {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: 'OK'
    })
  }
}

async function saveEmail(email) {
  try {
    const response = await axios.post(`${API_URL}saveEmail`, { email });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    ElMessageBox.alert('saveEmail network error, please try again', 'Info', {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: 'OK'
    })
  }
}

export default {
  generateList,
  searchItems,
  searchProperties,
  refineSearchItems,
  askItemDetails,
  saveEmail
}
