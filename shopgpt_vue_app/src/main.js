// main.js

import { createStore } from 'vuex'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import apiService from './services/apiService'
import './assets/global.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import vue3GoogleLogin from 'vue3-google-login'
import { createI18n } from 'vue-i18n'
import { ElMessageBox } from 'element-plus'


// Import your views
import HomePage from './views/HomePage.vue'
import PrivacyPolicy from './views/PrivacyPolicy.vue'
import TermsOfService from './views/TermsOfService.vue'
import DataDeletion from './views/DataDeletion.vue'

// Define your routes
const routes = [
  { path: '/', component: HomePage },
  { path: '/privacy-policy', component: PrivacyPolicy },
  { path: '/terms-of-service', component: TermsOfService },
  { path: '/data-deletion', component: DataDeletion }
]

// Create the router instance and pass the `routes` option
const router = createRouter({
  history: createWebHistory(),
  routes,
})

const messages = {
  english: {
    'Log Out': 'Log Out',
    'Privacy Policy': 'Privacy Policy',
    'Terms of Service': 'Terms of Service',
    'smart watch, Christmas gift, etc.' : 'smart watch, Christmas gift, etc.',
    'Search' : 'Search',
    'Thinking...' : 'Thinking...',
    'Fine Tune Choices!' : 'Fine Tune Choices!',
    'Tell me more about this item' : 'Tell me more about this item',
    'Ask AI' : 'Ask AI',
    'Pros': 'Pros',
    'Cons': 'Cons',
    // other translations...
  },
  chinese: {
    'Log Out': '登出',
    'Privacy Policy': '隐私条例',
    'Terms of Service': '服务声明',
    'smart watch, Christmas gift, etc.': '蓝牙音箱，圣诞礼物，等',
    'Search' : '搜索',
    'Thinking...' : '思考中...',
    'Fine Tune Choices!' : '优化搜索',
    'Tell me more about this item' : '我想了解更多',
    'Ask AI' : '问 AI',
    'Pros': '优点',
    'Cons': '缺点',
    // other translations...
  }
  // other languages...
}

const store = createStore({
  state() {
    return {
      searchResults: {
        choices: []
      },
      loading: false, 
      lang: 'english',  // default language is English
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
    },
    startLoading(state) {  // Add this mutation
      state.loading = true;
    },
    endLoading(state) {  // Add this mutation
      state.loading = false;
    },
    setLanguage(state, lang) {  // Add this mutation to change the language
      state.lang = lang;
      i18n.global.locale = store.state.lang; 
    }
},
actions: {
  async fetchSearchResults({ commit }, payload) {
    try {
      commit('startLoading');  // Start loading before the API request
      payload.language = store.state.lang;
      const response = await apiService.searchItems(payload);
      let results;
      try {
        results = JSON.parse(response);
      } catch (e) {
        console.error('Error parsing response:', e);
        results = response;  // Use the original response if parsing fails
      }
      commit('setSearchResults', results);
    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      commit('endLoading');  // End loading after the API request and committing the results or catching an error
    }
  },
  async fetchRefinedSearchResults({ commit }, queryObject) {
    try {
      commit('startLoading');  // Start loading before the API request
      queryObject.language = store.state.lang;
      const response = await apiService.refineSearchItems(queryObject);
      let results;
      try {
        results = JSON.parse(response);
      } catch (e) {
        console.error('Error parsing refined search response:', e);
        results = response; // Use the original response if parsing fails
      }
      commit('setSearchResults', results);
    } catch (error) {
      console.error('Error refining search results:', error);
    } finally {
      commit('endLoading');  // End loading after the API request and committing the results or catching an error
    }
  },
  async askQuestion({ commit }, queryObject) {
    try {
      commit('startLoading');  // Start loading before the API request
      queryObject.language = store.state.lang;
      const response = await apiService.askItemDetails(queryObject);
      let results;
      try {
        results = JSON.parse(response);
      } catch (e) {
        console.error('Error parsing ask question response:', e);
        results = response; // Use the original response if parsing fails
      }
      ElMessageBox.alert(results['answer'], 'I\'m Back', {
        // if you want to disable its autofocus
        // autofocus: false,
        confirmButtonText: 'OK',
        // callback: (action) => {  // Remove type annotation here
        //   ElMessage({
        //     type: 'info',
        //     message: `action: ${action}`,
        //   })
        // },
      })
    } catch (error) {
      console.error('Error ask question results:', error);
    } finally {
      commit('endLoading');  // End loading after the API request and committing the results or catching an error
    }
  },
}
})

const i18n = createI18n({
  locale: store.state.lang, // use the language from the Vuex state
  fallbackLocale: 'en', // set fallback locale
  messages, // set locale messages
})

const app = createApp(App)

app.use(store)
app.use(router)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(ElementPlus)
app.use(vue3GoogleLogin, {
  clientId: '386372323157-34tj0kthjhnbcgb9jl9msamk33fi27ad.apps.googleusercontent.com'
})
app.use(i18n)
app.mount('#app')
