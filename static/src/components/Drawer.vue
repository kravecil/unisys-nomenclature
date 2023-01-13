<script setup>
import { ref } from 'vue'
import { user } from '@/api/auth'

const drawer = ref(true)

const go = (url, isDisabled = false) => {
  if (isDisabled) return
  window.location = url
}
</script>

<template>
<q-drawer
  v-model="drawer"
  side="right"
  bordered
  elevated
  class="bg-grey-3 q-pa-lg"
>

  <q-item v-if="user.canShiftReportRead" clickable v-ripple @click="go('http://unisys-shift-report.mkvityaz.ru')">
    <q-item-section>
      <q-item-label caption>Доклады КДГ</q-item-label>
    </q-item-section>
  </q-item>

  <q-item v-if="user.canAssignmentsReportsRead" clickable v-ripple @click="go('http://unisys-assignments-reports.mkvityaz.ru')">
    <q-item-section>
      <q-item-label caption>Отчёты по командировкам</q-item-label>
    </q-item-section>
  </q-item>

</q-drawer>
</template>