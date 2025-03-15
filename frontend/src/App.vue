<template>
  <router-view></router-view>
</template>

<script setup>
</script>

<style>
:root {
  --primary-color: #3b82f6;
  --primary-light: #60a5fa;
  --text-color: #1e293b;
  --background-color: #f8fafc;
  --border-color: #e2e8f0;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
}

* {
  box-sizing: border-box;
}

button {
  font-family: inherit;
}

input, button {
  outline: none;
}

input:focus {
  border-color: var(--primary-color);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style> 