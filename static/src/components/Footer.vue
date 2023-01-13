<script setup>
import { matWarning } from '@quasar/extras/material-icons'
</script>

<template>
<q-footer class="transparent text-white row items-center q-pa-sm">
  <div class="row items-center q-gutter-sm">
    <q-icon :name="matWarning" size="xs" color="orange" />
    <span class="text-weight-bold text-orange">Модуль работает в режиме тестирования!</span>
  </div>
  <q-space />
  <div class="column items-end">
    <span class="text-weight-bold">&copy;2022 Акционерное общество "Кодун"</span>
    <span class="text-weight-light">Отдел автоматизированных систем управления предприятием</span>
  </div>
</q-footer>
</template>

<style lang="sass" scoped>
@import 'quasar/src/css/variables.sass'
span
  font-size: .7em
</style>