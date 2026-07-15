<template>
  <span class="pill" :class="pillClass">{{ label }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  tone: { type: String, default: 'neutral' } // success | warning | danger | neutral
})

const pillClass = computed(() => `pill-${props.tone}`)
</script>
