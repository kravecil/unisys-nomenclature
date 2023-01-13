<script setup>
import { ref, onMounted, watch } from 'vue'
import { getGroups } from '@/api/core'

const emit = defineEmits(['select'])

const menuRef = ref(null)
const groups = ref([])
const group = ref(null)

onMounted(() => {
    getGroups()
    .then(response => groups.value = response)
})

watch(group, (val) => {
    emit('select', val)
    menuRef.value.hide()
})
</script>

<template>
<div class="text-white row items-center q-gutter-x-sm" id="group-select">
    <span v-if="group"><strong>Группа:</strong> {{ groups.find(i => i.pk==group)?.name }}</span>
    <span v-else>Группа не выбрана.</span>
    <span @click="menuRef.show()" class="cursor-pointer link">Выбрать группу</span>
    <span v-if="group" @click="group=null" class="cursor-pointer link">Показать всё</span>
    
    <q-menu square fit no-parent-event ref="menuRef" class="q-pa-md bg-grey-10">
        <!-- 
            TODO: Добавить фильтр
         -->
        <q-tree
            text-color="white"
            :nodes="groups.filter(i => !i.parent_group)"
            node-key="pk"
            label-key="name"
            v-model:selected="group"
            selected-color="primary"
        />
    </q-menu>
</div>
</template>

<style scoped lang="sass">
@import 'quasar/src/css/variables.sass'
.tree
    border: 1px solid $grey-8
.link
    text-decoration: underline
    transition-duration: 200ms
    &:hover
        color: $primary
</style>