<template>
    <div v-for="article in info.results" v-bind:key="article.url" id="articles">
        <q-card class="my-card">
            <q-img src="http://www.dandanla.cn/wp-content/uploads/2020/07/image-1.png" style=""></q-img>
                <q-card-section>
                    <div class="text-h6" 
                    style="padding-left: 10px;"
                    >
                    {{ article.title }}
                    </div>
                    <div class="text-subtitle2"
                    style="padding-left: 50px;"
                    @click="111"
                    >
                    {{ formatted_time(article.created) }}
                    </div>
                <q-card-actions align="right">
                    <q-btn flat
                    v-for="tag in article.tags" 
                    v-bind:key="tag" 
                    >
                    {{ tag }}
                    </q-btn>
                    <q-btn flat color="primary">Read More</q-btn>
                </q-card-actions>
            </q-card-section>

        </q-card>

        <q-separator />

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
        padding-left: 200px;
        padding-bottom: 10px;
    }

    .my-card {
        width: 100%;
        max-width: 350px;
    }


</style>