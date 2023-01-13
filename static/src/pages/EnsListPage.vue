<script setup>
import { ref, watch, onMounted } from 'vue'

onMounted(() => reset())

const search = ref('')
watch(search, () => reset())

let page = 1
const infRef = ref(null)
const reset = () => {
    page = 1
    enses.value = []

    infRef.value?.reset()
    infRef.value?.poll()
    infRef.value?.resume()
}

const enses = ref([])
const onLoad = async (index, done) => {
    const response = await axios.get(`/api/enses?page=${page}&search=${search.value ?? ''}`)

    for (const item of response.data.results) enses.value.push(item)
    page++

    if (!response.data.has_next)infRef.value?.stop()

    done()
}
</script>

<template>
<q-page padding class="row">
    <div class="col column q-gutter-y-md">
        <div class="text-h6 text-grey-6">Единый номенклатурный справочник ГК "Ростех"</div>
        <div class="col-auto">
            <q-input v-model="search" dark clearable outlined dense label="поиск" :debounce="500" />
        </div>

        <div class="col-auto row q-ma-none">
            <div class="table-cell">Код</div>
            <div class="table-cell">Наименование</div>
            <div class="table-cell">Ед.изм</div>
            <div class="table-cell">ОКПД2</div>
            <div class="table-cell">ОКВЭД2</div>
            <div class="table-cell pre-line">Технические характеристики</div>
        </div>
        
        <q-scroll-area dark class="col column">
            <q-infinite-scroll ref="infRef" @load="onLoad" class="col column">
                <div v-for="ens in enses" :key="ens.id" class="row table-row">
                    <div class="table-cell">{{ ens.number }}</div>
                    <div class="table-cell">{{ ens.name }}</div>
                    <div class="table-cell">{{ ens.unit }}</div>
                    <div class="table-cell">{{ ens.okpd }}</div>
                    <div class="table-cell">{{ ens.okved }}</div>
                    <div class="table-cell pre-line">{{ ens.notes }}</div>
                </div>
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
// @import 'quasar/src/css/variables.sass'
.table-row
    background: linear-gradient(to right, #fff1, #fff2)
    margin: .5em 0
    border: 1px solid $grey-9
    border-radius: 5px
.table-cell
    color: $grey-4
    padding: 1em 1em
    font-size: .9em
    &:nth-child(1) // код
        width: 10%
        text-align: center
    &:nth-child(2) // наименование
        width: 30%
        font-weight: bold
    &:nth-child(3) // единицы измерения
        width: 5%
    &:nth-child(4) // ОКПД2
        width: 10%
    &:nth-child(5) // ОКВЭД2
        width: 10%
    &:nth-child(6) // технические характеристики
        width: 35%
</style>