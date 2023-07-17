<template>
  <el-card :body-style="{ padding: '0px' }" shadow="hover" class="card">
      <el-container>
        <!-- <el-header>HEAD</el-header> -->
        <el-main>
          <el-card :body-style="{ 'padding-top': '0px', 'padding-bottom': '0px' }">
            <div class="header" v-if="!choice.default">
              <h3>{{ choice.target }}</h3>
            </div>
            <div class="image-description">
              <el-image v-if="!choice.default"
                style="width: 150px; height: 150px"
                :src="choice.image_urls"
                :zoom-rate="1.2"
                :preview-src-list="choice.image_urls"
                fit="contain"
              />
              <el-image v-else
                style="width: 250px; height: 250px"
                :src="choice.image"
                fit="contain"
              />
              <h5 v-if="!choice.default">{{$t('click image to view more')}}</h5>
            </div>
            <!-- <div class="description" v-if="!choice.default">{{ choice.description }}</div> -->
            <div class="pros" v-if="choice.pros">
              <h4>{{$t('Pros')}}:</h4>
              <ul class="check-list">
                <li v-for="(pro, index) in choice.pros" :key="index">{{ pro }}</li>
              </ul>
            </div>
            <div class="cons" v-if="choice.cons">
              <h4>{{$t('Cons')}}:</h4>
              <ul class="cross-list">
                <li v-for="(con, index) in choice.cons" :key="index">{{ con }}</li>
              </ul>
            </div>
            <div class="amazon-link" v-if="choice.pros">
            <!-- <el-link :href="choice.url" target="_blank">
              <el-image :src="require('@/assets/images/amazon_button.png')" :fit="contain" />
            </el-link> -->
            <el-link @click="addToCart">
              <el-image :src="require('@/assets/images/amazon_button.png')" :fit="contain" />
            </el-link>
            </div>
            <div class="amazon-price" v-if="choice.pros"> 
              <h4>On Amazon for: {{ choice.price }}</h4>
            </div>
          </el-card>
        </el-main>
        <el-footer v-if="!choice.default">
          <div class="ask-question">
            <el-input v-model="question" :placeholder="$t('Tell me more about this item')" :prefix-icon="Search" clearable>
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
  }
};
</script>

<script setup>
import { Search } from '@element-plus/icons-vue'
</script>
