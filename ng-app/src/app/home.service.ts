import { Injectable } from '@angular/core';
// import { ACTORS } from './mock-data';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Actor } from './actor';
import { Title } from './title';
import { HomeMulti } from './home-multi';
import { baseUrl } from './base-url';

@Injectable({
  providedIn: 'root'
})
export class HomeService {
  private valuesUrl = baseUrl +'/multi';


  constructor(private http: HttpClient) { }

  // getActors(): Actor[] {
  //   return ACTORS;
  // }

  getValues() {
    
    return this.http.get<HomeMulti>(this.valuesUrl)
  }


}
