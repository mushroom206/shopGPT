<template>
    <div class="search-form">
      <form @submit.prevent="submitForm">
        <el-input v-model="item_query" placeholder="Enter item or description" :prefix-icon="Search" clearable maxlength="50" show-word-limit size="large" :autofocus="true">
          <template #append>
            <el-button type="primary" @click="submitForm">Search</el-button>
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
      // call your backend API
      this.store.dispatch('fetchSearchResults', this.item_query);
      // emit 'submit' event
      this.$emit('submit');
    }
  }
    }
  }
  </script>
  
  <style scoped>
  .search-form {
      text-align: center;
      vertical-align: middle;
      line-height: 400%;
    }
  /* .error-text {
    color: red;
  } */
  </style>
  