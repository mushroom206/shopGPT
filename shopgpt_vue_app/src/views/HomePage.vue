<template>
  <div class="common-layout">
    <el-container class="el-container">
      <el-header class="el-header">
        <el-row :gutter="20" justify="center">
          <el-col :xs="20" :sm="21" :md="22" :lg="23">
            <el-image
              style="width: 150px; height: 50px"
              :src="require('@/assets/images/shopGPT_logo_noBG_banner.png')"
              :fit="contain" class="logo">
            </el-image>
          </el-col>
          <el-col :xs="4" :sm="3" :md="2" :lg="1" class="google-login">
            <el-dropdown>
              <el-avatar v-if="userPicture" :src="userPicture" />
              <el-button v-else size="large" :icon=Avatar circle />
              <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                    <el-button @click="login">Log in by Gmail</el-button>
                </el-dropdown-item>
                <el-dropdown-item>
                  <el-button @click="gLogout">Log Out</el-button>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
            </el-dropdown>
          </el-col>
        </el-row>
      </el-header>
      <el-main class="el-main" v-loading="loading" element-loading-text="Thinking...">
        <el-row :gutter="20" justify="center" class="search-form">
          <el-col ::xs="24" :sm="16" :md="12" :lg="8">
            <SearchForm @submit="initialSubmit($event)" />
          </el-col>
        </el-row>
    <el-row :gutter="20" justify="center" class="card-container">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="choice in searchResults.choices" :key="choice.brand">
        <ChoiceCard :choice="choice" @ask-response="handleAskResponse" />
      </el-col>
    </el-row>
    <el-row :gutter="20" justify="center" class="fine-tune-section">
      <el-col :xs="24" :sm="18" :md="14" :lg="6">
        <el-card v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" shadow="hover" class="fine-tune-card">
          <QualityProperty v-for="quality in searchResults['qualities-properties']" :key="quality.name" :quality="quality" @option-selected="updateQuality" />
          <SearchButton v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" @submit="submitQualities" label="Fine Tune Choices!" class="fine-tune-button" />
        </el-card>
      </el-col>
    </el-row>
    </el-main>
      <el-footer height="10px">
        <el-row gutter="10" justify="center" class="footer-section">
          <el-col :xs="1" :sm="1" :md="6" :lg="6" class="centered-content"></el-col>
          <el-col :xs="8" :sm="8" :md="4" :lg="4" class="centered-content">
            <router-link to="/privacy-policy">
              <el-link type="info">Privacy Policy</el-link>
            </router-link>
          </el-col>
          <el-col :xs="5" :sm="5" :md="4" :lg="4" class="centered-content">
            <el-link type="info">ShopGPT&reg;</el-link>
          </el-col>
          <el-col :xs="9" :sm="9" :md="4" :lg="4" class="centered-content">
            <router-link to="/terms-of-service">
              <el-link type="info">Terms of Service</el-link>
            </router-link>
          </el-col>
          <el-col :xs="1" :sm="1" :md="6" :lg="6" class="centered-content"></el-col>
        </el-row>
      </el-footer>
    </el-container>
    </div>
  </template>
  
  <script setup>
import { ref, computed, reactive } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import SearchForm from '../components/SearchForm.vue'
import ChoiceCard from '../components/ChoiceCard.vue'
import QualityProperty from '../components/QualityProperty.vue'
import SearchButton from '../components/SearchButton.vue'
import { googleLogout } from "vue3-google-login"
// import { decodeCredential } from 'vue3-google-login'
import { googleTokenLogin } from "vue3-google-login"
import { onMounted } from 'vue'
import apiService from '@/services/apiService'  // Import the apiService here

import defaultImage1 from '@/assets/images/undraw_Web_search_re_efla.png';
import defaultImage2 from '@/assets/images/undraw_Faq_re_31cw.png';
import defaultImage3 from '@/assets/images/undraw_shopping_app_flsj.png';

import {
  Avatar,
} from '@element-plus/icons-vue'


// Vuex store
const store = useStore()

// Data
let item_query = ref(null)
let selectedQualities = ref({})
let askResponse = ref(null)
let loading = computed(() => store.state.loading);
let userPicture = ref(null);

// Initialize default choices
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
    let payload = { item_query: item_query.value }

    if (storedUserData) {
      const userData = JSON.parse(storedUserData)
      payload.email = userData.email // add email to payload
    }

    store.dispatch('fetchSearchResults', payload)
  }
}

const submitQualities = () => {
    store.dispatch('fetchRefinedSearchResults', { target: searchResults.value.target, qualities: selectedQualities.value })
}

const updateQuality = (selectedQuality) => {
  selectedQualities.value = { ...selectedQualities.value, ...selectedQuality }
}

const handleAskResponse = (response) => {
  let parsedResponse
  try {
    parsedResponse = JSON.parse(response)
  } catch (e) {
    console.error('Error parsing response:', e)
    parsedResponse = response  // Use the original response if parsing fails
  }
  askResponse.value = parsedResponse
  open(askResponse.value)
}

const open = (askResponse) => {
  ElMessageBox.alert(askResponse.answer, 'I\'m Back', {
    // if you want to disable its autofocus
    // autofocus: false,
    confirmButtonText: 'OK',
    callback: (action) => {  // Remove type annotation here
      ElMessage({
        type: 'info',
        message: `action: ${action}`,
      })
    },
  })
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


onMounted(() => {
  // Check local storage for user data
  const storedUserData = localStorage.getItem('userData')

  if (storedUserData) {
    // Parse the user data and update userPicture
    const userData = JSON.parse(storedUserData)
    userPicture.value = userData.picture
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
    padding-top: 20px;
    padding-bottom: 20px;
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
  
</style>

  