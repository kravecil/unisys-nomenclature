<script setup>
import { matEdit } from '@quasar/extras/material-icons'
import { user } from '@/api/auth'
import { useRouter } from 'vue-router'
import PersonItem from '@/components/PersonItem.vue'

const { request, isRequest } = defineProps(['request', 'isRequest'])

const router = useRouter()

const change = () => {
    router.push({name: 'updateRequest', params: { id: request.pk }})
}
</script>

<template>
<!-- TODO: карточка изделия и карточка запроса в один ряд -->
<div class="q-gutter-y-lg">
    <div class="product-title q-pa-md relative-position q-gutter-y-sm">
        <q-btn
            v-if="user.id==request.person_who_created.pk && !request.approved_at"
            class="q-mb-md"
            @click="change()"
            no-caps label="Изменить" :icon="matEdit" size="sm" outline />

        <div class="text-h5 text-grey-6">{{ request.product.number}}</div>
        <div class="row items-center q-gutter-md">
            <div class="text-h4 text-primary text-weight-bold">{{ request.product?.name }}</div>
            <q-chip
                v-if="request.product.unit_rel"
                :label="request.product.unit_rel.shortname"
                color="primary"
                size="sm" square
                text-color="white" class="text-weight-bold"
            />
        </div>
        <q-separator dark />
        <div v-if="request.product.okpd_rel" class="q-gutter-x-sm">
            <span class="text-weight-bold">ОКПД2:</span>
            <span>{{ request.product.okpd_rel.name }}</span>
            <span class="text-weight-bold">/ {{ request.product.okpd_rel.code }} /</span>
        </div>
        <div v-if="request.product.okved_rel" class="q-gutter-x-sm">
            <span class="text-weight-bold">ОКВЕД2:</span>
            <span>{{ request.product.okved_rel.name }}</span>
            <span class="text-weight-bold">/ {{ request.product.okved_rel.code }} /</span>
        </div>
        <div v-if="request.product.notes" class="pre-line text-grey-3 text-weight-thin">
            <div class="text-weight-bold">Технические характеристики:</div>
            <div>{{ request.product.notes }}</div>
        </div>
        <q-separator dark v-if="request.product.ens_rel" />
        <div v-if="request.product.ens_rel" class="row">
            <div class="q-gutter-x-sm ">
                <span>Привязка к ЕНС:</span>
                <span class="text-weight-thin">{{ request.product.ens_rel.number }}</span>
                <span class="text-primary">{{ request.product.ens_rel.name }}</span>
                <q-tooltip>
                    <div class="column">
                        <span><b>ОКПД2:</b> {{ request.product.ens_rel.okpd }}</span>
                        <span><b>ОКВЭД2:</b> {{ request.product.ens_rel.okved }}</span>
                        <div class="pre-line">{{ request.product.ens_rel.notes }}</div>
                    </div>
                </q-tooltip>
            </div>
        </div>

        <div v-if="!request.approved_at" class="absolute-top-right q-pa-xs text-dense bg-orange">Ожидает проверки</div>
        <div v-else class="absolute-top-right q-pa-xs text-dense bg-green">Одобрено</div>
    </div>
    <router-link
        v-if="!isRequest"
        class="text-white text-dense"
        :to="{name: 'requestDetails', params: {id: request.pk }}"
    >
        Посмотреть запрос
    </router-link>
    <div v-if="isRequest" class="col column text-weight-light">
        <div class="text-h6">Запрос</div>
        <q-separator dark />
        <person-item
            :name="request.person_who_created?.shortname"
            :date="request.created_at"
            :state="'request'"
        />
        <div v-if="request.approvers_left.length>0">
            <div class="text-h6">Без визы</div>
            <q-separator dark />
            <person-item
                v-for="approver in request.approvers_left" :key="approver.pk"
                :name="approver.person.shortname"
                :state="'waiting'"
            />
        </div>
        <div v-if="request.approvements.length>0 && request.approvements.some(i=>i.approved_at)">
            <div class="text-h6">Согласовано</div>
            <q-separator dark />
            <div v-for="approvement in request.approvements" :key="approvement.pk">
                <person-item
                    v-if="approvement.approved_at"
                    :name="approvement.approver.person.shortname"
                    :date="approvement.approved_at"
                    :comment="approvement.comment"
                    :state="'approved'"
                />
            </div>
        </div>
        <div v-if="request.approvements.length>0 && request.approvements.some(i=>i.rejected_at)">
            <div class="text-h6">Отклонено</div>
            <q-separator dark />
            <div  v-for="approvement in request.approvements" :key="approvement.pk">
                <person-item
                    v-if="approvement.rejected_at"
                    :name="approvement.approver.person.shortname"
                    :date="approvement.rejected_at"
                    :comment="approvement.comment"
                    :state="'rejected'"
                />
            </div>
        </div>
    </div>
</div>
</template>

<style scoped lang="sass">
.product-title
    border: 1px solid $grey-8
    border-left: 1em solid $primary
    background: #fff1
</style>