<script setup>
import { ref, onMounted } from 'vue'
import { matInfo, matWarning, matCancel } from '@quasar/extras/material-icons'
import { useRouter, useRoute } from 'vue-router'
import { Loading, Dialog } from 'quasar'
import { refreshStats } from '@/api/core'
import NomenclatureItem from '@/components/NomenclatureItem.vue'
import EnsSelectDialog from '@/dialogs/EnsSelectDialog.vue'

const router = useRouter()
const route = useRoute()

const isUpdate = ref(false)

const name = ref('')
const notes = ref('')

const similars = ref([])
const acSimilars = new AbortController()
const getSimilars = () => {
    // acSimilars.abort()
    const search = [name.value/* , notes.value */].join(' ')
    axios.get(`/api/products?similars=1&search=${search}`, { signal: acSimilars.signal })
    .then(response => {
        similars.value = response.data
    })
}

onMounted(()=>{
    getUnits()
    getOkpds()
    getOkveds()
    // getEnses()

    if (route.name=='updateRequest') {
        Loading.show({message: 'Получение значения полей'})
        isUpdate.value = true
        axios.get(`/api/requests/${route.params.id}`)
        .then(response => {
            name.value = response.data.product.name
            notes.value = response.data.product.notes
            unit.value = response.data.product.unit_rel
            okpd.value = response.data.product.okpd_rel
            okpd_initial = okpd.value?.code
            okved.value = response.data.product.okved_rel
            ens.value = response.data.product.ens_rel
        })
        .finally(() => Loading.hide())
    }
})

const unit = ref(null)
const units = ref([])
const optionsUnits = ref([])
const getUnits = () => {
    axios.get('/api/units')
    .then(response => units.value = response.data)
}
const filterUnits = (val, update) => {
    update(() => {
        const needle = val.toLowerCase()
        optionsUnits.value = units.value.filter(v =>
            v.name.toLowerCase().includes(needle) ||
            v.shortname.toLowerCase().includes(needle)
        )
    })
}

let okpd_initial = null
const okpd = ref(null)
const okpds = ref([])
const optionsOkpds = ref([])
const getOkpds = () => {
    axios.get('/api/okpds')
    .then(response => okpds.value = response.data)
}
const filterOkpds = (val, update) => {
    update(() => {
        const needle = val.toLowerCase()
        optionsOkpds.value = okpds.value.filter(v =>
            v.code.includes(needle) ||
            v.name.toLowerCase().includes(needle)
        )
    })
}

const okved = ref(null)
const okveds = ref([])
const optionsOkveds = ref([])
const getOkveds = () => {
    axios.get('/api/okveds')
    .then(response => okveds.value = response.data)
}
const filterOkveds = (val, update) => {
    update(() => {
        const needle = val.toLowerCase()
        optionsOkveds.value = okveds.value.filter(v =>
            v.code.includes(needle) ||
            v.name.toLowerCase().includes(needle)
        )
    })
}

const ens = ref(null)
const selectEnsDialog = () => {
    Dialog.create({ component: EnsSelectDialog, })
    .onOk(response => {
        ens.value = response.ens
        if (response.importData) {
            name.value = response.ens.name
            notes.value = response.ens.notes
            unit.value = units.value.find(i=>i.shortname==response.ens.unit)
            okpd.value = okpds.value.find(i=>i.code==response.ens.okpd)
            okved.value = okveds.value.find(i=>i.code==response.ens.okved)
        }
    })
}

const submit = () => {
    if (isUpdate.value && okpd_initial != okpd.value?.code) {
        Dialog.create({
            message: 'Значение ОКПД2 было изменёно.<br>Сгенерировать новый номенклатурный номер?',
            html: true,
            cancel: { label: 'Нет' },
            persistent: true,
        })
        .onOk(() => save(true))
        .onCancel(() => save(false))
        .onDismiss(() => save(false))
    } else save(false)
}
const save = (generate = false) => {
    Loading.show({message: 'Формирование заявки... Подождите.'})
    let url = '/api/requests/'
    let method = 'post'
    if (isUpdate.value) {
        url = `/api/requests/${route.params.id}/`
        method = 'put'
    }
    axios.request({method, url, data: {
        generate,
        product: {
            name: name.value,
            notes: notes.value,
            unit: unit.value?.code ?? '',
            okpd: okpd.value?.code ?? '',
            okved: okved.value?.code ?? '',
            ens: ens.value?.number ?? '',
        }
    }})
    .then(response => {
        refreshStats()
        router.push({name: 'requestDetails', params: { id: response.data.pk }})
    })
    .finally(() => Loading.hide())
    // router.push({name: 'productDetails', params: { productId: 123 }})
    // Loading.show({message: 'Создание заявки... Подождите.'})
}
</script>

