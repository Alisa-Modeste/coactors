import { Injectable } from '@angular/core';
import { Actor } from './actor';
import { ACTORS } from './mock-data';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ActorService {

  constructor() { }

  // getActors(): Actor[] {
  //   return ACTORS;
  // }

  getActors(): Observable<Actor[]> {
    const actors = of(ACTORS);
    return actors;
  }
}
