<template>
    <div class="row" justify-evenly>
        <div class="col-6">
            <div v-for="article in info.results" v-bind:key="article.url" id="articles">
                <q-card class="my-card">
                    <q-parallax v-bind:src="article.avatar.content" style="" :height="200" />
                        <q-card-section>
                            <div class="text-h6" 
                            align="left"
                            >
                            {{ article.title }}
                            </div>
                            <div class="text-subtitle2"
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
                            <q-btn flat color="primary"
                            v-on:click.prevent="Read(article.id)"
                            >Read More</q-btn>
                        </q-card-actions>
                    </q-card-section>

                </q-card>

                <q-separator />

            </div>
        </div>

        <div class="col-4">
            <div class="text-h6" style="margin:10px">友链</div>
            <div class="text-h7" style="margin:10px">淡淡</div>
            <div class="text-h7" style="margin:10px">李恒道</div>
            <div class="text-h7" style="margin:10px">南国旧梦</div>
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
            },
            Read :function (iso_date_string) {
                this.$router.push({path:"/article/" + iso_date_string});
            }
        },
    }

</script>

<!-- "scoped" 使样式仅在当前组件生效 -->
<style scoped>
    #articles {

        padding-bottom: 10px;
    }
    .col-6 {
        margin-left: 250px;
        /* margin: 0 auto; */
        padding-top: 20px;
    }

    .my-card {
        width: 100%;
        max-width: 600px;
    }


</style>