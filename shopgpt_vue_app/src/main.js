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
    'question?' : 'question?',
    'Ask AI' : 'Ask AI',
    'Pros': 'Pros',
    'Cons': 'Cons',
    'Help me get ready': 'Help me get ready',
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
    'Hide Search Menu': 'Hide Search Menu',
    'Show Search Menu': 'Show Search Menu',
    'Pre item loading...': 'Pre item loading...',
    'Next item loading...': 'Next item loading...',
    'Shopping Cart': 'Shopping Cart',
    'Check out on Amazon': 'Check out on Amazon',
    'Confirm List and View Items': 'Confirm List and View Items',
    'Fulfilled by Amazon': 'Fulfilled by Amazon',
    'Free Shipping': 'Free Shipping',
    'Prime Eligible': 'Prime Eligible',
    'Above 4 stars': 'Above 4 stars',
    'Find similar Item': 'Find similar Item',
    'Your Activity': 'Your Activity',
    'Essentials': 'Essentials',
    'Options': 'Options',
    'Household products': 'Household products',
    'Deep Discount': 'Deep Discount',
    'looking for something?': 'looking for something?',
    'Find Deal': 'Find Deal',
    'Discover items with': 'Discover items with',
    'most value': 'most value',
    'best rating': 'best rating',
    'fastest delivery': 'fastest delivery',
    'and': 'and',
    'significant discounts': 'significant discounts',
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
    'question?' : '有问题？',
    'Ask AI' : '问 AI',
    'Pros': '优点',
    'Cons': '缺点',
    'Help me get ready': '帮我准备',
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
    'Hide Search Menu': '隐藏搜索菜单',
    'Show Search Menu': '打开搜索菜单',
    'Pre item loading...': '正加载前项...',
    'Next item loading...': '正加载后项...',
    'Shopping Cart': '购物车',
    'Check out on Amazon': '去Amazon买单',
    'Confirm List and View Items': '确认清单开始选品',
    'Fulfilled by Amazon': 'Amazon发货',
    'Free Shipping': '免运费',
    'Prime Eligible': 'Prime会员',
    'Above 4 stars': '评价高于4星',
    'Find similar Item': '找近似商品',
    'Your Activity': '你的活动',
    'Essentials': '必需品',
    'Options': '选项',
    'Household products': '家居用品',
    'Deep Discount': '大幅折扣',
    'looking for something?': '需要什么吗？',
    'Find Deal': '最优选',
    'Discover items with': '找到',
    'most value': '最有价值',
    'best rating': '最高评价',
    'fastest delivery': '最快送达',
    'and': '以及',
    'significant discounts': '最高折扣',
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
      userSearchHistory: [],
      inSearchList: []
    }
  },
  mutations: {
    setGenerateListResults(state, results) {
      state.generateListResults = results;
    },
    setListResults(state, results) {
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
      // let {results1, results2} = payload
      let {results1} = payload
      if (Object.prototype.hasOwnProperty.call(state.listResults, results1.target)) {
        let item = state.listResults[results1.target]
        item.choices = results1.choices;
        if(results1.empty){
          item.empty = true
        }else{
          item.empty = false
          // item['qualities-properties'] = results2['qualities-properties'];
        }
        if(item.isSet){
          this.commit('setSearchResults', item)
          item.isSet = !item.isSet
          this.commit('endLoading')
        }
      }
      console.log(state.listResults)
    },
    setSearchResults(state, results) {
        console.log(results)
        // Check if 'qualities-properties' exists in results
        if (!Object.prototype.hasOwnProperty.call(results, 'qualities-properties')) {
            // If it does not exist, copy it from state.searchResults
            results['qualities-properties'] = state.searchResults['qualities-properties'];
        }
        if(!results.empty){
          //check if properties are included in the target
          if(results.target.includes(state.searchResults.target) 
          && results['qualities-properties']
          && results['qualities-properties'].length != 0 
          && !results.target.include(results['qualities-properties'][0].quality) ){
            results.target = state.searchResults.target
          }
          state.searchResults = results;
        }else{
          // state.searchResults = {
          //   "target": results.target,
          //   "choices": [],
          //   "empty": results.empty
          // }
          ElMessageBox.alert("We did not find anything", 'Sorry!', {
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
    setInSearchList(state, item_query) {
      state.inSearchList.push(item_query);
    },
    removeFromSearchList(state, item_query){
      state.inSearchList = state.inSearchList.filter(str => str !== item_query);
    },
    setVariants(state, variantsResult){
      for (let i = 0; i < state.searchResults.choices.length; i++) {
        if (state.searchResults.choices[i].asin === variantsResult.asin) {
          state.searchResults.choices[i].variants = variantsResult.variants;
          state.searchResults.choices[i].variation_dimensions = variantsResult.variation_dimensions;
          break;  // This will exit the loop after the first match is found
        }
      }
    }
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
      commit('endLoading'); 
      // ElMessageBox.alert(results['tip'], 'tip', {
        // if you want to disable its autofocus
        // autofocus: false,
        // confirmButtonText: 'OK',
        // callback: (action) => {  // Remove type annotation here
        //   ElMessage({
        //     type: 'info',
        //     message: `action: ${action}`,
        //   })
        // },
      // })
      payload.item_query = results.itemList[0]
      dispatch('fetchSearchResults', payload)

      let payload1 = {...payload}
          payload1.item_query = results.itemList[1]
          payload1.commit_flag = false;
          setTimeout(() => { 
          dispatch('fetchSearchResults', payload1)
          }, 3000);

      // results.itemList.forEach((result, index) => {
      //   if(index != 0){
      //     let payload1 = {...payload}
      //     payload1.item_query = result
      //     payload1.commit_flag = false;
      //     setTimeout(() => { 
      //     dispatch('fetchSearchResults', payload1)
      //     }, 3000);
      //   }
      // });
      
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
      
      if(!store.state.inSearchList.includes(payload.item_query)){
        commit('setInSearchList', payload.item_query);
      }
      
      let results1;
      // let results2;
      try {
        // const [response1, response2] = await Promise.all(
        const [response1] = await Promise.all(  
          [apiService.searchItems(payload), 
            // apiService.searchProperties(payload)
          ]
          );
        // try {
          results1 = response1;
          console.log(results1)
        // } catch (e) {
        //   console.error('Error parsing response:', e);
        //   results = response;  // Use the original response if parsing fails
        // }
        // try {
        //   results2 = JSON.parse(response2);
        // } catch (e) {
        //   console.error('Error parsing response:', e);
        //   results2 = response2;  // Use the original response if parsing fails
        // }  
      } catch (error) {
        // handle error here if necessary
        console.error('Error:', error);
      } finally {
        commit('removeFromSearchList', payload.item_query);
      }

      if(results1){
        if(payload.commit_flag){
          commit('setSearchResults', results1);
          // if(!results1.empty){
          //   commit('setSearchPropertiesResults', results2);
          // }
        }
        commit('setListResultsItem', {results1});
        // commit('setListResultsItem', {results1, results2});
      }
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
  async fetchMoreItems({ commit, dispatch }) {
    try {
      commit('startLoading');  // Start loading before the API request
      let queryObject = store.state.generateListResults
      queryObject.loading_flag = false;
      queryObject.commit_flag = true;
      queryObject.language = store.state.lang;
      const response = await apiService.getMoreItems(queryObject);
      let results;
      try {
        results = JSON.parse(response);
      } catch (e) {
        console.error('Error parsing response:', e);
        results = response;  // Use the original response if parsing fails
      }
      store.state.generateListResults.itemList =  store.state.generateListResults.itemList.concat(results.itemList)
      commit('setListResults', results.itemList);
      commit('endLoading'); 
      // ElMessageBox.alert(results['tip'], 'tip', {
        // if you want to disable its autofocus
        // autofocus: false,
        // confirmButtonText: 'OK',
        // callback: (action) => {  // Remove type annotation here
        //   ElMessage({
        //     type: 'info',
        //     message: `action: ${action}`,
        //   })
        // },
      // })
      queryObject.item_query = results.itemList[0]
      dispatch('fetchSearchResults', queryObject)

      let queryObject1 = {...queryObject}
          queryObject1.item_query = results.itemList[1]
          queryObject1.commit_flag = false;
          setTimeout(() => { 
          dispatch('fetchSearchResults', queryObject1)
          }, 3000);

      // results.itemList.forEach((result, index) => {
      //   if(index != 0){
      //     let queryObject1 = {...queryObject}
      //     queryObject1.item_query = result
      //     queryObject1.commit_flag = false;
      //     setTimeout(() => { 
      //     dispatch('fetchSearchResults', queryObject1)
      //     }, 3000);
      //   }
      // });
      
    } catch (error) {
      console.error('Error fetching search results:', error);
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
  async startLoading({ commit }) {
    commit('startLoading');
  },
  async endLoading({ commit }) {
    commit('endLoading');
  },
  async setSearchResults({ commit }, item) {
    commit('setSearchResults', item);
  },
  async setVariants({ commit }, variantsResult) {
    commit('setVariants', variantsResult);
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
