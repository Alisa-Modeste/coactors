import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ActorsComponent } from './actors/actors.component';
import { TitlesComponent } from './titles/titles.component';
import { ActorDetailComponent } from './actor-detail/actor-detail.component';
import { MessagesComponent } from './messages/messages.component';
import { HomeComponent } from './home/home.component';
import { SearchResultComponent } from './search-result/search-result.component';
import { HeaderBufferComponent } from './header-buffer/header-buffer.component';

@NgModule({
  declarations: [
    AppComponent,
    ActorsComponent,
    TitlesComponent,
    ActorDetailComponent,
    MessagesComponent,
    HomeComponent,
    SearchResultComponent,
    HeaderBufferComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
