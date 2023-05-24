<template>
  <div id="app">
    <router-view/>
    <SearchForm @submit="initialSubmit" />
    <div class="choices">
      <ChoiceCard v-for="choice in searchResults.choices" :key="choice.brand" :choice="choice" />
    </div>
    <div v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" class="qualities-properties">
      <h2>Things to consider when shopping {{ searchResults.target }}</h2>
      <QualityProperty v-for="quality in searchResults['qualities-properties']" :key="quality.name" :quality="quality" @option-selected="updateQuality" />
    </div>
    <SearchButton v-if="searchResults['qualities-properties'] && searchResults['qualities-properties'].length" @submit="submitQualities" label="Fine Tune!" />
  </div>
</template>

<script>
import SearchForm from './components/SearchForm.vue'
import ChoiceCard from './components/ChoiceCard.vue'
import QualityProperty from './components/QualityProperty.vue'
import { mapState } from 'vuex'
import SearchButton from './components/SearchButton.vue';

export default {
  components: {
    SearchForm,
    ChoiceCard,
    QualityProperty,
    SearchButton
  },
  data() {
    return {
      item_query: null,
      selectedQualities: {},
      allQualitiesSelected: false,
    }
  },
  computed: mapState({
    searchResults: state => state.searchResults
  }),
  watch: {
    searchResults: {
      handler(newVal) {
        console.log(JSON.stringify(newVal, null, 2));
      },
      deep: true
    }
  },
  methods: {
    initialSubmit() {
      if (this.item_query != null) {
      console.log('initialSubmit is called with item_query: ', this.item_query);
      this.$store.dispatch('fetchSearchResults', this.item_query);
      }
      else {
        return
      }
    },
    submitQualities() {
      if (this.allQualitiesSelected) {
        this.$store.dispatch('fetchRefinedSearchResults', { target: this.searchResults.target, qualities: this.selectedQualities });
        this.allQualitiesSelected = false;
      }
    },
    updateQuality(selectedQuality) {
      this.selectedQualities = { ...this.selectedQualities, ...selectedQuality };

      if (Object.keys(this.selectedQualities).length === this.searchResults['qualities-properties'].length) {
        this.allQualitiesSelected = true;
      }
    }
  }
}

</script>
