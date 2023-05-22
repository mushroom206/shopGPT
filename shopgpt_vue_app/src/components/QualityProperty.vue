<template>
  <div class="quality-property">
    <label for="quality-select">{{ quality.quality }}: </label>
    <select id="quality-select" @change="optionSelected">
      <option disabled selected value="">Select {{ quality.quality }} preference</option>
      <option v-for="option in quality.options" :key="option">{{ option }}</option>
    </select>
  </div>
</template>

<script>
export default {
  props: ['quality'],
  methods: {
    optionSelected(event) {
      this.$emit('option-selected', { [this.quality.quality]: event.target.value })
    }
  }
}
</script>
