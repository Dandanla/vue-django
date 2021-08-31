<template>

    <BlogHeader/>

    <div id="grid">
        <div id="signup">
            <h3>注册账号</h3>
            <form>
                <div class="form-elem">
                    <span>账号：</span>
                    <input v-model="signupName" type="text" placeholder="输入用户名">
                </div>

                <div class="form-elem">
                    <span>密码：</span>
                    <input v-model="signupPwd" type="password" placeholder="输入密码">
                </div>

                <div class="form-elem">
                    <button v-on:click.prevent="signup">提交</button>
                </div>
            </form>
        </div>
    </div>


    <BlogFooter/>

</template>

<script>
    import axios from 'axios';
    import BlogHeader from '../components/BlogHeader.vue'
    import BlogFooter from '../components/BlogFooter.vue'


    export default {
        name: 'Login',
        components: {BlogHeader, BlogFooter},
        data: function () {
            return {
                signupName: '',
                signupPwd: '',
                signupResponse: null,
            }
        },
        methods: {
            signup() {
                const that = this;
                axios
                    .post('/api/user/', {
                        username: this.signupName,
                        password: this.signupPwd,
                    })
                    .then(function (response) {
                        that.signupResponse = response.data;
                        alert('用户注册成功，快去登录吧！');
                    })
                    .catch(function (error) {

                        alert(error.message);

                        // Handling Error here...

                        // https://github.com/axios/axios#handling-errors

                    });
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
        display: grid;
        margin: 0 auto;
    }

    #signup {
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