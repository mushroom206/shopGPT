<template>
  <div class="quality-property">
    <el-row>
      <el-col :span="10">
        <label for="quality-select">{{ quality.quality }}: </label>
      </el-col>
      <el-col :span="14">
        <select id="quality-select" @change="optionSelected">
          <option v-for="option in quality.options" :key="option" :selected="option === quality.options[0]">{{ option }}</option>
        </select>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  props: ['quality'],
  methods: {
    optionSelected(event) {
      this.$emit('option-selected', { [this.quality.quality]: event.target.value })
    },
  },
  created() {
    if (this.quality.options && this.quality.options.length > 0) {
      this.$emit('option-selected', { [this.quality.quality]: this.quality.options[0] });
    }
  }
}
</script>
