<template>
  <div class="quality-property">
    <label for="quality-select">{{ quality.quality }}: </label>
    <el-radio-group v-model="selectedOption" @change="optionSelected">
      <el-radio-button v-for="option in quality.options" :key="option" :label="option"></el-radio-button>
    </el-radio-group>
  </div>
</template>

<script>
export default {
  props: ['quality'],
  data() {
    return {
      selectedOption: this.quality.options[0]
    };
  },
  watch: {
    selectedOption(value) {
      this.$emit('option-selected', { [this.quality.quality]: value })
    }
  },
  created() {
    if (this.quality.options && this.quality.options.length > 0) {
      this.$emit('option-selected', { [this.quality.quality]: this.quality.options[0] });
    }
  }
}
</script>

