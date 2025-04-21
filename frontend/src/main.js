import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import useUserStore from './stores/userStore'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/main.css'

const app = createApp(App)

// 创建userStore实例
const userStore = useUserStore()

// 注入 userStore
app.provide('userStore', userStore)

app.use(router)
app.use(ElementPlus)
app.mount('#app') 