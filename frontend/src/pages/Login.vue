<template>

    <div id="grid">
        <div id="signin">
            <div class="text-h3">登录账号</div>
            <form>
                <div class="form-elem">
                    <span>账号：</span>
                    <input v-model="signinName" type="text" placeholder="输入用户名">
                </div>

                <div class="form-elem">
                    <span>密码：</span>
                    <input v-model="signinPwd" type="password" placeholder="输入密码">
                </div>

                <div class="form-elem">
                    <button v-on:click.prevent="signin">登录</button>
                </div>
            </form>
        </div>
    </div>


    <BlogFooter/>

</template>

<script>
    import axios from 'axios';
    import BlogFooter from '../components/BlogFooter.vue'


    export default {
        name: 'Login',
        components: {BlogFooter},
        data: function () {
            return {
                signinName: '',
                signinPwd: '',
                signupResponse: null,
            }
        },
        methods: {
            signin() {
                const that = this;
                axios
                    .post('/api/token/', {
                        username: that.signinName,
                        password: that.signinPwd,
                    })
                    .then(function (response) {
                        const storage = localStorage;
                        // Date.parse(...) 返回1970年1月1日UTC以来的毫秒数
                        const expiredTime = Date.parse(response.headers.date) + 60 * 100 * 1000;
                        // 设置 localStorage
                        storage.setItem('access.myblog', response.data.access);
                        storage.setItem('refresh.myblog', response.data.refresh);
                        storage.setItem('expiredTime.myblog', expiredTime);
                        storage.setItem('username.myblog', that.signinName);

                        // 是否为管理员
                        axios
                            .get('/api/user/' + that.signinName + '/')
                            .then(function (response) {
                                storage.setItem('isSuperuser.myblog', response.data.is_superuser);
                                // 路由跳转
                                alert('用户登陆成功！');
                                that.$router.push({name: 'Home'});
                            });
                            // .catch(...)
                    })
                // .catch(...)
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

            // 初始 token 未过期
            if (expiredTime > current) {
                alert('用户已登陆！');
                that.$router.push({name: 'Home'});

            }
            },
    }
</script>

<style scoped>

    #grid {
        padding-top: 200px;
        display: grid;
        margin: 0 auto;
    }

    #signin {
        text-align: center;
    }

    .form-elem {
        padding: 10px;
    }

    input {
        height: 25px;
        padding-left: 10px;
    }

    button {
        height: 35px;
        cursor: pointer;
        border: none;
        outline: none;
        background: gray;
        color: whitesmoke;
        border-radius: 5px;
        width: 60px;
    }
</style>