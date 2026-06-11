<script setup lang="ts">
import Film from './Film.vue'
import { reactive, watch } from 'vue'
import type {FilmFetchType} from '../vue.d.ts';
import { RouterLink, useRoute } from 'vue-router';

interface State {
    results: FilmFetchType
    isLoading: boolean
    
}
const state: State = reactive({
    results: {
          results: [],
  current_page: 0,
  pages: 1,
    },
    isLoading: true
})
const route = useRoute()

const fetchFilms = async () => {
    try {
        const res = await fetch(`http://127.0.0.1:8000/api/films${route.query.page ? `?page=${route.query.page}` : "" }`)
        const data: FilmFetchType = await res.json()
        state.results = data

    } catch (error) {
        console.log(error)
    } finally {
        state.isLoading = false
    }
}

watch(() => route.query.page, fetchFilms, { immediate: true })
</script>

<template>
    <div class="films-grid">
        
        <li v-for="film in state.results.results" :key="film.title" class="film-li">
                <RouterLink :to="'/films/' + film.id">
                
                <Film  :title="film.title" :poster="film.poster" :blu_ray="film.blu_ray" :four_kay="film.four_kay"  />
            </RouterLink>
            </li>
        </div>
        
                    <div class="paginate">
        
                        <div><RouterLink :to="'?page=' + `${state.results.current_page - 1}`" v-if="state.results.current_page > 1" >Prev</RouterLink></div>
                        <span>{{state.results.current_page}}/{{ state.results.pages }}</span>
                        <div>
                            <RouterLink v-if="state.results.current_page < state.results.pages"   :to="'?page=' + `${state.results.current_page + 1}`" >Next</RouterLink>
                        </div>
                        
                    </div>
</template>