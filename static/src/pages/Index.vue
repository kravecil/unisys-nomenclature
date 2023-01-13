<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getSummary } from '@/api/core'
import SearchField from '@/components/SearchField.vue'
import CardSummary from '@/components/CardSummary.vue'

const router = useRouter()

const summary = ref({})
const loading = ref(false)
const search = ref('')

onMounted(() => {
    loading.value = true
    getSummary()
    .then(response => summary.value = response)
    .finally(() => loading.value = false)
})

const submit = (e) => {
    console.log(e)
    router.push({name:'nomenclature', query: { search: e }})
}
</script>

<template>
<q-page class="column justify-center items-center">
    <div class="column">
        <search-field @submit="submit" v-model="search" />
        <div class="q-gutter-lg row q-py-lg no-wrap">
            <card-summary title="Недавние добавленные" :data="summary.recentApproved" :loading="loading" />
            <card-summary title="Недавние заявки" :data="summary.recentCreated" :loading="loading" />
            <card-summary title="Самые просматриваемые" :data="summary.mostPopular" :loading="loading" />
        </div>
    </div>
</q-page>
</template>