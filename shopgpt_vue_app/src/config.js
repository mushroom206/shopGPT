const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://shopgpt-cloudbuild-service-7bz57dofha-wl.a.run.app' 
  : 'http://localhost:5000';

module.exports = { API_URL };

