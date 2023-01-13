<script setup>
import { ref, computed } from 'vue'
import { matCancel } from '@quasar/extras/material-icons'
const props = defineProps(['modelValue'])
const emit = defineEmits(['submit', 'update:modelValue'])

const data = computed({
    get() {
        return props.modelValue
    },
    set(val) {
        emit('update:modelValue', val)
    }
})

const submit = () => {
    emit('submit', data.value ?? '')
    // data.value = ''
}
</script>

<template>
    <q-form @submit="submit()">
        <q-input
            v-model="data"
            class="search"
            dense
            color="white"
            outlined
            autofocus
            :debounce="500"
            autofill="off"
            input-class="text-white"
            placeholder="поиск по базе"
        >
            <template v-if="data" v-slot:append>
                <q-icon :name="matCancel" @click.stop.prevent="data = ''" class="cursor-pointer" color="white" />
            </template>
        </q-input>
    </q-form>
</template>

<style scoped lang="sass">
.search :deep(.q-field__control)
    &:before
        border-color: $grey-6
</style>