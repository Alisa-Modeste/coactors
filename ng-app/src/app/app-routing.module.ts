import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ActorDetailComponent } from './actor-detail/actor-detail.component';
import { ActorsComponent } from './actors/actors.component';
import { HomeComponent } from './home/home.component';
import { SearchResultComponent } from './search-result/search-result.component';

const routes: Routes = [
  { path: 'actors', component: ActorsComponent },
  // { path: '/', component: HomeComponent },
  { path: '', component: HomeComponent },
  // { path: '', redirectTo: '/', pathMatch: 'full' }
  { path: 'actor/:uid', component: ActorDetailComponent },
  { path: 'search', component: SearchResultComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

