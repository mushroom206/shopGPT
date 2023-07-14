<template>
  <div class="common-layout">
    <el-container class="el-container">
      <el-header class="el-header">
        <el-row :gutter="20" justify="center">
          <el-col :xs="16" :sm="18" :md="20" :lg="22">
            <el-image
              style="width: 150px; height: 50px"
              :src="require('@/assets/images/shopGPT_logo_noBG_banner.png')">
            </el-image>
          </el-col>
          <el-col :xs="4" :sm="3" :md="2" :lg="1" class="language-icon">
            <el-dropdown>
              <el-image
              style="width: 35px; height: 35px"
              :src="require('@/assets/images/language_icon_144262.png')">
            </el-image>
              <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <el-button @click="changeLanguage('English')">English</el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button @click="changeLanguage('Simplified_Chinese')">中文</el-button>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
            </el-dropdown>
          </el-col>
          <el-col :xs="4" :sm="3" :md="2" :lg="1" class="google-login">
            <el-dropdown>
              <el-avatar v-if="userPicture" :src="userPicture" />
              <el-button v-else size="large" :icon=Avatar circle />
              <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <!-- <el-button @click="login"></el-button> -->
                  <el-image style="width: 160px; height: 40px" :src="require('@/assets/images/btn_google_signin.png')" :fit="contain" @click="login" />
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button @click="gLogout">{{$t('Log Out')}}</el-button>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
            </el-dropdown>
          </el-col>
        </el-row>
      </el-header>
      <el-main class="el-main" v-loading="loading" :element-loading-text="$t('Thinking...')">
        <el-row :gutter="20" justify="center" class="search-form">
          <el-col ::xs="24" :sm="16" :md="12" :lg="8">
            <el-button round @click="fillInputbox($event)">{{$t('Just moved, fill my living room')}}</el-button>
            <el-button round @click="fillInputbox($event)">{{$t('Fisrt day at college')}}</el-button>
            <el-button round @click="fillInputbox($event)">{{$t('Going camping this weekend')}}</el-button>
            <el-dropdown>
              <el-button primary>{{$t('more')}}<el-icon><arrow-down /></el-icon></el-button>
              <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <el-button round @click="fillInputbox($event)">{{$t('Hosting a birthday party')}}</el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button round @click="fillInputbox($event)">{{$t('Need office supplies')}}</el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button round @click="fillInputbox($event)">{{$t('Expecting a cat')}}</el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button round @click="fillInputbox($event)">{{$t('Daily hair care set')}}</el-button>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
            </el-dropdown>
          </el-col>
        </el-row>
        <el-row :gutter="20" justify="center" class="search-form">
          <el-col ::xs="24" :sm="16" :md="12" :lg="8">
            <el-input
              v-model="userInputInputbox"
              :autosize="{ minRows: 3, maxRows: 10 }"
              type="textarea"
              :placeholder="$t('what\'s in your mind')"
            /> 
          </el-col>
        </el-row>
        <el-row :gutter="20" justify="center" class="search-form">
          <el-col :xs="24" :sm="16" :md="12" :lg="8" class="generate-button">
              <el-button type="info" plain @click="generateEssentials">{{$t('Generate List of Essentials')}}</el-button>
          </el-col>
        </el-row>
        <el-row :gutter="20" justify="center" class="card-container">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-card shadow="hover" class="card">
              <el-card v-if="store.state.generateListResults.itemList.length === 0">
                    <el-image :src="defaultListImage" fit="cover"/>
              </el-card>
              <el-button 
                round 
                v-for="(item, index) in store.state.generateListResults.itemList.slice(0, 5)" 
                :key="'first-' + index"
                @click="setItemQuery($event)"
              >
                {{ item }}
              </el-button>
              <el-dropdown v-if="store.state.generateListResults.itemList.length > 5">
                <el-button primary>{{$t('more')}}<el-icon><arrow-down /></el-icon></el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item 
                      v-for="(item, index) in store.state.generateListResults.itemList.slice(5)" 
                      :key="'rest-' + index"
                    >
                      <el-button round @click="setItemQuery($event)">{{ item }}</el-button>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" justify="center" class="card-container" v-if="store.state.userSearchHistory.length != 0">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-card shadow="hover" class="card">
              <el-button 
                round 
                v-for="(item, index) in store.state.userSearchHistory.searchHistory" :key="index"
                @click="setItemQuery($event)"
              >
                {{ item['search_query'] }}
              </el-button>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" justify="center" class="search-form">
          <el-col ::xs="24" :sm="16" :md="12" :lg="8">
            <SearchForm @keydown.enter.prevent @submit="initialSubmit($event)" />
          </el-col>
        </el-row>
    <el-row :gutter="20" justify="center" class="card-container">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="choice in searchResults.choices" :key="choice.brand">
        <ChoiceCard :choice="choice" @ask-question="askQuestion" />
      </el-col>
    </el-row>
    <el-row :gutter="20" justify="center" class="fine-tune-section">
      <el-col :xs="24" :sm="18" :md="14" :lg="6">
        <el-card v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" shadow="hover" class="fine-tune-card">
          <QualityProperty v-for="quality in searchResults['qualities-properties']" :key="quality.name" :quality="quality" @option-selected="updateQuality" />
          <div class="price-inputs">
            <div class="price-input">
              <label for="min-price">{{$t('Min Price')}}: </label>
              <el-input id="min-price" v-model="minPrice"></el-input>
            </div>
            <div class="price-input">
              <label for="max-price">{{$t('Max Price')}}: </label>
              <el-input id="max-price" v-model="maxPrice"></el-input>
            </div>
          </div>
          <div class="fine-tune-button-div">
            <SearchButton v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" @submit="submitQualities" :label="$t('Fine Tune Choices!')" class="fine-tune-button" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    </el-main>
      <el-footer height="10px">
        <el-row :gutter="10" justify="center" class="footer-section">
          <el-col :xs="1" :sm="1" :md="6" :lg="6" class="centered-content"></el-col>
          <el-col :xs="8" :sm="8" :md="4" :lg="4" class="centered-content">
            <router-link to="/privacy-policy">
              <el-link type="info">{{$t('Privacy Policy')}}</el-link>
            </router-link>
          </el-col>
          <el-col :xs="5" :sm="5" :md="4" :lg="4" class="centered-content">
            <el-link type="info">ShopGPT&reg;</el-link>
          </el-col>
          <el-col :xs="9" :sm="9" :md="4" :lg="4" class="centered-content">
            <router-link to="/terms-of-service">
              <el-link type="info">{{$t('Terms of Service')}}</el-link>
            </router-link>
          </el-col>
          <el-col :xs="1" :sm="1" :md="6" :lg="6" class="centered-content"></el-col>
        </el-row>
      </el-footer>
    </el-container>
    </div>
  </template>
  
  <script setup>
