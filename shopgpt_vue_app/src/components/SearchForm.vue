<template>
    <div class="search-form">
      <form @submit.prevent="submitForm">
        <el-input v-model="globalState.itemQuery" :placeholder="$t('smart watch, yoga mat, etc.')"  clearable size="large">
          <template #append>
            <el-button type="primary" @click="submitForm">{{$t('Search')}}</el-button>
          </template>
        </el-input>
        <!-- <span v-if="v$.item_query.$error" class="error-text">Input is required and should be less than 20 words</span> -->
      </form>
    </div>
  </template>
  
  <script>
  import { useStore } from 'vuex'
  import { inject } from 'vue'
  
  export default {
    setup() {
      const globalState = inject('globalState')
      const store = useStore()

      return { store, globalState }
    },
    data() {

    },
    validations() {

    },
    components: {
  },
    methods: {
      async submitForm() {
        if(this.globalState.itemQuery != null && this.globalState.itemQuery != ''){
          this.$emit('submit', this.globalState.itemQuery);
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
  