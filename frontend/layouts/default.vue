<template>
  <div class="app-shell">
    <AppSidebar />
    <div class="main-area">
      <AppTopBar />
      <main class="page-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background: var(--color-bg);
}
.main-area {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}
.page-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}
</style>
