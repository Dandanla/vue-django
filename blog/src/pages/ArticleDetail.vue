
<template>

    <BlogHeader/>

    <div v-if="article !== null" class="grid-container">
        <div>
            <q-card class="my-card" flat bordered>
            <q-item>
                <q-item-section avatar>
                <q-avatar>
                    <img src="https://cdn.quasar.dev/img/boy-avatar.png">
                </q-avatar>
                </q-item-section>

                <q-item-section>
                <q-item-label>{{article.title}}</q-item-label>
                <q-item-label caption>
                    本文由 {{ article.author.username }} 发布于 {{ formatted_time(article.created) }}
                </q-item-label>
                </q-item-section>
            </q-item>

            <q-separator />

            <q-card-section horizontal>

                <q-separator vertical />

                <q-card-section v-html="article.body_html">
                </q-card-section>
            </q-card-section>
            </q-card>
        </div>
    </div>

    <BlogFooter/>

</template>

<script>
    import BlogHeader from '../components/BlogHeader.vue'
    import BlogFooter from '../components/BlogFooter.vue'

    import axios from 'axios';


    export default {
        name: 'ArticleDetail',
        components: {BlogHeader, BlogFooter},
        data: function () {
            return {
                article: null
            }
        },
        mounted() {
            axios
                .get('/api/article/' + this.$route.params.id)
                .then(response => (this.article = response.data))
        },
        methods: {
            formatted_time: function (iso_date_string) {
                const date = new Date(iso_date_string);
                return date.toLocaleDateString()
            }
        }
    }
</script>

<style scoped>
    .grid-container {
        display: grid;
    }


    .my-card{
        width: 100%;
        height: 100%;
        max-width: 1000px;
        max-height: 1000px;
        margin: 0 auto;
    }

    #subtitle {
        text-align: center;
        color: gray;
        font-size: small;
    }

</style>

<style>
    .article-body p img {
        max-width: 100%;
        border-radius: 50px;
        box-shadow: gray 0 0 20px;
    }

    .toc ul {
        list-style-type: none;
    }

    .toc a {
        color: gray;
    }
</style>
