<!-- SearchButton.vue -->
<template>
  <el-button type="info" plain class="search-button" @click="emitSubmit">{{ label }}</el-button>
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


