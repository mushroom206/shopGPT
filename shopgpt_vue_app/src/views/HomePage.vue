<template>
  <div class="common-layout">
    <el-container class="el-container">
      <el-header height="50px" class="el-header">
        <el-row :gutter="20" justify="center">
          <el-col :xs="15" :sm="15" :md="18" :lg="21">
            <el-image
              style="width: 120px; height: 40px"
              :src="require('@/assets/images/shopGPT_logo_noBG_banner.png')"
              @click="goToHomePage"
            >
            </el-image>
          </el-col>
          <el-col :xs="3" :sm="3" :md="2" :lg="1" class="cart-icon">
            <el-dropdown ref="cart">
              <el-button size="medium" circle>
                  <!-- <el-image
                    style="width: 25px; height: 25px"
                    :src="require('@/assets/images/language_icon_144262.png')">
                  </el-image> -->
                <el-icon :size="15">
                  <ShoppingCart />
                </el-icon>  
              </el-button>
              <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-if="cartDropdownItems.length == 0">cart is empty</el-dropdown-item>
                <el-scrollbar max-height="50vh">
                      <el-dropdown-item v-for="(item, index) in cartDropdownItems" :key="index">
                        <el-card :body-style="{ padding: '15px' }">
                          <el-badge :value=item.price class="item" type="warning">
                            <el-image
                              style="width: 50px; height: 50px"
                              :src="item.image_urls"
                              :title="item.target"
                              fit="contain"
                            />
                          </el-badge>
                          <el-input-number class="el-input-number" :min="1" :max="10" size="small" v-model="item.quantity" @click.prevent.self/>
                          <el-icon class="el-icon-delete" @click="deleteCartItem(item.target, index)" @click.prevent.self>
                            <Delete />
                          </el-icon>
                          <div style="width: 250px; white-space: normal;">{{ item.target }}</div>
                        </el-card>
                      </el-dropdown-item>
                </el-scrollbar>
                <el-dropdown-item v-if="cartDropdownItems.length != 0" class="check-out-button-dropdown-item">
                  <el-button type="primary" @click="checkoutOnAmazon">{{$t('Check out on Amazon')}}</el-button>                
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
            </el-dropdown>
          </el-col>
          <el-col :xs="3" :sm="3" :md="2" :lg="1" class="language-icon">
            <el-dropdown ref="language_dropdown">
              <el-button size="medium" circle>
                  <!-- <el-image
                    style="width: 25px; height: 25px"
                    :src="require('@/assets/images/language_icon_144262.png')">
                  </el-image> -->
                <el-icon :size="15">
                  <Tools />
                </el-icon>  
              </el-button>
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
          <el-col :xs="3" :sm="3" :md="2" :lg="1" class="google-login">
            <el-dropdown>
              <el-avatar v-if="userPicture" :src="userPicture" :size="30"/>
              <el-button v-else size="medium" circle>
                <el-icon :size="15">
                  <Avatar />
                </el-icon>
              </el-button>
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
        <!-- <el-row :gutter="20" justify="center" class="search-form" v-show="isVisible">
          <el-col ::xs="24" :sm="16" :md="12" :lg="8">
            <el-card shadow="hover" class="card" :body-style="{ padding: '5px' }">
              <div style="margin-bottom: 5px;"><el-tag type="warning" effect="dark" round>{{$t('Your Activity')}}:</el-tag></div>
              <el-button round @click="fillInputbox($event)">{{$t('Just moved, fill my living room')}}</el-button>
              <el-button round @click="fillInputbox($event)">{{$t('Fisrt day at college')}}</el-button>
              <el-button round @click="fillInputbox($event)">{{$t('Need office supplies')}}</el-button>
              <el-button round @click="fillInputbox($event)">{{$t('Workout in Gym')}}</el-button>
              <el-button round @click="fillInputbox($event)">{{$t('Going camping this weekend')}}</el-button>
              <el-dropdown>
                <el-button style="margin-left: 5px;" primary>{{$t('more')}}<el-icon><arrow-down /></el-icon></el-button>
                <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>
                    <el-button round @click="fillInputbox($event)">{{$t('Hosting a birthday party')}}</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button round @click="fillInputbox($event)">{{$t('First time making Pasta')}}</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button round @click="fillInputbox($event)">{{$t('Expecting a cat')}}</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button round @click="fillInputbox($event)">{{$t('Daily hair care set')}}</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button round @click="fillInputbox($event)">{{$t('Facial care set')}}</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button round @click="fillInputbox($event)">{{$t('BBQ weekend')}}</el-button>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <el-button round @click="fillInputbox($event)">{{$t('Household products')}}</el-button>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
              </el-dropdown>
            </el-card>
          </el-col>
        </el-row> -->
        <el-row :gutter="20" justify="center" class="search-form" v-show="isVisible">
          <el-col ::xs="24" :sm="16" :md="12" :lg="8">
            <el-input v-model="userInputInputbox" :placeholder="$t('looking for something?')"  clearable size="large" class="my-input">
              <template #append>
                <el-button type="info" plain @click="generateEssentials">{{$t('Best Deal')}}</el-button>
              </template>
            </el-input>
          </el-col>
        </el-row>
        <el-row :gutter="20" justify="center" class="card-container" ref="choice_card_container">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-card shadow="hover" class="card" :body-style="{ padding: '5px' }" v-show="isVisible || store.state.generateListResults.itemList.length !== 0">
              <!-- <div v-if="store.state.generateListResults.itemList.length !== 0" style="margin-bottom: 5px;"><el-tag type="warning" effect="dark" round>{{$t('Essentials')}}:</el-tag></div> -->
              <el-card v-if="store.state.generateListResults.itemList.length === 0">
                    <el-image :src="defaultListImage" fit="cover"/>
              </el-card>
              <!-- <el-button 
                round 
                v-for="(item, index) in store.state.generateListResults.itemList.slice(0, 5)" 
                :key="'first-' + index"
                @click="setItemQuery($event)"
              > -->
              <!-- <el-badge style="margin: 7px;" value="X" v-for="(item) in store.state.listResults" :key="item.target" @click="deleteFromList(item.target)"> -->
                <el-button 
                  v-for="(item) in store.state.listResults" :key="item.target"
                  style="margin: 7px;"
                  round 
                  @click.stop="setItemQuery($event)"
                >
                  {{ item.target }}
                </el-button>
                <el-badge 
                v-if="store.state.generateListResults.itemList.length !== 0"
                style="margin: 7px;" value="+" @click="moreItems"
                >
                <el-button
                  round 
                  >
                  more
                </el-button>
              </el-badge>
              <!-- </el-badge> -->
              <!-- <div class="confirm-list-button">
                <el-button style="margin-top: 5px;" v-if="Object.keys(store.state.listResults).length !== 0"
                type="primary" @click="confirmList">{{$t('Confirm List and View Items')}}</el-button>
              </div> -->
              <!-- <el-dropdown v-if="store.state.generateListResults.itemList.length > 5">
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
              </el-dropdown> -->
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" justify="center" class="card-container" v-if="store.state.userSearchHistory.searchHistory && store.state.userSearchHistory.searchHistory
.length != 0">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-card shadow="hover" class="card" :body-style="{ padding: '10px' }">
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
        <!-- <el-row :gutter="20" justify="center" class="search-form" v-show="isVisible">
          <el-col ::xs="24" :sm="16" :md="12" :lg="8">
            <SearchForm @keydown.enter.prevent @submit="initialSubmit($event)" />
          </el-col>
        </el-row> -->
        <!-- <el-row :gutter="20" justify="center" class="expand-button" v-if="searchResults.target"> -->
          <!-- <el-button @click="toggleVisibility" size="medium">
            <template v-if="isVisible">
              <el-icon :size="15">
                <Remove />
              </el-icon>
              <span>{{$t('Hide Search Menu')}}</span>
            </template>

            <template v-else>
              <el-icon :size="15">
                <CirclePlus />
              </el-icon>
              <span>{{$t('Show Search Menu')}}</span>
            </template>
          </el-button> -->
          <!-- <el-button size="medium" @click="showShoppingCart">
              <span>{{$t('Shopping Cart')}}</span>
              <el-icon :size="15">
                <ShoppingCart />
              </el-icon>
          </el-button>
        </el-row> -->
        <!-- <el-row :gutter="20" justify="center" class="next-button" ref="next_container">
          <el-button-group>
            <el-button 
              type="primary" 
              :icon="ArrowLeft"
              @click="preItem" 
              v-if="store.state.listResults[store.state.searchResults.target] 
              && store.state.listResults[store.state.searchResults.target].pre
              && (store.state.listResults[store.state.listResults[store.state.searchResults.target].pre].choices.length != 0 
                || store.state.listResults[store.state.listResults[store.state.searchResults.target].pre].empty)"
            >
              {{store.state.listResults[store.state.searchResults.target].pre}}
            </el-button>
            <el-button 
              type="primary" 
              v-else-if="store.state.listResults[store.state.searchResults.target]
                      && store.state.listResults[store.state.searchResults.target].pre"
            >
            <el-icon class="el-icon--right"><ArrowLeft /></el-icon>
            {{$t('Pre item loading...')}}
            </el-button>
            <el-button 
              type="primary" 
              @click="nextItem" 
              v-if="store.state.listResults[store.state.searchResults.target] 
              && store.state.listResults[store.state.searchResults.target].next 
              && (store.state.listResults[store.state.listResults[store.state.searchResults.target].next].choices.length != 0 
                || store.state.listResults[store.state.listResults[store.state.searchResults.target].next].empty)"
            >
              {{store.state.listResults[store.state.searchResults.target].next}}
              <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
            <el-button 
              type="primary" 
              v-else-if="store.state.listResults[store.state.searchResults.target]
                      && store.state.listResults[store.state.searchResults.target].next"
            >
            {{$t('Next item loading...')}}
              <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
          </el-button-group>
        </el-row> -->
    <el-row :gutter="20" justify="center" class="card-container">
      <el-scrollbar>
        <div class="scrollbar-flex-content">
          <div style="margin-left: 5px; max-width: 95vw;" v-for="choice in searchResults.choices" :key="choice.target">
            <ChoiceCard :choice="choice" @ask-question="askQuestion" @add-to-cart="addToCart" @find-similar="findSimilar"  @find-variants="findVariants"/>
          </div>
        </div>
      </el-scrollbar>
    </el-row>
    <el-row :gutter="20" justify="center" class="next-button">
      <el-button-group>
            <el-button 
              type="primary" 
              :icon="ArrowLeft"
              @click="preItem" 
              v-if="store.state.listResults[store.state.searchResults.target] 
              && store.state.listResults[store.state.searchResults.target].pre
              && (store.state.listResults[store.state.listResults[store.state.searchResults.target].pre].choices.length != 0 
                || store.state.listResults[store.state.listResults[store.state.searchResults.target].pre].empty)"
            >
              {{store.state.listResults[store.state.searchResults.target].pre}}
            </el-button>
            <el-button 
              type="primary" 
              v-else-if="store.state.listResults[store.state.searchResults.target]
                      && store.state.listResults[store.state.searchResults.target].pre"
            >
            {{$t('Pre item loading...')}}
              <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
            <el-button 
              type="primary"
              @click="nextItem" 
              v-if="store.state.listResults[store.state.searchResults.target] 
              && store.state.listResults[store.state.searchResults.target].next
              && store.state.listResults[store.state.listResults[store.state.searchResults.target].next].choices.length != 0"
            >
              {{store.state.listResults[store.state.searchResults.target].next}}
              <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
            <el-button 
              type="primary" 
              v-else-if="store.state.listResults[store.state.searchResults.target]
                      && store.state.listResults[store.state.searchResults.target].next"
            >
            {{$t('Next item loading...')}}
              <el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
          <el-button v-else size="medium" @click="showShoppingCart">
              <span>{{$t('Shopping Cart')}}</span>
              <el-icon :size="15">
                <ShoppingCart />
              </el-icon>
          </el-button>
          </el-button-group>
        </el-row>
        <!-- <el-row :gutter="20" justify="center" class="expand-button" v-if="searchResults.target"> -->
          <!-- <el-button @click="toggleVisibility" size="medium">
            <template v-if="isVisible">
              <el-icon :size="15">
                <Remove />
              </el-icon>
              <span>{{$t('Hide Search Menu')}}</span>
            </template>

            <template v-else>
              <el-icon :size="15">
                <CirclePlus />
              </el-icon>
              <span>{{$t('Show Search Menu')}}</span>
            </template>
          </el-button> -->
          <!-- <el-button size="medium" @click="showShoppingCart">
              <span>{{$t('Shopping Cart')}}</span>
              <el-icon :size="15">
                <ShoppingCart />
              </el-icon>
          </el-button>
        </el-row>     -->
    <el-row :gutter="20" justify="center" class="fine-tune-section">
      <el-col :xs="24" :sm="18" :md="10" :lg="8">
        <el-card :body-style="{ padding: '0px' }" v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" shadow="hover" class="fine-tune-card">
          <QualityProperty v-for="quality in searchResults['qualities-properties']" :key="quality.name" :quality="quality" @option-selected="updateQuality" />
            <div class="price-inputs">
              <label for="min-price">{{$t('Min Price')}}: </label>
              <el-input id="min-price" v-model="minPrice"></el-input>
              <label for="max-price">{{$t('Max Price')}}: </label>
              <el-input id="max-price" v-model="maxPrice"></el-input>
            </div>
          <div class="fine-tune-button-div">
            <SearchButton v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" @submit="submitQualities" :label="$t('Fine Tune Choices!')" class="fine-tune-button" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    <template>
      <div>
        <form id="amazon-form" method="GET" action="https://www.amazon.com/gp/aws/cart/add.html" style="display:none" target="_blank">
          <input type="hidden" name="AssociateTag" value="rei042-20" />
          <div v-for="(item, index) in cartDropdownItems" :key="index">
            <input type="hidden" :name="`ASIN.${index+1}`" :value="item.asin" />
            <input type="hidden" :name="`Quantity.${index+1}`" :value="item.quantity" />
          </div>
        </form>
      </div>
    </template>
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
    <div class="bot-search-bar" v-if="!isVisible">
      <el-input
      v-model="userInputInputbox_bot"
      size="large"
    >
    <template #append>
        <el-button :icon="Search" @click="generateEssentials"/>
      </template>
    </el-input>
    <el-button size="large" @click="showShoppingCart" style="margin-right: 5px;" >
      <el-icon :size="20">
        <ShoppingCart />
      </el-icon>
    </el-button>
    </div>
    </div>
  </template>
  
