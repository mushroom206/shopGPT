<template>
  <el-card :body-style="{ padding: '0px' }" shadow="hover" class="card" v-if="!choice.default">
      <el-container>
        <!-- <el-header>HEAD</el-header> -->
        <el-main style="padding: 5px;">
          <el-card :body-style="{ 'padding-top': '5px', 'padding-bottom': '0px', 'padding-left': '5px', 'padding-right': '5px', 'font-size': '15px' }">
            <div style="margin-left: 5px;" v-if="!choice.default">
              <b>{{ choice.target }}</b>
            </div>
            <div class="image-description">
              <div>
                <el-image v-if="!choice.default"
                  style="width: 155px; height: 155px; margin-top: 5px; margin-right: 5px; margin-bottom: 5px;"
                  :src="localData.choice.image_urls"
                  :zoom-rate="1.2"
                  :preview-src-list="localData.choice.image_urls"
                  fit="contain"
                />
                <el-image v-else
                  :src="choice.image"
                  fit="contain"
                />
                <div class="amazon-info" v-if="choice.pros" style="margin-bottom: 5px; margin-top: -5px;">
                  <el-tag size="large" type="warning" effect="light" round>
                    <b>{{ localData.choice.price }}</b>
                  </el-tag>
                </div>
              </div>
              <div style="margin-left: 10px;">
                <div class="amazon-info" v-if="choice.pros && localData.choice.amazon_fulfill"><el-tag size="large" type="success" effect="plain" round>{{$t('Fulfilled by Amazon')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 5px;" v-if="choice.pros && localData.choice.free_shipping"><el-tag size="large" type="success" effect="plain" round>{{$t('Free Shipping')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 5px;" v-if="choice.pros && localData.choice.prime_eligible"><el-tag size="large" type="success" effect="plain" round>{{$t('Prime Eligible')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 5px;" v-if="choice.pros"><el-tag size="large" type="success" effect="plain" round>{{$t('Above 4 stars')}}</el-tag></div>
                <div class="amazon-info" style="margin-top: 15px;" v-if="choice.pros"><el-button @click="findVariants" size="medium" type="primary" :icon="Search">{{$t('Check Variants')}}</el-button></div>
              </div>
            </div>
            <!-- <span v-if="!choice.default">{{$t('click to see more')}}</span> -->
            <!-- <div class="description" v-if="!choice.default">{{ choice.description }}</div> -->
            <div v-if="choice.variation_dimensions">
              <div v-for="(dimension, index) in choice.variation_dimensions" :key="index">
                <div style="margin-bottom: 5px;"><b>{{ dimension.display_name }}</b></div>
                <el-scrollbar>
                  <div class="scrollbar-flex-content" style="margin-bottom: 5px;">
                    <div class="variation_options" v-for="(value, valueIndex) in dimension.values" :key="valueIndex" @click="changeButtonDisplay(dimension.name, value)">
                      <el-image v-if="getVariantPreviewImage(dimension.name, value)"
                      style="width: 50px; height: 50px; margin-top: -5px;  margin-bottom: 3px;"
                      :src="getVariantPreviewImage(dimension.name, value)"
                      fit="contain"
                      >
                      </el-image>
                      <el-tag
                        :type="availableOptions[dimension.name].includes(value) ? 'success' : 'danger'"
                        size="medium"
                        :effect="selectedOptions[dimension.name] != value ? 'light' : 'dark'"
                      >
                        {{ truncateValue(value, 10) }}
                      </el-tag>
                    </div>
                  </div>
                </el-scrollbar>
              </div>  
            </div>
            <div class="pros" v-if="choice.pros">
              <!-- <h4>{{$t('Pros')}}:</h4> -->
              <ul class="check-list">
                <li v-for="(pro, index) in choice.pros" :key="index">{{ pro }}</li>
              </ul>
            </div>
            <div class="cons" v-if="choice.cons">
              <!-- <h4>{{$t('Cons')}}:</h4> -->
              <ul class="cross-list">
                <li v-for="(con, index) in choice.cons" :key="index">{{ con }}</li>
              </ul>
            </div>
            <div class="amazon-link" v-if="choice.pros">
            <!-- <el-link :href="choice.url" target="_blank">
              <el-image :src="require('@/assets/images/amazon_button.png')" :fit="contain" />
            </el-link> -->
            <el-link @click="addToCart" style="margin-bottom: 5px; margin-right:5px;">
              <el-image :src="require('@/assets/images/amazon_button.png')" :fit="contain" style="width: 140px; height: 35px" />
            </el-link>
            <el-button @click="findSimilar" style="margin-bottom: 5px;" size="medium" type="primary" :icon="Search">{{$t('Find similar Item')}}</el-button>
            </div>
            <!-- <div class="amazon-price" v-if="choice.pros"> 
              <h4>For: {{ choice.price }}</h4>
            </div> -->
          </el-card>
        </el-main>
        <el-footer height="40px" v-if="!choice.default">
          <div class="ask-question">
            <el-input v-model="question" :placeholder="$t('Tell me more')" :prefix-icon="Search" clearable>
              <template #append>
                <el-button type="primary" @click="askQuestion" :loading="$store.state.loading">{{$t('Ask AI')}}</el-button>
              </template>
            </el-input>
          </div>
        </el-footer>
      </el-container>
  </el-card>
</template>

<script setup>
import { Search } from '@element-plus/icons-vue'
import { ref, reactive, watch, defineProps, defineEmits } from 'vue';

// Define props
const props = defineProps({
  choice: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['ask-question', 'add-to-cart', 'find-similar', 'find-variants']);

const localData = reactive({
  choice: props.choice
});


let question = ref('');
let selectedOptions = ref({});
let availableOptions = ref({});

const getVariantPreviewImage = (attrName, option) => {
  if(attrName == props.choice.variation_dimensions[0].name){
    for (let i = 0; i < props.choice.variants.length; i++) {
      if (props.choice.variants[i].variation_attributes.find(v => v.name == attrName).value == option) {
        return props.choice.variants[i].image_urls[0]
      }
    }
  }

  return ""
}

const truncateValue = (value, length) => {
  return value.length > length ? value.substring(0, length - 3) + '...' : value;
}

const changeButtonDisplay = (attrName, option) => {
  availableOptions.value = {}

  selectedOptions.value = { ...selectedOptions.value, [attrName]: option };
    //set all availableOptions values to true for the clicked attr
    availableOptions.value[attrName] = props.choice.variation_dimensions.find(d => d.name == attrName).values
    //set values of other availableOptions
    props.choice.variation_dimensions.forEach(dim => {
        if(!availableOptions.value[dim.name]){
          let values = []
          props.choice.variants.forEach(variant => {
              if(variant.variation_attributes.find(v => v.name == attrName).value ==  option){
                values.push(variant.variation_attributes.find(v => v.name == dim.name).value)
              }
            })
            availableOptions.value[dim.name] = values
        }
      });
      //check if slected options are all still available after click, if not find an available one
      for (let key in selectedOptions.value) {
        if(key != attrName){
          if(availableOptions.value[key].indexOf(selectedOptions.value[key]) == -1){
            selectedOptions.value = { ...selectedOptions.value, [key]: availableOptions.value[key][0] };
          }
        }
      }

};

watch(() => props.choice.variants, (newVariants) => {
  // Whenever props.choice.variation_dimensions changes, this function will be executed.
  let chosenValue
  let chosenName
  if (newVariants) {
    //set selectedOptions attr.name to first available variant
      newVariants[0].variation_attributes.forEach(attr => {
        selectedOptions.value = { ...selectedOptions.value, [attr.name]: attr.value };
        if (Object.keys(availableOptions.value).length === 0) {
          //get set availableOptions values for attr.name
          availableOptions.value[attr.name] = props.choice.variation_dimensions.find(d => d.name == attr.name).values
          chosenValue = attr.value;
          chosenName = attr.name
        }
      });
      props.choice.variation_dimensions.forEach(dim => {
        //if dim.name not yet in availableOptions
        if(!availableOptions.value[dim.name]){
          let values = []
          //for each variant add values to availableOptions respective dim
            newVariants.forEach(variant => {
              if(variant.variation_attributes.find(v => v.name == chosenName).value ==  chosenValue){
                values.push(variant.variation_attributes.find(v => v.name == dim.name).value)
              }
            })
            availableOptions.value[dim.name] = values
        }
      });
    }
}, { immediate: true });

watch(() => selectedOptions.value, (newOpitons) => {
  let flag = true
  let index = 0
  for (let i = 0; i < props.choice.variants.length; i++) {
    flag = true
    props.choice.variants[i].variation_attributes.forEach(attr => {
      if(newOpitons[attr.name] != attr.value){
        flag = false
      }
    })
    if(flag){
      index = i
      break
    }
  }
  localData.choice.image_urls = props.choice.variants[index].image_urls
  localData.choice.price = props.choice.variants[index].price
  localData.choice.amazon_fulfill = props.choice.variants[index].amazon_fulfill
  localData.choice.free_shipping = props.choice.variants[index].free_shipping
  localData.choice.prime_eligible = props.choice.variants[index].prime_eligible
  localData.choice.asin = props.choice.variants[index].asin
});

// Methods for events
const askQuestion = () => {
  if (question.value !== '') {
    emit('ask-question', props.choice, question.value);
  }
};

const addToCart = () => {
  emit('add-to-cart', localData.choice);
};

const findSimilar = () => {
  emit('find-similar', props.choice.target);
};

const findVariants = () => {
  emit('find-variants', props.choice.asin);
};
</script>
