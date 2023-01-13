<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { Loading } from 'quasar'
import { user } from '@/api/auth'
import { refreshStats } from '@/api/core'
import { useRoute } from 'vue-router'
import ProductDetails from '@/components/ProductDetails.vue'

const route = useRoute()
watch(route, (val) => {
    if (val.name=='productDetails' || val.name=='requestDetails') refresh()
})

const isRequest = computed(() => route.name=='requestDetails')
const isApproved = computed(() => product.value.approved_at)

const product = ref(null)
const refresh = async () => {
    Loading.show({message: 'Получение информации о запросе...'})
    product.value = null
    let model = 'requests'
    if (!isRequest.value) model = 'products'
    const response = await axios.get(`/api/${model}/${route.params.id}`)
    product.value = response.data

    if (isRequest.value) {
        const approvement = product.value.approvements.find(i => i.approver.person.pk == user.value.id)
        if (approvement !=undefined) {
            if (approvement.approved_at != null) choice.value = 1
            if (approvement.rejected_at != null) choice.value = -1
            comment.value = approvement.comment
        } else choice.value = 0
    }

    refreshStats()

    Loading.hide()
}

const choices = [
    {label: 'Не выбрано', value: 0},
    {label: 'Согласовать', value: 1},
    {label: 'Отказать', value: -1},
]
const choice = ref(0)
const choiceUpdated = (val) => {
    axios.post(`/api/requests/${product.value.pk}/change-approvement/`, {
        state: val,
        comment: comment.value ?? ''
    })
    .then(() => refresh())
}

const comment = ref('')
onMounted(() => refresh())
</script>

<template>
<q-page padding>
    <div class="product-details">
        <q-banner
            class="bg-grey-8 text-white"
            v-if="isRequest && product?.approvers_all.some(i => i.person.pk==user.id) && !isApproved"
        >
            Выберите или измените вашу визу
            <template v-slot:action>
                <q-input
                    class="custom-border"
                    v-model="comment"
                    dense
                    clearable
                    outlined
                    label="Комментарий"
                    label-color="grey-5"
                    input-class="text-white"
                />
                <q-separator dark vertical inset class="q-mx-md" />
                <q-btn-toggle
                    v-model="choice"
                    :options="choices"
                    flat
                    dense
                    no-caps
                    @update:model-value="choiceUpdated"
                />
            </template>
        </q-banner>
        <div class="q-gutter-x-lg text-white">
            <!-- ДЕТАЛИ ИЗДЕЛИЯ -->
            <product-details
                v-if="product"
                :request="product"
                :is-request="route.name=='requestDetails'"
            />
            
            <!-- <q-separator vertical color="grey-8" /> -->
            
            <!-- ДИСКУССИЯ -->
            <!-- <div class="col">тут будет чат, обмен мгновенными сообщениями и история</div> -->
        </div>
    </div>
</q-page>
</template>

<style scoped lang="sass">
.product-details
    width: 100%
    max-width: 1170px
    margin: 0 auto
.custom-border :deep(.q-field__control)
    &:before
        border-color: $grey-6
</style>