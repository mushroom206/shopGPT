// apiService.js

import axios from 'axios';
import { API_URL } from '@/config'
// import { ElMessageBox } from 'element-plus'

const timeout = 120000;

// async function generateList(payload) {
//   try {
//     console.log('Sending axios request with payload: ', payload);
//     const response = await axios.post(`${API_URL}generateList`, payload, { timeout });
//     return response.data;
//   } catch (error) {
//     console.error('Error:', error);
//     ElMessageBox.alert('generateList network error, please try again', 'Info', {
//       // if you want to disable its autofocus
//       // autofocus: false,
//       confirmButtonText: 'OK'
//     })
//   }
// }

async function generateList(payload) {
  const maxRetries = 3;
  const delayBetweenRetriesMs = 1000;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      console.log(`Attempt ${attempt+1}: Sending axios request with payload:`, payload);
      const response = await axios.post(`${API_URL}generateList`, payload, { timeout });
      return response.data;  // If the request is successful, return the result immediately
    } catch (error) {
      console.error('Error:', error);

      // Show an alert
      // ElMessageBox.alert('generateList network error, please try again', 'Info', {
      //   confirmButtonText: 'OK'
      // });

      // If this was the last attempt, rethrow the error
      // if (attempt === maxRetries - 1) {
      //   throw error;
      // }

      // If there are more attempts left, wait for a bit before trying again
      await new Promise(resolve => setTimeout(resolve, delayBetweenRetriesMs));
    }
  }
}


// async function searchItems(payload) {
//   try {
//     console.log('Sending axios request with payload: ', payload);
//     const response = await axios.post(`${API_URL}search`, payload, { timeout });
//     return response.data;
//   } catch (error) {
//     console.error('Error:', error);
//     ElMessageBox.alert('searchItems network error, please try again', 'Info', {
//       // if you want to disable its autofocus
//       // autofocus: false,
//       confirmButtonText: 'OK'
//     })
//   }
// }

async function searchItems(payload) {
  const maxRetries = 3;
  const delayBetweenRetriesMs = 1000;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      console.log(`Attempt ${attempt+1}: Sending axios request with payload:`, payload);
      const response = await axios.post(`${API_URL}search`, payload, { timeout });
      return response.data;  // If the request is successful, return the result immediately
    } catch (error) {
      console.error('Error:', error);

      // ElMessageBox.alert('searchItems network error, please try again', 'Info', {
      //   // if you want to disable its autofocus
      //   // autofocus: false,
      //   confirmButtonText: 'OK'
      // })

      // If this was the last attempt, rethrow the error
      // if (attempt === maxRetries - 1) {
      //   throw error;
      // }

      // If there are more attempts left, wait for a bit before trying again
      await new Promise(resolve => setTimeout(resolve, delayBetweenRetriesMs));
    }
  }
}


// async function searchProperties(payload) {
//   try {
//     console.log('Sending axios request with payload: ', payload);
//     const response = await axios.post(`${API_URL}searchProperties`, payload, { timeout });
//     return response.data;
//   } catch (error) {
//     console.error('Error:', error);
//     ElMessageBox.alert('searchProperties network error, please try again', 'Info', {
//       // if you want to disable its autofocus
//       // autofocus: false,
//       confirmButtonText: 'OK'
//     })
//   }
// }

// async function refineSearchItems(queryObject) {
//   try {
//     const response = await axios.post(`${API_URL}refineSearch`, queryObject, { timeout });
//     return response.data;
//   } catch (error) {
//     console.error('Error:', error);
//     ElMessageBox.alert('refineSearchItems network error, please try again', 'Info', {
//       // if you want to disable its autofocus
//       // autofocus: false,
//       confirmButtonText: 'OK'
//     })
//   }
// }

// async function askItemDetails(queryObject) {
//   try {
//     const response = await axios.post(`${API_URL}ask`, { queryObject }, { timeout });
//     return response.data;
//   } catch (error) {
//     console.error('Error:', error);
//     ElMessageBox.alert('askItemDetails network error, please try again', 'Info', {
//       // if you want to disable its autofocus
//       // autofocus: false,
//       confirmButtonText: 'OK'
//     })
//   }
// }

async function searchProperties(payload) {
  const maxRetries = 3;
  const delayBetweenRetriesMs = 1000;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      console.log(`Attempt ${attempt+1}: Sending axios request with payload:`, payload);
      const response = await axios.post(`${API_URL}searchProperties`, payload, { timeout });
      return response.data;
    } catch (error) {
      console.error('Error:', error);

      // Show an alert
      // ElMessageBox.alert('searchProperties network error, please try again', 'Info', {
      //   confirmButtonText: 'OK'
      // });

      // If this was the last attempt, rethrow the error
      // if (attempt === maxRetries - 1) {
      //   throw error;
      // }

      // If there are more attempts left, wait for a bit before trying again
      await new Promise(resolve => setTimeout(resolve, delayBetweenRetriesMs));
    }
  }
}

async function refineSearchItems(queryObject) {
  const maxRetries = 3;
  const delayBetweenRetriesMs = 1000;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await axios.post(`${API_URL}refineSearch`, queryObject, { timeout });
      return response.data;
    } catch (error) {
      console.error('Error:', error);

      // Show an alert
      // ElMessageBox.alert('refineSearchItems network error, please try again', 'Info', {
      //   confirmButtonText: 'OK'
      // });

      // If this was the last attempt, rethrow the error
      // if (attempt === maxRetries - 1) {
      //   throw error;
      // }

      // If there are more attempts left, wait for a bit before trying again
      await new Promise(resolve => setTimeout(resolve, delayBetweenRetriesMs));
    }
  }
}

async function askItemDetails(queryObject) {
  const maxRetries = 3;
  const delayBetweenRetriesMs = 1000;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await axios.post(`${API_URL}ask`, { queryObject }, { timeout });
      return response.data;
    } catch (error) {
      console.error('Error:', error);

      // Show an alert
      // ElMessageBox.alert('askItemDetails network error, please try again', 'Info', {
      //   confirmButtonText: 'OK'
      // });

      // If this was the last attempt, rethrow the error
      // if (attempt === maxRetries - 1) {
      //   throw error;
      // }

      // If there are more attempts left, wait for a bit before trying again
      await new Promise(resolve => setTimeout(resolve, delayBetweenRetriesMs));
    }
  }
}


async function saveEmail(email) {
  try {
    const response = await axios.post(`${API_URL}saveEmail`, { email }, { timeout });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    // ElMessageBox.alert('saveEmail network error, please try again', 'Info', {
    //   if you want to disable its autofocus
    //   autofocus: false,
    //   confirmButtonText: 'OK'
    // })
  }
}

async function getUserSearchHistory(userId) {
  try {
    const response = await axios.get(`${API_URL}search-history/${userId}`, { timeout });
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    // ElMessageBox.alert('getUserSearchHistory network error, please try again', 'Info', {
    //   confirmButtonText: 'OK'
    // })
  }
}

export default {
  generateList,
  searchItems,
  searchProperties,
  refineSearchItems,
  askItemDetails,
  saveEmail,
  getUserSearchHistory
}
