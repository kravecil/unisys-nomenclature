<script setup>
import { matDone, matHelpOutline, matDescription, matHighlightOff } from '@quasar/extras/material-icons'
const props = defineProps(['name', 'date', 'state', 'comment'])
const icons = {
    'request': [matDescription, 'white'],
    'approved': [matDone, 'green'],
    'waiting': [matHelpOutline, 'yellow'],
    'rejected': [matHighlightOff, 'red'],
}
// console.log(props.state)
// console.log(icons['request'][1])
</script>

<template>
<q-item dark>
    <q-item-section avatar>
        <q-icon :name="icons[state][0]" size="sm" :color="icons[state][1]" />
    </q-item-section>
    <q-item-section>
        <q-item-label class="text-bold" >{{ name }}</q-item-label>
        <q-item-label caption>{{ date }}</q-item-label>
    </q-item-section>
    <q-item-section>
        <q-item-label caption>{{ comment }}</q-item-label>
    </q-item-section>
</q-item>
</template>