import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AboutComponent } from './about/about.component';
import { ActorDetailComponent } from './actor-detail/actor-detail.component';
import { ActorsComponent } from './actors/actors.component';
import { HomeComponent } from './home/home.component';
import { SearchResultComponent } from './search-result/search-result.component';
import { TitleDetailComponent } from './title-detail/title-detail.component';
import { TitlesComponent } from './titles/titles.component';

const routes: Routes = [
  { path: 'actors', component: ActorsComponent },
  { path: '', component: HomeComponent },
  { path: 'actor/:uid', component: ActorDetailComponent },
  { path: 'search', component: SearchResultComponent },
  { path: 'titles', component: TitlesComponent },
  { path: 'title/:uid', component: TitleDetailComponent },
  { path: 'about', component: AboutComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

