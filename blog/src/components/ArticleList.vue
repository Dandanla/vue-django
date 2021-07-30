作者：杜赛
链接：https://zhuanlan.zhihu.com/p/358612676
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

<!--  frontend/src/components/ArticleList.vue  -->

<template>
    <div v-for="article in info.results" v-bind:key="article.url" id="articles">
        <div>
            <span
                  v-for="tag in article.tags" 
                  v-bind:key="tag" 
                  class="tag"
            >
                {{ tag }}
            </span>
        </div>
        <div class="article-title">
            {{ article.title }}
        </div>
        <div>{{ formatted_time(article.created) }}</div>
    </div>

</template>

<script>
    import axios from 'axios';

    export default {
        name: 'ArticleList',
        data: function () {
            return {
                info: ''
            }
        },
        mounted() {
            axios
                .get('/api/article')
                .then(response => (this.info = response.data))
        },
        methods: {
            formatted_time: function (iso_date_string) {
                const date = new Date(iso_date_string);
                return date.toLocaleDateString()
            }
        }
    }

</script>

<!-- "scoped" 使样式仅在当前组件生效 -->
<style scoped>
    #articles {
        padding: 10px;
    }

    .article-title {
        font-size: large;
        font-weight: bolder;
        color: black;
        text-decoration: none;
        padding: 5px 0 5px 0;
    }

    .tag {
        padding: 2px 5px 2px 5px;
        margin: 5px 5px 5px 0;
        font-family: Georgia, Arial, sans-serif;
        font-size: small;
        background-color: #4e4e4e;
        color: whitesmoke;
        border-radius: 5px;
    }
</style>