<script setup>
import NomenclatureItem from '@/components/NomenclatureItem.vue'
defineProps(['title', 'data', 'loading'])
</script>

<template>
<q-card square class="card relative-position">
    <q-card-section class="card-title">
        <div class=" text-grey-5">{{ title }}</div>
    </q-card-section>
    <q-separator color="grey-7" />
    <q-card-section>
        <nomenclature-item
            v-for="item in data" :key="item.pk"
            :data="item"
        />
    </q-card-section>
    <q-inner-loading :showing="loading" />
</q-card>
</template>

<style scoped lang="sass">
.card
    // width: 100%
    // max-width: 400px
    width: 350px
    background: #fff2
.card-title
    // background: #bbb
</style>