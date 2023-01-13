<script setup>
defineProps(['data'])
</script>

<template>
<q-item
    clickable
    class="q-my-sm item rounded-borders"
    :to="{name: data.approved_at?'productDetails':'requestDetails', params: { id: data.pk }}"
>
    <q-item-section>
        <q-item-label class="text-deep-orange">
            <q-item-label lines="2"  class="text-weight-bold">{{ data.product?.name }}</q-item-label>
        </q-item-label>
        <q-item-label caption class="text-grey-5">
            {{ data.product?.number }}
        </q-item-label>
    </q-item-section>
    <q-item-section side top class="text-caption">{{ data.created_at}}</q-item-section>
    <q-tooltip :delay="500">{{ data.product?.name }}</q-tooltip>
</q-item>
</template>

<style scoped lang="sass">
.item
    background: #fff1
</style>