<template>
    <div class="row" justify-evenly>
        <div class="col-6">
            <div v-for="article in info.results" v-bind:key="article.url" id="articles">
                <q-card class="my-card">
                    <q-parallax src="https://cdn.quasar.dev/img/parallax1.jpg" style="" :height="200" />
                        <q-card-section>
                            <div class="text-h6" 
                            align="left"
                            >
                            {{ article.title }}
                            </div>
                            <div class="text-subtitle2"
                            v-on:click.prevent=""
                            }
                            align="left"
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
        </div>

        <div class="col-4">
        友链
        </div>
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

        padding-bottom: 10px;
    }
    .col-6 {
        margin: 0 auto;
    }

    .my-card {
        width: 100%;
        max-width: 500px;
    }


</style>