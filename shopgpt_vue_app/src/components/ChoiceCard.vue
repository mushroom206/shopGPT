<template>
  <el-card shadow="hover" class="card">
      <el-container>
        <!-- <el-header>HEAD</el-header> -->
        <el-main>
          <div class="header" v-if="!choice.default">
            <h2>{{ choice.brand }} - {{ choice.item_category }} - {{ choice.model }}</h2>
          </div>
          <el-card>
            <div class="image-description">
              <el-image :src="choice.image || placeholderImageUrl" fit="cover"></el-image>
            </div>
            <div class="description" v-if="!choice.default">{{ choice.description }}</div>
            <div class="pros" v-if="choice.pros">
              <h3>Pros:</h3>
              <ul class="check-list">
                <li v-for="(pro, index) in choice.pros" :key="index">{{ pro }}</li>
              </ul>
            </div>
            <div class="cons" v-if="choice.cons">
              <h3>Cons:</h3>
              <ul class="cross-list">
                <li v-for="(con, index) in choice.cons" :key="index">{{ con }}</li>
              </ul>
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
      placeholderImageUrl: 'https://via.placeholder.com/150',
      question: '',
    };
  },
  methods: {
    async askQuestion() {
    if (this.question !== '') {
      this.$emit('ask-question', this.choice, this.question);
    }
  }
  }
};
</script>
<style scoped>
.card{
    background-color: #fff5d8;
    border-radius: 30px;
  }
</style>

<script setup>
import { Search } from '@element-plus/icons-vue'
</script>
