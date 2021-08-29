
<!--  frontend/src/App.vue  -->

<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
import Home from "./pages/Home.vue"
    export default {
        Home,
        name: 'App',
    }
</script>

<style>
    /* #app {
        font-family: Georgia, Arial, sans-serif;
        margin-left: 40px;
        margin-right: 40px;
    } */
</style>