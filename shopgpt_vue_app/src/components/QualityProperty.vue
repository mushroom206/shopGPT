<template>
  <div class="quality-property">
    <!-- <label for="quality-select">{{ quality.quality }}: </label> -->
    <el-dropdown @command="optionSelected">
      <el-button type="primary">
        {{ selectedOption }}<el-icon class="el-icon--right"><ArrowDown /></el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item v-for="(option, index) in quality.options" :key="index" :command="option">{{ option }}</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <!-- <label for="quality-select">{{ quality.quality }}: </label>
    <el-radio-group v-model="selectedOption" @change="optionSelected">
      <el-radio-button v-for="option in quality.options" :key="option" :label="option"></el-radio-button>
    </el-radio-group> -->
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
  methods: {
    optionSelected(value) {
      this.selectedOption = value;
    },
  },
  watch: {
    'quality.options': {
      handler: function(newVal) {
        this.selectedOption = newVal[0];
      },
      deep: true
    },
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


