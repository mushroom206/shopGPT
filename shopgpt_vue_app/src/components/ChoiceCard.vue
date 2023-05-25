<template>
  <div class="choice-card">
    <h2>{{ choice.brand }} - {{ choice.item_category }} - {{ choice.model }}</h2>
    <img :src="placeholderImageUrl" alt="Product image">
    <p>{{ choice.description }}</p>
    <div class="pros-cons">
      <div class="pros">
        <h3>Pros:</h3>
        <ul>
          <li v-for="(pro, index) in choice.pros" :key="index">{{ pro }}</li>
        </ul>
      </div>
      <div class="cons">
        <h3>Cons:</h3>
        <ul>
          <li v-for="(con, index) in choice.cons" :key="index">{{ con }}</li>
        </ul>
      </div>
    </div>
    <div class="ask-question">
      <input type="text" v-model="question" placeholder="Ask a question about this item">
      <button @click="askQuestion">Ask</button>
      </div>
  </div>
</template>

<script>
import apiService from '../services/apiService'

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
        // trigger the API call here
        const response = await apiService.askItemDetails(this.choice, this.question);
        // for now just log the response
        console.log(response);
        // Emit the custom event with the response as payload
        this.$emit('ask-response', response);
        // clear the question field after submitting
        this.question = '';
      }
    }
  }
};
</script>

