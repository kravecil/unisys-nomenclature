<script setup>
defineProps(['data'])
</script>

<template>
<q-item
    clickable
    class="q-my-sm item rounded-borders"
    :to="{name: 'requestDetails', params: { id: data.pk }}"
>
    <q-item-section>
        <q-item-label class="text-caption text-grey-5">{{ data.created_at }}</q-item-label>
        <q-item-label class="text-grey-4 text-weight-bold">{{ data.person_who_created?.shortname }}</q-item-label>
    </q-item-section>
    <q-item-section side class="text-primary text-weight-bold">
        <q-item-label lines="2">
            {{ data.product.name }}
        </q-item-label>
    </q-item-section>
</q-item>
</template>

<style scoped lang="sass">
.item
    background: #fff1
</style>