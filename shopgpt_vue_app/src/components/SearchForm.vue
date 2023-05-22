<template>
    <div class="search-form">
      <form @submit.prevent="submitForm" class="search-form">
        <input type="text" v-model="item_query" placeholder="Enter item name or description">
        <span v-if="v$.item_query.$error" class="error-text">Input is required and should be less than 20 words</span>
        <SearchButton @submit="submit" />
      </form>
    </div>
  </template>
  
  <script>
  import { required, maxLength } from '@vuelidate/validators'
  import { useVuelidate } from '@vuelidate/core'
  import { useStore } from 'vuex'
  import SearchButton from './SearchButton.vue';
  
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
          maxLength: maxLength(20)
        }
      }
    },
    components: {
    SearchButton,
    // other components go here
  },
    methods: {
      async submitForm() {
        await this.v$.$validate()
  
        if (this.v$.item_query.$error) {
          // Don't submit form if there's a validation error
          return
        }
  
        // call your backend API
        this.store.dispatch('fetchSearchResults', this.item_query);
      }
    }
  }
  </script>
  
  <style scoped>
  .error-text {
    color: red;
  }
  </style>
  