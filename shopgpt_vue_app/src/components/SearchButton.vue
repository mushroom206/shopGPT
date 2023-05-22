<!-- SearchButton.vue -->
<template>
  <button class="search-button" @click="emitSubmit">{{ label }}</button>
</template>

<script>
export default {
  name: 'SearchButton',
  props: {
    label: {
      type: String,
      default: 'Search'
    }
  },
  methods: {
    emitSubmit() {
      this.$emit('submit');
    },
  },
};
</script>


