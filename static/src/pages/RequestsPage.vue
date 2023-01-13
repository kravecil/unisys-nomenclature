<script setup>
import { ref, onMounted } from 'vue'
import { getRequests } from '@/api/core'
import RequestItem from '@/components/RequestItem.vue'

const requests = ref([])
const infRef = ref(null)

let page = 1
const reset = () => {
    page = 1
    requests.value = []

    infRef.value?.reset()
    infRef.value?.poll()
    infRef.value?.resume()
}

onMounted(() => reset())

const onLoad = (index, done) => {
    getRequests(page)
    .then(response => {
        for (const item of response.results) requests.value.push(item)
        page++

        if (!response.has_next) infRef.value?.stop()

        done()
    })
}
</script>

<template>
<q-page padding class="row">
    <div class="column col WAL q-mx-auto q-gutter-y-md q-pa-md">
        <div class="text-h6 text-grey-6">Заявки</div>
        <q-scroll-area class="col" dark>
            <q-infinite-scroll ref="infRef" @load="onLoad">
                <request-item
                    v-for="request in requests" :key="request.pk"
                    :data="request"
                />
                <template v-slot:loading>
                    <div class="row justify-center q-my-md">
                    <q-spinner-dots color="primary" size="40px" />
                    </div>
                </template>
            </q-infinite-scroll>
        </q-scroll-area>
    </div>
</q-page>
</template>

<style scoped lang="sass">
.WAL
    width: 100%
    max-width: 800px
</style>