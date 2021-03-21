import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Actor } from './actor';
import { SearchResult } from './search-result';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private actorsUrl = 'http://127.0.0.1:5000/actor_search';
  private titlesUrl = 'http://127.0.0.1:5000/title_search';

  constructor(private http: HttpClient) { }

  getActors(query: string, more:string = "") {
    let url = this.actorsUrl + `?query=${query}&type=actor&more=${more}`
    // return this.http.get<Actor[]>(url)
    return this.http.get<SearchResult>(url)
  }

  getTitles(query: string, more:string = "") {
    let url = this.titlesUrl + `?query=${query}&type=title&more=${more}`
    
    return this.http.get<SearchResult>(url)
    
  }

  }
