<template>
  <q-layout view="lHh Lpr fff" class="bg-grey-1">
    <q-header elevated class="bg-white text-grey-8" height-hint="64">
      <q-toolbar class="GPL__toolbar" style="height: 64px">

        <q-toolbar-title v-if="$q.screen.gt.sm" shrink class="row items-center no-wrap">
          <q-btn outline rounded color="primary"
          no-caps
          v-on:click.prevent="signin"
          >
          Welcome，{{username}}
          </q-btn>
        </q-toolbar-title>

        <q-space />

        <q-input class="GPL__toolbar-input" dense standout="bg-primary" v-model="search" placeholder="Search">
          <template v-slot:prepend>
            <q-icon v-if="search === ''" name="search" />
            <q-icon v-else name="clear" class="cursor-pointer" @click="search = ''" />
          </template>
        </q-input>

        <q-space />

        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn round dense flat color="grey-8" icon="notifications">
            <!-- <q-badge color="red" text-color="white" floating>
              2
            </q-badge> -->
            <q-tooltip>{{notice}}</q-tooltip>
          </q-btn>
          <q-btn round flat>
            <q-avatar size="26px">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png">
            </q-avatar>
            <q-tooltip>{{username}}</q-tooltip>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>


    <q-page-container>
      <router-view />
    </q-page-container>

    
  </q-layout>
</template>

<script>
import { ref } from 'vue'
export default {
  name: 'Layout',
  data: function () {
    return {
        searchText: '',
        username: '',
        hasLogin: false,
    }
},
  setup () {
    const leftDrawerOpen = ref(false)
    const search = ref('')
    const storage = ref(0.26)
    function toggleLeftDrawer () {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }
    return {
      leftDrawerOpen,
      search,
      storage,
    }
  },

        methods: {
            signin() {
                const that = this;
                that.$router.push({name: 'Login'});
            },
        },
        
    mounted() {
      const that = this;
      const storage = localStorage;
      // 过期时间
      const expiredTime = Number(storage.getItem('expiredTime.myblog'));
      // 当前时间
      const current = (new Date()).getTime();
      // 刷新令牌
      const refreshToken = storage.getItem('refresh.myblog');
      // 用户名
      that.username = storage.getItem('username.myblog');

      that.notice = "暂无消息"

      // 初始 token 未过期
      if (expiredTime > current) {

          that.hasLogin = true;
      }
      // 初始 token 过期
      // 如果有刷新令牌则申请新的token
      else if (refreshToken !== null) {
          that.username = "登陆信息过期，点击重新登陆"
          storage.clear();
          that.hasLogin = false;
      }
      // 无任何有效 token
      else {
          storage.clear();
          that.hasLogin = false;
          that.username = "点击登陆"
          that.notice = "请先登陆"
      }
    }
}
</script>

<style lang="sass">
.GPL
  &__toolbar
    height: 64px
  &__toolbar-input
    width: 35%
  &__drawer-item
    line-height: 24px
    border-radius: 0 24px 24px 0
    margin-right: 12px
    .q-item__section--avatar
      padding-left: 12px
      .q-icon
        color: #5f6368
    .q-item__label:not(.q-item__label--caption)
      color: #3c4043
      letter-spacing: .01785714em
      font-size: .875rem
      font-weight: 500
      line-height: 1.25rem
    &--storage
      border-radius: 0
      margin-right: 0
      padding-top: 24px
      padding-bottom: 24px
  &__side-btn
    &__label
      font-size: 12px
      line-height: 24px
      letter-spacing: .01785714em
      font-weight: 500
  @media (min-width: 1024px)
    &__page-container
      padding-left: 94px
</style>