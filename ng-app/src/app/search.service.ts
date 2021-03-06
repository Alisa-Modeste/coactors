import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Actor } from './actor';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private actorsUrl = 'http://127.0.0.1:5000/actor_search';
  private titlesUrl = 'http://127.0.0.1:5000/title_search';

  constructor(private http: HttpClient) { }

  getActors(query: string) {
    let url = this.actorsUrl + `?query=${query}&type=actor`
    return this.http.get<Actor[]>(url)
  }

  getTitles() {
    // return this.http.get<Title[]>(this.titlesUrl)
    
  }
}
