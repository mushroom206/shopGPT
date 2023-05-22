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
  </div>
</template>

<script>
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
    };
  },
};
</script>

