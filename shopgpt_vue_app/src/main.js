// main.js

import { createStore } from 'vuex'
import { createApp } from 'vue'
import App from './App.vue'
import apiService from './services/apiService'
import './assets/global.css'
import Vue from 'vue'
import router from './router'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

const store = createStore({
  state() {
    return {
      searchResults: [],
    }
  },
  mutations: {
    setSearchResults(state, results) {
        // Check if 'qualities-properties' exists in results
        if (!Object.prototype.hasOwnProperty.call(results, 'qualities-properties')) {
            // If it does not exist, copy it from state.searchResults
            results['qualities-properties'] = state.searchResults['qualities-properties'];
        }

        state.searchResults = results;
    }
},
  actions: {
    async fetchSearchResults({ commit }, item_query) {
      console.log('Dispatching fetchSearchResults with item_query: ', item_query);
      const response = await apiService.searchItems(item_query);
  
      // If the response is already an object, this will have no effect.
      // If the response is a JSON string, it will be parsed into an object.
      let results;
      try {
        results = JSON.parse(response);
      } catch (e) {
        console.error('Error parsing response:', e);
        results = response;  // Use the original response if parsing fails
      }
  
      commit('setSearchResults', results);
    },
    async fetchRefinedSearchResults({ commit }, queryObject) {
      const response = await apiService.refineSearchItems(queryObject);
      
      let results;
      try {
        results = JSON.parse(response);
      } catch (e) {
        console.error('Error parsing refined search response:', e);
        results = response; // Use the original response if parsing fails
      }

      commit('setSearchResults', results);
    }
  }
})

const app = createApp(App)

app.use(store)
app.mount('#app')
