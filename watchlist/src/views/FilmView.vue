<script setup lang="ts">
import Film from '../components/Film.vue'
import { onMounted, ref } from 'vue'
import type {FilmType} from '../vue.d.ts';
import { useRoute } from 'vue-router';


const film = ref({} as FilmType)

onMounted(async () => {
    const route = useRoute()
   try {
    const res = await fetch(`http://127.0.0.1:8000/api/films/${route.params.id}`)
    const data: FilmType = await res.json()
    film.value = data
   } catch (error) {
    console.log(error)
   }
})
</script>

<template>
        <Film  :title="film.title" :poster="film.poster" />
</template>