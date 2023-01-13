<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { useRoute } from 'vue-router';

const route = useRoute()
const isHomepage = () => {
    if (route.path == "/" || route.path == "/shifts") {
        return true
    } else {
        return false
    }
}
</script>

<template>
    <q-layout view="hHh LpR fFf">
        <div class="video-container">
            <video autoplay muted loop>
            <source src="/static/bg_vid.mp4" />
            </video>
        </div>
        <Header />
        <q-page-container>
            <router-view v-slot="{ Component }" class="page-container">
                <transition enter-active-class="animate__animated animate__fadeIn">
                    <component :is="Component" />
                </transition>
            </router-view>
        </q-page-container>
        <Footer />
        
    </q-layout>
</template>

<style lang="sass" scoped>
.page-container
//   width: 100%
//   max-width: 1170px
//   margin: 0 auto
.video-container
     z-index: -1
     position: fixed
     top: 0
     width: 100%
     height: 100%
     & video
       width: 100%
       height: 100%
       filter: grayscale(80%)
       object-fit: cover
</style>
