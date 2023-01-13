import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar/* , transformAssetUrls */ } from '@quasar/vite-plugin'

import { resolve } from 'path'
// import { env } from 'process'

export default defineConfig({
  plugins: [
        vue({
            template: {
                transformAssetUrls: {
                    base: '/static/',
                },
            }
        }),
        quasar({
            sassVariables: resolve('./static/src/assets/css/quasar-variables.sass')
        })
    ],
  root: resolve('./static/src'),
  base: '/static/',
  server: {
    host: 'unisys-nomenclature.mkvityaz.ru',
    port: 3000,
    open: false,
    watch: {
        usePolling: true,
    },
  },
  build: {
    manifest: true,
    outDir: resolve('./static/dist'),
    emptyOutDir: true,
    rollupOptions: {
        input: {
            main: resolve('./static/src/main.js')
        },
    }
  },
  resolve: {
    alias: {
        '@': resolve(__dirname, './static/src')
    }
  }
})