import { ref, computed, reactive, inject } from 'vue'
import { useStore } from 'vuex'
// import { ElMessageBox } from 'element-plus'
import SearchForm from '../components/SearchForm.vue'
import ChoiceCard from '../components/ChoiceCard.vue'
import QualityProperty from '../components/QualityProperty.vue'
import SearchButton from '../components/SearchButton.vue'
import { googleLogout } from "vue3-google-login"
// import { decodeCredential } from 'vue3-google-login'
import { googleTokenLogin } from "vue3-google-login"
import { onMounted } from 'vue'
import apiService from '@/services/apiService'  // Import the apiService here

import defaultImage1_en from '@/assets/images/undraw_Web_search_re_efla.png';
import defaultImage2_en from '@/assets/images/undraw_Faq_re_31cw.png';
import defaultImage3_en from '@/assets/images/undraw_shopping_app_flsj.png';
import defaultImage1_zh from '@/assets/images/undraw_Search_app_flsj_zh.png';
import defaultImage2_zh from '@/assets/images/undraw_ask_app_flsj_zh.png';
import defaultImage3_zh from '@/assets/images/undraw_shopping_app_flsj_zh.png';
import defaultListImage from '@/assets/images/thinking.png';

import {
  Avatar, ArrowDown
} from '@element-plus/icons-vue'


// Vuex store
const store = useStore()

// Data
const globalState = inject('globalState')
let item_query = ref(null)
let selectedQualities = ref({})
let userInputInputbox = ref('')
let minPrice = ref('')
let maxPrice = ref('')
// let askResponse = ref(null)
let loading = computed(() => store.state.loading);
let userPicture = ref(null);
let defaultImage1 = ref(defaultImage1_en);
let defaultImage2 = ref(defaultImage2_en);
let defaultImage3 = ref(defaultImage3_en);

// initialize default choices
let defaultChoices = reactive([
  {
    default: true,
    image: defaultImage1,
    description: 'Find and compare items',
  },
  {
    default: true,
    description: 'Ask AI anything about the items',
    image: defaultImage2,
  },
  {
    default: true,
    description: 'Happy shopping!',
    image: defaultImage3,
  },
])
// Computed
let searchResults = computed(() => {
  return store.state.searchResults.choices.length ? store.state.searchResults : { choices: defaultChoices }
})


// Methods
const initialSubmit = (query) => {
  item_query.value = query;
  if (item_query.value != null) {
    loading.value = true;

    // check if user is logged in
    const storedUserData = localStorage.getItem('userData')
    let payload = { item_query: String(item_query.value) }

    if (storedUserData) {
      const userData = JSON.parse(storedUserData)
      payload.email = userData.email // add email to payload
    }

    store.dispatch('fetchSearchResults', payload)
    store.dispatch('fetchPropertiesResults', payload)
  }
}

