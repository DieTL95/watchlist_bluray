declare module "*.vue" {
  import { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

export interface FilmType {
  id: number;
  title: string;
  poster: string | undefined;
  relative_url: string;
  blu_ray: boolean | undefined;
  four_kay: boolean | undefined;
}

export interface FilmFetchType {
  results: FilmType[];
  current_page: number;
  pages: number;
}
