import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3005,
    proxy: {
      '/api': {
        target: 'http://localhost:5008',
        changeOrigin: true,
        secure: false,
        ws: true,
        rewrite: (path) => path
      },
      '/uploads': {
        target: 'http://localhost:5008',
        changeOrigin: true,
        secure: false,
        ws: true
      },
      '/default-avatar.png': {
        target: 'http://localhost:5008',
        changeOrigin: true,
        secure: false
      }
    },
    hmr: {
      overlay: false
    }
  },
  optimizeDeps: {
    force: true
  },
  clearScreen: false
}) 