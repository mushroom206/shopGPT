import Vue from 'vue';
import Router from 'vue-router';
import PrivacyPolicy from './views/PrivacyPolicy.vue';
import TermsOfService from './views/TermsOfService.vue';

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/privacy-policy',
            name: 'PrivacyPolicy',
            component: PrivacyPolicy
        },
        {
            path: '/terms-of-service',
            name: 'TermsOfService',
            component: TermsOfService
        },
        // other routes...
    ]
});

