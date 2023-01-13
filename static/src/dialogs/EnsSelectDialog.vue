<script setup>
import { ref, watch } from 'vue'
import { useDialogPluginComponent } from 'quasar'

defineProps()
defineEmits([
  ...useDialogPluginComponent.emits
])
const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()

const search = ref('')
watch(search, (val) => refresh())

const importData = ref(false)

let page = 1
const infRef = ref(null)
const refresh = () => {
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


function onSelect (ens) {
    onDialogOK({
        importData: importData.value,
        ens
    })
}
</script>

<template>
<q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="dialog q-pa-lg bg-grey-4">
        <q-card-section class="text-h6">Справочник ЕНС</q-card-section>
        <q-card-section>
            <q-input
                v-model="search"
                clearable
                label="быстрый поиск..."
                outlined
                dense
                :debounce="500"
            />
        </q-card-section>
        <q-card-section>
            <q-scroll-area class="scroll-area">
                <q-infinite-scroll ref="infRef" @load="onLoad">
                    <q-list ordered square>
                        <q-item
                            v-for="ens in enses" :key="ens.code"
                            clickable
                            @click="onSelect(ens)">
                            <q-item-section>
                                <q-item-label class="text-weight-bold text-deep-orange-10">
                                    {{ ens.name }}
                                </q-item-label>
                                <q-item-label caption>{{ ens.unit }}</q-item-label>
                                <q-item-label caption>
                                    <span class="text-weight-bold">ОКПД2: </span>{{ ens.okpd }}
                                </q-item-label>
                                <q-item-label caption>
                                    <span class="text-weight-bold">ОКВЭД2: </span>{{ ens.okved }}
                                </q-item-label>
                            </q-item-section>
                            <q-tooltip><div class="pre-line">{{ ens.notes }}</div></q-tooltip>
                        </q-item>
                    </q-list>
                    <template v-slot:loading>
                        <div class="row justify-center q-my-md">
                            <q-spinner-dots color="primary" size="40px" />
                        </div>
                    </template>
                </q-infinite-scroll>
            </q-scroll-area>
        </q-card-section>
        <q-card-actions align="right">
            <q-checkbox v-model="importData" label="заполнить форму заявки выбранными значениями" />
        </q-card-actions>
    </q-card>
</q-dialog>
</template>

<style scoped lang="sass">
.dialog
    width: 800px
    // height: 100%
    // max-height: 700px
.scroll-area
    height: 400px
</style>