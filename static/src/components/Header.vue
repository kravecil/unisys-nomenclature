<script setup>
import { ref, onMounted } from 'vue'
import { user } from '@/api/auth'
import hosts from '@/api/hosts'
import { refreshStats } from '@/api/core'
import { stats } from '@/api/store'
import { matAccountCircle } from '@quasar/extras/material-icons'

onMounted(() => refreshStats())

const goHome = () => {
  window.location = hosts.home
}
</script>

<template>
<q-header class="header" elevated>
  <q-toolbar class="q-px-lg">
    <q-toolbar-title class="column">
      <router-link :to="{name:'index'}" class="text-caption text-weight-bold link self-start">
        Номенклатурно-справочная информация
      </router-link>
    </q-toolbar-title>

    <div class="text-caption q-gutter-x-md row items-center">
      <!-- <a :href="hosts.home" class="text-primary link text-weight-bold">ЕИС</a>

      <q-separator vertical inset color="grey-7" /> -->

      <router-link class="link" :to="{name:'enses'}">ЕНС</router-link>

      <q-separator vertical inset color="grey-7" />

      <div class="q-gutter-sm">
        <router-link class="link" :to="{name:'nomenclature'}">Номенклатурные номера</router-link>
        <q-badge class="text-weight-light text-dense bg-grey-9">{{ stats.products }}</q-badge>
      </div>

      <q-separator vertical inset color="grey-7" />

      <div class="q-gutter-sm">
        <router-link class="link" :to="{name:'requests'}">Заявки</router-link>
        <q-badge class="text-weight-light text-dense bg-grey-9">{{ stats.requests }}</q-badge>
      </div>
      <q-btn no-caps label="Новая заявка" color="primary" :to="{name:'newRequest'}" />

      <q-separator vertical inset color="grey-7" />

      <q-icon :name="matAccountCircle" size="sm" class="cursor-pointer">
        <q-menu>
          <q-list dense class="text-caption">
            <q-item class="text-deep-orange">
              <q-item-section>{{ user.fullname }}</q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable @click="goHome()">
              <q-item-section>Домашная страница ЕИС</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-icon>
    </div>

    <!-- <Search /> -->

  </q-toolbar>
  <q-separator color="grey-9" />
</q-header>
</template>
<style scoped lang="sass">
// @import 'quasar/src/css/variables.sass'
.header
  background: #fff2
.link
  text-decoration: none
  color: white
  transition-duration: 200ms
  &:hover
    color: $primary
</style>