<template>
  <div class="common-layout">
    <el-container class="el-container">
      <el-header class="el-header">
        <el-row :gutter="20" justify="center">
          <el-col :span="6">
            <el-image
              style="width: 150px; height: 50px"
              :src="require('@/assets/images/shopGPT_logo_noBG_banner.png')"
              :fit="contain" class="logo">
            </el-image>
          </el-col>
          <el-col :span="6"></el-col>
          <el-col :span="6"></el-col>
          <el-col :span="6" :push="4">
            <GoogleLogin :callback="callback" class="google-login"/>
          </el-col>
        </el-row>
      </el-header>
      <el-main class="el-main" v-loading="loading" element-loading-text="Loading...">
        <el-row :gutter="20" justify="center" class="search-form">
          <el-col :span="8">
            <SearchForm @submit="initialSubmit" />
          </el-col>
        </el-row>
    <el-row :gutter="20" justify="center" class="card-container">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="choice in searchResults.choices" :key="choice.brand">
        <ChoiceCard :choice="choice" @ask-response="handleAskResponse" />
      </el-col>
    </el-row>
    <el-row :gutter="20" justify="center" class="fine-tune-section">
      <el-col :span="6">
        <el-card v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" shadow="hover" class="fine-tune-card">
          <!-- <h2>Things to consider when shopping {{ searchResults.target }}</h2> -->
          <QualityProperty v-for="quality in searchResults['qualities-properties']" :key="quality.name" :quality="quality" @option-selected="updateQuality" />
          <SearchButton v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" @submit="submitQualities" label="Fine Tune Choices!" class="fine-tune-button" />
        </el-card>
      </el-col>
    </el-row>
    </el-main>
      <!-- <el-footer>Footer</el-footer> -->
    </el-container>
    </div>
  </template>
  
  <script setup>
import { ref, computed, reactive } from 'vue'
import { useStore } from 'vuex'
import { decodeCredential } from 'vue3-google-login'
import { ElMessage, ElMessageBox } from 'element-plus'
import SearchForm from '../components/SearchForm.vue'
import ChoiceCard from '../components/ChoiceCard.vue'
import QualityProperty from '../components/QualityProperty.vue'
import SearchButton from '../components/SearchButton.vue'

import defaultImage1 from '@/assets/images/undraw_Web_search_re_efla.png';
import defaultImage2 from '@/assets/images/undraw_Faq_re_31cw.png';
import defaultImage3 from '@/assets/images/undraw_shopping_app_flsj.png';

// Vuex store
const store = useStore()

// Data
let item_query = ref(null)
let selectedQualities = ref({})
let askResponse = ref(null)
let loading = computed(() => store.state.loading);

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
const initialSubmit = () => {
  if (item_query.value != null) {
    console.log('initialSubmit is called with item_query: ', item_query.value)
    loading.value = true;
    store.dispatch('fetchSearchResults', item_query.value)
      .then(() => {
        loading.value = false;
      })
      .catch(() => {
        loading.value = false;
      });
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

const callback = (response) => {
  // decodeCredential will retrive the JWT payload from the credential
  const userData = decodeCredential(response.credential)
  console.log("Handle the userData", userData)
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

  .el-container{
    background-color: #f5c4c9;
    padding-top: 10px;
    padding-bottom: 20px;
  }

  .el-main{
    padding-left: 0%;
    padding-right: 0.4%;
    padding-top: 0;
  }

  .google-login{
    padding-top: 5px;
  }
  
</style>

  