<template>
  <el-card :body-style="{ padding: '0px' }" shadow="hover" class="card">
      <el-container>
        <!-- <el-header>HEAD</el-header> -->
        <el-main style="padding: 5px;">
          <el-card :body-style="{ 'padding-top': '5px', 'padding-bottom': '0px', 'padding-left': '5px', 'padding-right': '5px', 'font-size': '15px' }">
            <div style="margin-left: 5px;" v-if="!choice.default">
              <b>{{ choice.target }}</b>
            </div>
            <div class="image-description">
              <div>
                <el-image v-if="!choice.default"
                  style="width: 150px; height: 150px; margin-top: 5px; margin-right: 5px; margin-bottom: 5px;"
                  :src="choice.image_urls"
                  :zoom-rate="1.2"
                  :preview-src-list="choice.image_urls"
                  fit="contain"
                />
                <el-image v-else
                  style="width: 300px; height: 300px"
                  :src="choice.image"
                  fit="contain"
                />
                <div class="amazon-info" v-if="choice.pros" style="margin-bottom: 5px;"><el-tag size="large" type="warning" effect="light" round><b>{{ choice.price }}</b></el-tag></div>
              </div>
              <div style="margin-left: 10px;">
                <div class="amazon-info" v-if="choice.pros && choice.amazon_fulfill"><el-tag size="large" type="success" effect="plain" round>{{$t('Fulfilled by Amazon')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 5px;" v-if="choice.pros && choice.free_shipping"><el-tag size="large" type="success" effect="plain" round>{{$t('Free Shipping')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 5px;" v-if="choice.pros && choice.prime_eligible"><el-tag size="large" type="success" effect="plain" round>{{$t('Prime Eligible')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 5px;" v-if="choice.pros"><el-tag size="large" type="success" effect="plain" round>{{$t('Above 4 stars')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 10px;" v-if="choice.pros"><el-button @click="findSimilar" size="medium" type="primary" :icon="Search">{{$t('Find similar Item')}}</el-button></div>
              </div>
            </div>
            <!-- <span v-if="!choice.default">{{$t('click to see more')}}</span> -->
            <!-- <div class="description" v-if="!choice.default">{{ choice.description }}</div> -->
            <div class="pros" v-if="choice.pros">
              <!-- <h4>{{$t('Pros')}}:</h4> -->
              <ul class="check-list">
                <li v-for="(pro, index) in choice.pros" :key="index">{{ pro }}</li>
              </ul>
            </div>
            <div class="cons" v-if="choice.cons">
              <!-- <h4>{{$t('Cons')}}:</h4> -->
              <ul class="cross-list">
                <li v-for="(con, index) in choice.cons" :key="index">{{ con }}</li>
              </ul>
            </div>
            <div class="amazon-link" v-if="choice.pros">
            <!-- <el-link :href="choice.url" target="_blank">
              <el-image :src="require('@/assets/images/amazon_button.png')" :fit="contain" />
            </el-link> -->
            <el-link @click="addToCart" style="margin-bottom: 5px;">
              <el-image :src="require('@/assets/images/amazon_button.png')" :fit="contain" style="width: 140px; height: 35px" />
            </el-link>
            </div>
            <!-- <div class="amazon-price" v-if="choice.pros"> 
              <h4>For: {{ choice.price }}</h4>
            </div> -->
          </el-card>
        </el-main>
        <el-footer height="40px" v-if="!choice.default">
          <div class="ask-question">
            <el-input v-model="question" :placeholder="$t('Tell me more')" :prefix-icon="Search" clearable>
              <template #append>
                <el-button type="primary" @click="askQuestion" :loading="$store.state.loading">{{$t('Ask AI')}}</el-button>
              </template>
            </el-input>
          </div>
        </el-footer>
      </el-container>
  </el-card>
</template>

<script>
// import apiService from '../services/apiService'

export default {
  props: {
    choice: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      question: ''
    };
  },
  methods: {
    async askQuestion() {
    if (this.question !== '') {
      this.$emit('ask-question', this.choice, this.question);
    }
  },
  addToCart() {
    this.$emit('add-to-cart', this.choice);
    },
  findSimilar() {
    this.$emit('find-similar', this.choice.target);
    }  
  }
};
</script>

<script setup>
import { Search } from '@element-plus/icons-vue'
</script>
