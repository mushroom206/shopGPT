const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://shopgpt-cloudbuild-service-7bz57dofha-wl.a.run.app/api/' 
  : 'http://localhost:5000/api/';

module.exports = { API_URL };