<template>
<div class="full-width row text-white  q-pa-md">
    <div class="column col-8 q-gutter-y-md">
        <div>
            <div class="text-h6 text-grey-6">{{ isUpdate? 'Изменение заявки':'Новая заявка'}}</div>
            <div class="text-h6 text-caption">на добавление номенклатурного номера</div>
        </div>

        <q-item dense class="bg-grey-4 rounded-borders text-black">
            <q-item-section avatar><q-icon :name="matInfo" /></q-item-section>
            <q-item-section>
                Номенклатурный номер присваивается автоматически и недоступен для редактирования.
            </q-item-section>
        </q-item>

        <q-item v-if="isUpdate" dense class="bg-warning rounded-borders text-black">
            <q-item-section avatar><q-icon :name="matWarning" /></q-item-section>
            <q-item-section>
                После изменения заявки все одобрительные визы аннулируются.
            </q-item-section>
        </q-item>

        <q-form
            @submit="submit"
            class="q-gutter-y-md col"
        >
            <q-input
                class="input-custom"
                v-model="name"
                label="Наименование"
                label-color="grey-6"
                input-class="text-white"
                outlined
                autofocus
                :debounce="500"
                @update:model-value="getSimilars()"
                :rules="[val=>!!val || 'Обязательно поле']"
            />
            <q-input
                class="input-custom"
                v-model="notes"
                type="textarea"
                label="Технические характеристики"
                label-color="grey-6"
                input-class="text-white"
                outlined
                :debounce="500"
                @update:model-value="getSimilars()"
                :rules="[val=>!!val || 'Обязательно поле']"
            />
            <q-select
                class="input-custom"
                label-color="grey-6"
                label="Единицы измерения"
                v-model="unit"
                :options="optionsUnits"
                option-label="name"
                @filter="filterUnits"
                use-input 
                outlined dark clearable dense
            />
            <q-select
                class="input-custom"
                label-color="grey-6"
                label="ОКПД2"
                v-model="okpd"
                :options="optionsOkpds"
                option-label="name"
                @filter="filterOkpds"
                use-input 
                outlined dark clearable dense
            />
            <q-select
                class="input-custom"
                label-color="grey-6"
                label="ОКВЭД2"
                v-model="okved"
                :options="optionsOkveds"
                option-label="name"
                @filter="filterOkveds"
                use-input 
                outlined dark clearable dense
            />
            <div class="row q-gutter-md">
                <q-space />
                <q-item v-if="ens" dense class="col">
                    <q-item-section side>Привязка к ЕНС:</q-item-section>
                    <q-separator vertical dark spaced />
                    <q-item-section>
                        <q-item-label caption  class="text-grey-6">{{ ens.number }}</q-item-label>
                        <q-item-label lines="2" class="text-primary text-weight-bold">
                            {{ ens.name }}
                        </q-item-label>
                    </q-item-section>
                    <q-item-section side>
                        <q-btn :icon="matCancel" dark @click="ens = null" />
                    </q-item-section>
                    <q-tooltip :delay="500">
                        <div class="column">
                            <div class="text-weight-bold">{{ ens.name }}</div>
                            <div>ОКПД2: {{ ens.okpd }}</div>
                            <div>ОКВЭД2: {{ ens.okved }}</div>
                            <div class="pre-line">{{ ens.notes }}</div>
                        </div>
                    </q-tooltip>
                </q-item>
                <q-btn
                    label="Привязать ЕНС..."
                    color="grey-8"
                    no-caps
                    class="self-center"
                    @click="selectEnsDialog()"
                />
                <q-btn
                    label="Отправить"
                    color="green"
                    class="self-center"
                    type="submit"
                    no-caps
                />
            </div>
        </q-form>
    </div>
    <transition
        enter-active-class="animate__animated animate__fadeIn animate__faster"
        leave-active-class="animate__animated animate__fadeOut animate__faster">
        <div class="col q-pa-lg" v-if="similars.length">
            <q-item>
                <q-item-section avatar>
                    <q-icon :name="matInfo" size="lg" color="yellow" />
                </q-item-section>
                <q-item-section class="text-weight-bold text-yellow">
                    Возможно, номенклатура уже присутствует в системе:
                </q-item-section>
            </q-item>
            <nomenclature-item
                v-for="request in similars" :key="request.pk"
                :data="request"
            />
        </div>
    </transition>
</div>
</template>

<style scoped lang="sass">
.WAL
    width: 100%
    max-width: 800px
    // background: #fff2
.input-custom :deep(.q-field__control)
    &:before
        border-color: $grey-6
</style>