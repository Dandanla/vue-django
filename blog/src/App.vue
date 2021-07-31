
<!--  frontend/src/App.vue  -->

<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
import HomeVue from "./pages/Home.vue"
    export default {
        HomeVue,
        name: 'App'
    }
</script>

<style>
    /* #app {
        font-family: Georgia, Arial, sans-serif;
        margin-left: 40px;
        margin-right: 40px;
    } */
</style>