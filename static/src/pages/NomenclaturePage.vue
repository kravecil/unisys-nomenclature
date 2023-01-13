<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getProducts } from '@/api/core'
import NomenclatureItem from '@/components/NomenclatureItem.vue'
import SearchField from '@/components/SearchField.vue'
// import GroupSelect from '@/components/GroupSelect.vue'

const route = useRoute()
// const ac = new AbortController()

const search = ref(route.query.search ?? '')
const products = ref([])
const infRef = ref(null)
const group = ref(undefined)

watch(search, () => reset())

let page = 1
const reset = () => {
    page = 1
    products.value = []

    infRef.value?.reset()
    infRef.value?.poll()
    infRef.value?.resume()
}

onMounted(() => reset())

const groupChanged = (e) => {
    group.value = e
    reset()
}

const onLoad = async (index, done) => {
    // ac.abort()
    const response = await axios(
        `/api/products/?page=${page}&search=${search.value}&group=${group.value ?? ''}`,
        // {signal: ac.signal}
    )

    for (const item of response.data.results) products.value.push(item)
    page++

    if (!response.data.has_next)infRef.value?.stop()

    done()
}
</script>

<template>
<q-page padding class="row">
    <div class="column col WAL q-mx-auto q-gutter-y-md q-pa-md">
        <div class="text-h6 text-grey-6">Номенклатурные номера</div>
        <search-field class="col-auto" @submit="(s) => search=s" v-model="search" />
        <!-- <group-select @select="groupChanged"/> -->
        <q-scroll-area class="col" dark>
            <q-infinite-scroll ref="infRef" @load="onLoad">
                <nomenclature-item
                    v-for="product in products" :key="product.pk"
                    :data="product"
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