<template>
  <div>
    <button @click="googleSignIn">Sign In with Google</button>
  </div>
</template>

<script>
export default {
  methods: {
    async googleSignIn() {
      try {
        const googleUser = await this.$gAuth.signIn();
        const idToken = googleUser.getAuthResponse().id_token;
        console.log(idToken);
        // Here you would usually send the idToken to your server for verification and sign in the user
      } catch(error) {
        console.error(error);
      }
    }
  }
}
</script>

