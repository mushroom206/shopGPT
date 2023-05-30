<template>
    <div class="search-form">
      <form @submit.prevent="submitForm">
        <el-input v-model="item_query" :placeholder="$t('smart watch, Christmas gift, etc.')"  clearable maxlength="50" show-word-limit size="large">
          <template #append>
            <el-button type="primary" @click="submitForm">{{$t('Search')}}</el-button>
          </template>
        </el-input>
        <!-- <span v-if="v$.item_query.$error" class="error-text">Input is required and should be less than 20 words</span> -->
      </form>
    </div>
  </template>
  
  <script>
  import { required, maxLength } from '@vuelidate/validators'
  import { useVuelidate } from '@vuelidate/core'
  import { useStore } from 'vuex'
  
  export default {
    setup() {
      const v$ = useVuelidate()
      const store = useStore()
      return { v$, store }
    },
    data() {
      return {
        item_query: ''
      }
    },
    validations() {
      return {
        item_query: {
          required,
          maxLength: maxLength(100)
        }
      }
    },
    components: {
  },
    methods: {
      async submitForm() {
    await this.v$.$validate()
    if (!this.v$.item_query.$error) {
      this.$emit('submit', this.item_query);
    }
  }
    }
  }
  </script>
  
  <style scoped>
  .search-form {
      text-align: center;
      vertical-align: middle;
      line-height: 200%;
    }
  /* .error-text {
    color: red;
  } */
  </style>
  