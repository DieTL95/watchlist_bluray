<script setup lang="ts">

defineProps<{
    title: string
    poster?: string
    blu_ray?: boolean
    four_kay?: boolean
}>()
</script>
<template>
    <div class="film-item">
        <img :src="poster ? poster : 'https://s.ltrbxd.com/static/img/empty-poster-125-AiuBHVCI.png'" :alt="title" :width=250 class="film-poster">
        <div class="formats">
            <span class="format-span" v-if="blu_ray === true">Blu-Ray</span>
            <span class="format-span" v-if="four_kay === true">4K</span>
        </div>
        <span class="film-span">{{ title }}</span>
     

    </div>
</template>