<script setup>
import { ref, computed, reactive, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
// import SearchForm from '../components/SearchForm.vue'
import ChoiceCard from '../components/ChoiceCard.vue'
import QualityProperty from '../components/QualityProperty.vue'
import SearchButton from '../components/SearchButton.vue'
import { googleLogout } from "vue3-google-login"
// import { decodeCredential } from 'vue3-google-login'
import { googleTokenLogin } from "vue3-google-login"
import { onMounted } from 'vue'
import apiService from '@/services/apiService'  // Import the apiService here

import defaultImage1_en from '@/assets/images/undraw_Web_search_re_efla.png';
// import defaultImage2_en from '@/assets/images/undraw_Faq_re_31cw.png';
import defaultImage3_en from '@/assets/images/undraw_shopping_app_flsj.png';
import defaultImage1_zh from '@/assets/images/undraw_Search_app_flsj_zh.png';
// import defaultImage2_zh from '@/assets/images/undraw_ask_app_flsj_zh.png';
import defaultImage3_zh from '@/assets/images/undraw_shopping_app_flsj_zh.png';
import defaultListImage_en from '@/assets/images/thinking_en.png';
import defaultListImage_zh from '@/assets/images/thinking_zh.png';

import {
  Avatar, Tools, ShoppingCart, Delete, Search, ArrowRight, ArrowLeft
} from '@element-plus/icons-vue'


// Vuex store
const store = useStore()

// Data
const globalState = inject('globalState')
let item_query = ref(null)
let selectedQualities = ref({})
let userInputInputbox = ref('')
let userInputInputbox_bot = ref('')
let minPrice = ref('')
let maxPrice = ref('')
let choice_card_container = ref(null);
// let next_container = ref(null);
let cartDropdownItems= ref([]);
let cart= ref(null);
let language_dropdown= ref(null);
// let askResponse = ref(null)
let loading = computed(() => store.state.loading);
let isVisible = ref(true);
let userPicture = ref(null);
let defaultImage1 = ref(defaultImage1_en);
// let defaultImage2 = ref(defaultImage2_en);
let defaultImage3 = ref(defaultImage3_en);

// initialize default choices
let defaultChoices = reactive([
  {
    default: true,
    image: defaultImage1,
    description: 'Find and compare items',
  },
  // {
  //   default: true,
  //   description: 'Ask AI anything about the items',
  //   image: defaultImage2,
  // },
  {
    default: true,
    description: 'Happy shopping!',
    image: defaultImage3,
  },
])

let defaultListImage = ref(defaultListImage_en)
// Computed
let searchResults = computed(() => {
  return store.state.searchResults.choices.length ? store.state.searchResults : { choices: defaultChoices }
})

const router = useRouter()

// Methods
const initialSubmit = (query) => {
  closeLanguage()
  item_query.value = query;
  if (item_query.value != null) {
    // check if user is logged in
    const storedUserData = localStorage.getItem('userData')
    let payload = { item_query: String(item_query.value) }

    if (storedUserData) {
      const userData = JSON.parse(storedUserData)
      payload.email = userData.email // add email to payload
    }

    payload.loading_flag = true;
    payload.commit_flag = true;

    store.dispatch('fetchSearchResults', payload)

    // Scroll to the position
    window.scrollTo({ top: choice_card_container.value.$el.offsetTop, behavior: 'smooth' });
    isVisible.value = false;

  setTimeout(() => {  
    if(store.state.listResults[item_query.value]
      && store.state.listResults[item_query.value].next 
      && store.state.listResults[store.state.listResults[item_query.value].next].choices.length == 0)
      {
        const storedUserData = localStorage.getItem('userData')
          let payload = { item_query: store.state.listResults[item_query.value].next }

          if (storedUserData) {
            const userData = JSON.parse(storedUserData)
            payload.email = userData.email // add email to payload
          }

          payload.loading_flag = false;
          payload.commit_flag = false;
          store.dispatch('fetchSearchResults', payload)
      }
    }, 2000);  

    setTimeout(() => {
    if(store.state.listResults[item_query.value]
      && store.state.listResults[item_query.value].pre 
      && store.state.listResults[store.state.listResults[item_query.value].pre].choices.length == 0)
      {
        const storedUserData = localStorage.getItem('userData')
          let payload = { item_query: store.state.listResults[item_query.value].pre }

          if (storedUserData) {
            const userData = JSON.parse(storedUserData)
            payload.email = userData.email // add email to payload
          }

          payload.loading_flag = false;
          payload.commit_flag = false;
          store.dispatch('fetchSearchResults', payload)
      }
    }, 4000);    
  }
}

const generateEssentials = () => {
  if(userInputInputbox_bot.value){
    userInputInputbox.value = userInputInputbox_bot.value
  }
  closeLanguage()
  if (userInputInputbox.value != null && userInputInputbox.value != '') {
    loading.value = true;

    // check if user is logged in
    const storedUserData = localStorage.getItem('userData')
    let payload = { list_query: String(userInputInputbox.value) }

    if (storedUserData) {
      const userData = JSON.parse(storedUserData)
      payload.email = userData.email // add email to payload
    }

    store.dispatch('fetchGenerateListResults', payload).then(() => {
      globalState.itemQuery = store.state.generateListResults.itemList[0]
    })

    isVisible.value = false;
  }
}

const moreItems = () => {
    store.dispatch('fetchMoreItems')
}

const preItem = () => {
  globalState.itemQuery = store.state.listResults[store.state.searchResults.target].pre
  store.dispatch('setPreItem', store.state.listResults[store.state.searchResults.target].pre)
  if(store.state.listResults[store.state.searchResults.target].pre 
  && store.state.listResults[store.state.listResults[store.state.searchResults.target].pre].choices.length == 0){
    const storedUserData = localStorage.getItem('userData')
      let payload = { item_query: store.state.listResults[store.state.searchResults.target].pre }

      if (storedUserData) {
        const userData = JSON.parse(storedUserData)
        payload.email = userData.email // add email to payload
      }

      payload.loading_flag = false;
      payload.commit_flag = false;

      store.dispatch('fetchSearchResults', payload)
  }  
    // Scroll to the position
  window.scrollTo({ top: choice_card_container.value.$el.offsetTop, behavior: 'smooth' });
}

const nextItem = () => {
  globalState.itemQuery = store.state.listResults[store.state.searchResults.target].next
  store.dispatch('setNextItem', store.state.listResults[store.state.searchResults.target].next)
  if(store.state.listResults[store.state.searchResults.target].next 
  && store.state.listResults[store.state.listResults[store.state.searchResults.target].next].choices.length == 0){
    const storedUserData = localStorage.getItem('userData')
      let payload = { item_query: store.state.listResults[store.state.searchResults.target].next }

      if (storedUserData) {
        const userData = JSON.parse(storedUserData)
        payload.email = userData.email // add email to payload
      }

      payload.loading_flag = false;
      payload.commit_flag = false;

      store.dispatch('fetchSearchResults', payload)
  }  
    // Scroll to the position
    window.scrollTo({ top: choice_card_container.value.$el.offsetTop, behavior: 'smooth' });
}

const submitQualities = () => {
    store.dispatch('fetchRefinedSearchResults', { target: searchResults.value.target, qualities: selectedQualities.value, minPrice: minPrice.value, maxPrice: maxPrice.value })
    // Scroll to the position
    window.scrollTo({ top: choice_card_container.value.$el.offsetTop, behavior: 'smooth' });
}

const updateQuality = (selectedQuality) => {
  selectedQualities.value = { ...selectedQualities.value, ...selectedQuality }
}

const askQuestion = (choice, question) => {
  store.dispatch('askQuestion', { choice: choice, question: String(question) })
}

const findSimilar = (target) => {
  initialSubmit(store.state.searchResults.target + " " + target)
}

const findVariants = (asin) => {
  store.dispatch('startLoading')
  apiService.getVariants(asin)  // Use apiService to save the email here
        .then((response) => {
          console.log(response)
          if(response.error){
            if(response.error == "NoResults"){
              ElMessage({
                  message: 'No variants for this item',
                  type: 'error',
                  duration: 2000, // Duration is in milliseconds, so 2000 ms = 2 seconds
              });
            }
          }else{
            store.dispatch('setVariants', response);
          }
        })
        .catch(error => console.error(error))
        .finally(() => {
          store.dispatch('endLoading');
        });
}

const getUserData = async (accessToken) => {
  try {
    const response = await fetch(`https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=${accessToken}`);
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    const userData = await response.json();
    // console.log("User data: ", userData);
    return userData;
  } catch (error) {
    console.error("Error fetching user data: ", error);
  }
}

const login = () => {
  closeLanguage()
  googleTokenLogin().then((response) => {
    getUserData(response.access_token).then((data) => {
      userPicture.value = data.picture
      // Save user data to local storage
      const userData = { ...response, picture: data.picture, email: data.email }
      localStorage.setItem('userData', JSON.stringify(userData))

      // send email to backend
      apiService.saveEmail(data.email)  // Use apiService to save the email here
        .then((response) => {
          if(response.message && response.message == "Email saved successfully"){
            store.dispatch('fetchUserSearchHistory', userData.email)
          }  
        })
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

const changeLanguage = (language) => {
  store.commit('setLanguage', language);
  if(language == 'English'){
    defaultChoices[0].image = defaultImage1_en;
    // defaultChoices[1].image = defaultImage2_en;
    defaultChoices[1].image = defaultImage3_en;
    defaultListImage = defaultListImage_en;
  }
  if(language == 'Simplified_Chinese'){
    defaultChoices[0].image = defaultImage1_zh;
    // defaultChoices[1].image = defaultImage2_zh;
    defaultChoices[1].image = defaultImage3_zh;
    defaultListImage = defaultListImage_zh
  }
}

// const fillInputbox = (event) => {
//       userInputInputbox.value = event.target.innerText;
//       generateEssentials()
// }

const setItemQuery = (event) => {
  console.log("setItemQuery", event.target.innerText)
  globalState.itemQuery = event.target.innerText;
  let item = store.state.listResults[event.target.innerText]
  if(item.choices.length != 0 || item.empty){
    store.dispatch('setSearchResults', item)
  }else{
    initialSubmit(globalState.itemQuery)
  }
  // if(!store.state.inSearchList.includes(event.target.innerText) 
  // && (item.choices.length != 0 
  //   || item.empty)){
  //   initialSubmit(globalState.itemQuery)
  // }else{
  //   if(item.choices.length != 0 
  //   || item.empty){
  //     store.dispatch('setSearchResults', item)
  //   }else{
  //     item.isSet = true
  //     store.dispatch('startLoading')
  //   }
  // }
}

// const toggleVisibility = () => {
//     isVisible.value = !isVisible.value;
//     window.scrollTo({ top: choice_card_container.value.$el.offsetTop, behavior: 'smooth' });
//   }

  const addToCart = (choice) => {
  // Check if the item is already in the array
  const exists = cartDropdownItems.value.find(item => item.asin === choice.asin);

  if (!exists) {
    // If the item doesn't exist, add it to the array
    cartDropdownItems.value.push({
      target: truncateValue(choice.target, 35), 
      asin: choice.asin, 
      image_urls: choice.image_urls, 
      price: choice.price, 
      quantity: "1" 
    });

    ElMessage({
      message: 'item added to cart',
      type: 'success',
      duration: 2000, // Duration is in milliseconds, so 2000 ms = 2 seconds
    });

    // if(store.state.listResults[store.state.searchResults.target].next
    // && store.state.listResults[store.state.listResults[store.state.searchResults.target].next].choices.length == 0){
    //   setTimeout(() => {
    //     nextItem()
    //   }, 1500); 
    // }

  } else {
    ElMessage({
      message: 'item already in cart',
      type: 'info',
      duration: 2000,
    });
  }
}

const deleteCartItem = (target, index) => {
  cartDropdownItems.value.splice(index, 1);
  ElMessage({
  message: target + ' Deleted',
  type: 'success',
  duration: 2000, // Duration is in milliseconds, so 2000 ms = 2 seconds
  });
  if (cart.value && cart.value.handleClose && cartDropdownItems.value.length == 0) {
    cart.value.handleClose()
  }
}

const showShoppingCart = () => {
  if (cart.value && cart.value.handleOpen) {
    cart.value.handleOpen()
  }
  window.scrollTo({ top: cart.value.$el.offsetTop, behavior: 'smooth' });
}

const checkoutOnAmazon = () => {
      document.getElementById('amazon-form').submit();
    }

const closeLanguage = () => {
  if (language_dropdown.value && language_dropdown.value.handleClose) {
    language_dropdown.value.handleClose()
  }
}

// const deleteFromList = (item) => {

//   let list = store.state.listResults
//   if(list[item]['target'] != store.state.searchResults['target']){
//   // Check if item exists in list
//   if (!list[item]) {
//         console.error('Item not found in list');
//         return list;
//     }

//     // Get the "pre" and "next" items from the item to be deleted
//     let pre = list[item]['pre'];
//     let next = list[item]['next'];

//     // Update the "next" of the "pre" item
//     if (pre !== "" && list[pre]) {
//         list[pre]['next'] = next;
//     }

//     // Update the "pre" of the "next" item
//     if (next !== "" && list[next]) {
//         list[next]['pre'] = pre;
//     }

//     // Delete the item from list
//     delete list[item];

//     console.log(store.state.listResults)

//     ElMessage({
//         message: item + ' Deleted',
//         type: 'success',
//         duration: 2000, // Duration is in milliseconds, so 2000 ms = 2 seconds
//     });
//   }else{
//     ElMessage({
//         message: 'Present item can not be deleted',
//         type: 'error',
//         duration: 2000, // Duration is in milliseconds, so 2000 ms = 2 seconds
//     });
//   }

// }

const truncateValue = (value, length) => {
  return value.length > length ? value.substring(0, length - 3) + '...' : value;
}

const goToHomePage = () => {
      router.push('/').then(() => window.location.reload())
    }

// const confirmList = () => {
//   window.scrollTo({ top: choice_card_container.value.$el.offsetTop, behavior: 'smooth' });
// }

onMounted(() => {
  // Check local storage for user data
  const storedUserData = localStorage.getItem('userData')

  if (storedUserData) {
    // Parse the user data and update userPicture
    const userData = JSON.parse(storedUserData)
    userPicture.value = userData.picture
    store.dispatch('fetchUserSearchHistory', userData.email)    
  }

  if (language_dropdown.value && language_dropdown.value.handleOpen) {
    language_dropdown.value.handleOpen()
    setTimeout(() => {
      if (language_dropdown.value && language_dropdown.value.handleClose) {  
        language_dropdown.value.handleClose()
      }
    }, 1500);  
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
    padding-bottom: 10px;
  }
  .search-form{
    background-color: honeydew;
    padding-top: 5px;
    padding-bottom: 5px;
  }

  .fine-tune-section{
    background-color: honeydew;
    padding-top: 10px;
    padding-bottom: 10px;
  }

  .fine-tune-card{
    border-radius: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .fine-tune-button{
    margin-top: 10px;
  }

  .fine-tune-button-div{
    text-align: center;
    padding-bottom: 5px;
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
    padding-top: 5px;
  }

  .cart-icon{
    padding-top: 5px;
  }
  
  .generate-button{
    text-align: center;
  }

</style>

  