const generateEssentials = () => {
  if (userInputInputbox.value != null && userInputInputbox.value != '') {
    loading.value = true;

    // check if user is logged in
    const storedUserData = localStorage.getItem('userData')
    let payload = { list_query: String(userInputInputbox.value) }

    if (storedUserData) {
      const userData = JSON.parse(storedUserData)
      payload.email = userData.email // add email to payload
    }

    store.dispatch('fetchGenerateListResults', payload)
  }
}

const submitQualities = () => {
    store.dispatch('fetchRefinedSearchResults', { target: searchResults.value.target, qualities: selectedQualities.value, minPrice: minPrice.value, maxPrice: maxPrice.value })
}

const updateQuality = (selectedQuality) => {
  selectedQualities.value = { ...selectedQualities.value, ...selectedQuality }
}

const askQuestion = (choice, question) => {
  store.dispatch('askQuestion', { choice: choice, question: String(question) })
}

const getUserData = async (accessToken) => {
  try {
    const response = await fetch(`https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=${accessToken}`);
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    const userData = await response.json();
    console.log("User data: ", userData);
    return userData;
  } catch (error) {
    console.error("Error fetching user data: ", error);
  }
}

const login = () => {
  googleTokenLogin().then((response) => {
    getUserData(response.access_token).then((data) => {
      userPicture.value = data.picture
      // Save user data to local storage
      const userData = { ...response, picture: data.picture, email: data.email }
      localStorage.setItem('userData', JSON.stringify(userData))

      // send email to backend
      apiService.saveEmail(data.email)  // Use apiService to save the email here
        .then(response => console.log(response))
        .catch(error => console.error(error))

      store.dispatch('fetchUserSearchHistory', data.email) 
    })
  })
}


const gLogout = () => {
  // your logout logics
  googleLogout()
  // Clear user data from local storage
  localStorage.removeItem('userData')
  // Reset userPicture
  userPicture.value = null
  console.log("logout")
}

const changeLanguage = (language) => {
  store.commit('setLanguage', language);
  if(language == 'English'){
    defaultChoices[0].image = defaultImage1_en;
    defaultChoices[1].image = defaultImage2_en;
    defaultChoices[2].image = defaultImage3_en;
  }
  if(language == 'Simplified_Chinese'){
    defaultChoices[0].image = defaultImage1_zh;
    defaultChoices[1].image = defaultImage2_zh;
    defaultChoices[2].image = defaultImage3_zh;
  }
}

const fillInputbox = (event) => {
      userInputInputbox.value = event.target.innerText;
}

const setItemQuery = (event) => {
  console.log("setItemQuery", event.target.innerText)
  globalState.itemQuery = event.target.innerText;
}    


onMounted(() => {
  // Check local storage for user data
  const storedUserData = localStorage.getItem('userData')

  if (storedUserData) {
    // Parse the user data and update userPicture
    const userData = JSON.parse(storedUserData)
    userPicture.value = userData.picture
    store.dispatch('fetchUserSearchHistory', userData.email)    
  }
})


</script>

<style scoped>
  /* .imgBK {
  background-image: url("https://www.usatoday.com/gcdn/-mm-/b2b05a4ab25f4fca0316459e1c7404c537a89702/c=0-0-1365-768/local/-/media/2022/03/16/USATODAY/usatsports/imageForEntry5-ODq.jpg?width=1365&height=768&fit=crop&format=pjpg&auto=webp");
  background-repeat: no-repeat;
  background-size: cover; 
  background-position: center; 
  } */

  .card-container{
    background-color: honeydew;
    padding-top: 20px;
    padding-bottom: 20px;
  }
  .search-form{
    background-color: honeydew;
    padding-top: 5px;
    padding-bottom: 5px;
  }

  .fine-tune-section{
    background-color: honeydew;
    padding-top: 20px;
    padding-bottom: 20px;
  }

  .fine-tune-card{
    border-radius: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .fine-tune-button{
    margin-top: 10px;
  }

  .fine-tune-button-div{
    text-align: center;
  }

  .centered-content{
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 5px;
  }

  .el-container{
    background-color: #f5c4c9;
    padding-top: 10px;
    padding-bottom: 20px;
  }

  .el-main{
    padding-left: 0%;
    padding-right: 0.4%;
    padding-top: 0;
    padding-bottom: 0%;
  }

  .google-login{
    padding-top: 5px;
  }

  .language-icon{
    padding-top: 7px;
  }
  
  .generate-button{
    text-align: center;
  }

</style>

  