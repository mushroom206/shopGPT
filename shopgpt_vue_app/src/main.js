// main.js

import { createStore } from 'vuex'
import { createApp, reactive } from 'vue'
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
  English: {
    'Log Out': 'Log Out',
    'Privacy Policy': 'Privacy Policy',
    'Terms of Service': 'Terms of Service',
    'smart watch, yoga mat, etc.' : 'smart watch, yoga mat, etc.',
    'Search' : 'Search',
    'Thinking...' : 'Thinking...',
    'Fine Tune Choices!' : 'Fine Tune Choices!',
    'Tell me more about this item' : 'Tell me more about this item',
    'Ask AI' : 'Ask AI',
    'Pros': 'Pros',
    'Cons': 'Cons',
    'Generate Essentials': 'Generate Essentials',
    'what\'s in your mind': 'what\'s in your mind',
    'Just moved, fill my living room': 'Just moved, fill my living room',
    'Fisrt day at college': 'Fisrt day at college',
    'Going camping this weekend': 'Going camping this weekend',
    'Workout in Gym': 'Workout in Gym',
    'First time making Pasta': 'First time making Pasta',
    'Hosting a birthday party': 'Hosting a birthday party',
    'Need office supplies': 'Need office supplies',
    'Expecting a cat': 'Expecting a cat',
    'Daily hair care set': 'Daily hair care set',
    'Facial care set': 'Facial care set',
    'BBQ weekend': 'BBQ weekend',
    'click image to view more': 'click image to view more',
    'more': 'more',
    'Min Price': 'Min Price',
    'Max Price': 'Max Price',
    'Hide Menu': 'Hide Menu',
    'Show Menu': 'Show Menu',
    'Pre item loading...': 'Pre item loading...',
    'Next item loading...': 'Next item loading...',
    // other translations...
  },
  Simplified_Chinese: {
    'Log Out': '登出',
    'Privacy Policy': '隐私条例',
    'Terms of Service': '服务声明',
    'smart watch, yoga mat, etc.': '智能手表，瑜伽垫，等',
    'Search' : '搜索',
    'Thinking...' : '思考中...',
    'Fine Tune Choices!' : '优化结果',
    'Tell me more about this item' : '我想了解更多',
    'Ask AI' : '问 AI',
    'Pros': '优点',
    'Cons': '缺点',
    'Generate Essentials': '生成必需品',
    'what\'s in your mind': '帮你计划',
    'Just moved, fill my living room': '刚搬家，需要客厅用的家具',
    'Fisrt day at college': '大学开学第一天',
    'Going camping this weekend': '周末要去露营',
    'Workout in Gym': '去健身',
    'First time making Pasta': '第一次煮通心粉',
    'Hosting a birthday party': '办生日会',
    'Need office supplies': '需要办公用品',
    'Expecting a cat': '准备养一只猫',
    'Daily hair care set': '每日护发用品',
    'Facial care set': '面部护理用品',
    'BBQ weekend': '周末烧烤',
    'click image to view more': '点击图片查看更多',
    'more': '更多',
    'Min Price': '最低价',
    'Max Price': '最高价',
    'Hide Menu': '隐藏菜单',
    'Show Menu': '打开菜单',
    'Pre item loading...': '正加载前项...',
    'Next item loading...': '正加载后项...',
    // other translations...
  }
  // other languages...
}

