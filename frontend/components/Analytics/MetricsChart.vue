<template>
  <div class="chart-wrap">
    <ClientOnly>
      <Line :data="data" :options="options" />
      <template #fallback>
        <div class="chart-skeleton" />
      </template>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

defineProps<{ data: object }>()

const options = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index' as const,
    intersect: false,
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1E1E2C',
      titleColor: '#F0EFF8',
      bodyColor: '#8B8AA8',
      borderColor: 'rgba(255,255,255,0.08)',
      borderWidth: 1,
      padding: 10,
      callbacks: {
        label: (ctx: any) => ` ${ctx.parsed.y} DMs`,
      },
    },
  },
  scales: {
    x: {
      grid: { color: 'rgba(255,255,255,0.04)' },
      ticks: { color: '#8B8AA8', font: { size: 11 } },
      border: { color: 'transparent' },
    },
    y: {
      grid: { color: 'rgba(255,255,255,0.04)' },
      ticks: { color: '#8B8AA8', font: { size: 11 } },
      border: { color: 'transparent' },
      beginAtZero: true,
    },
  },
  elements: {
    point: {
      radius: 4,
      hoverRadius: 6,
      backgroundColor: '#6C63FF',
      borderColor: '#6C63FF',
      borderWidth: 2,
    },
    line: {
      borderWidth: 2,
    },
  },
}
</script>

<style scoped>
.chart-wrap { height: 240px; }
.chart-skeleton {
  height: 240px;
  border-radius: 8px;
  background: var(--color-surface-2, #1a1a2e);
  animation: pulse 1.4s ease infinite;
}
@keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 0.8; } }
</style>