const store = createStore({
  state() {
    return {
      generateListResults: {
        itemList: []
      },
      listResults: {},
      searchResults: {
        choices: []
      },
      loading: false, 
      lang: 'English',  // default language is English
      userSearchHistory: []
    }
  },
  mutations: {
    setGenerateListResults(state, results) {
      state.generateListResults = results;
    },
    setListResults(state, results) {
      state.listResults = {};
      results.forEach((result, index) => {
        let pre = index > 0 ? results[index - 1] : '';
        let next = index < results.length - 1 ? results[index + 1] : '';
        state.listResults[result] = {
          "target": result,
          "choices": [],
          "qualities-properties": [],
          "pre": pre,
          "next": next,
        };
      });
      console.log(state.listResults)
    },
    setListResultsItem(state, payload) {
      let {results1, results2} = payload
      if (Object.prototype.hasOwnProperty.call(state.listResults, results1.target)) {
        state.listResults[results1.target].choices = results1.choices;
        if(results1.empty){
          state.listResults[results1.target].empty = true
        }else{
          state.listResults[results1.target].empty = false
          state.listResults[results1.target]['qualities-properties'] = results2['qualities-properties'];
        }
      }
      console.log(state.listResults)
    },
    setSearchResults(state, results) {
        // Check if 'qualities-properties' exists in results
        if (!Object.prototype.hasOwnProperty.call(results, 'qualities-properties')) {
            // If it does not exist, copy it from state.searchResults
            results['qualities-properties'] = state.searchResults['qualities-properties'];
        }
        if(!results.empty){
          state.searchResults = results;
        }else{
          state.searchResults = {
            "target": results.target,
            "choices": [],
            "empty": results.empty
          }
          ElMessageBox.alert("We did not find anything for "+results.target, 'Sorry!', {
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
        }
    },
    setSearchPropertiesResults(state, results) {
      state.searchResults['qualities-properties'] = results['qualities-properties'];
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
    },
    setUserSearchHistory(state, searchHistory) {
      state.userSearchHistory = searchHistory;
    },
},
actions: {
  async fetchGenerateListResults({ commit, dispatch }, payload) {
    try {
      commit('startLoading');  // Start loading before the API request
      payload.language = store.state.lang;
      payload.loading_flag = false;
      payload.commit_flag = true;
      const response = await apiService.generateList(payload);
      let results;
      try {
        results = JSON.parse(response);
      } catch (e) {
        console.error('Error parsing response:', e);
        results = response;  // Use the original response if parsing fails
      }
      commit('setGenerateListResults', results);
      commit('setListResults', results.itemList);
      ElMessageBox.alert(results['tip'], 'tip', {
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
      payload.item_query = results.itemList[0]
      await dispatch('fetchSearchResults', payload),

      payload.item_query = results.itemList[1]
      payload.commit_flag = false;
      setTimeout(() => {
        dispatch('fetchSearchResults', payload)
      }, 1000); 

    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      commit('endLoading');  // End loading after the API request and committing the results or catching an error
    }
  },
  async fetchSearchResults({ commit }, payload) {
    try {
      if(payload.loading_flag){
        commit('startLoading');  // Start loading before the API request
      }
      payload.language = store.state.lang;
      const response1Promise = apiService.searchItems(payload);
      const response2Promise = new Promise(resolve => setTimeout(resolve, 1000))
        .then(() => apiService.searchProperties(payload));
      
      const [response1, response2] = await Promise.all([response1Promise, response2Promise]);
      let results1;
      let results2;
      // try {
        results1 = response1;
        console.log(results1)
      // } catch (e) {
      //   console.error('Error parsing response:', e);
      //   results = response;  // Use the original response if parsing fails
      // }
      try {
        results2 = JSON.parse(response2);
      } catch (e) {
        console.error('Error parsing response:', e);
        results2 = response2;  // Use the original response if parsing fails
      }
      if(payload.commit_flag){
        commit('setSearchResults', results1);
        if(!results1.empty){
          commit('setSearchPropertiesResults', results2);
        }
      }
      commit('setListResultsItem', {results1, results2});
    } catch (error) {
      console.error('Error fetching search results:', error);
    } finally {
      if(payload.loading_flag){
        commit('endLoading');  // End loading after the API request and committing the results or catching an error
      }
    }
  },
  // async fetchPropertiesResults({ commit }, payload) {
  //   try {
  //     payload.language = store.state.lang;
  //     const response = await apiService.searchProperties(payload);
  //     let results;
  //     try {
  //       results = JSON.parse(response);
  //     } catch (e) {
  //       console.error('Error parsing response:', e);
  //       results = response;  // Use the original response if parsing fails
  //     }
  //     commit('setSearchPropertiesResults', results);
  //   } catch (error) {
  //     console.error('Error fetching properties results:', error);
  //   }
  // },
  async fetchRefinedSearchResults({ commit }, queryObject) {
    try {
      commit('startLoading');  // Start loading before the API request
      queryObject.language = store.state.lang;
      const response = await apiService.refineSearchItems(queryObject);
      let results;
      // try {
      //   results = JSON.parse(response);
      // } catch (e) {
      //   console.error('Error parsing refined search response:', e);
        results = response; // Use the original response if parsing fails
      // }
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
  async fetchUserSearchHistory({ commit }, userId) {
    try {
      const searchHistory = await apiService.getUserSearchHistory(userId);
      commit('setUserSearchHistory', searchHistory);
    } catch (error) {
      console.error('Error fetching user search history:', error);
    }
  },
  async setPreItem({ commit }, item) {
    commit('setSearchResults', store.state.listResults[item]);
  },
  async setNextItem({ commit }, item) {
    commit('setSearchResults', store.state.listResults[item]);
  },
}
})

const i18n = createI18n({
  locale: store.state.lang, // use the language from the Vuex state
  fallbackLocale: 'en', // set fallback locale
  messages, // set locale messages
})

const app = createApp(App)
app.provide('globalState', reactive({ itemQuery: '' }))

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
