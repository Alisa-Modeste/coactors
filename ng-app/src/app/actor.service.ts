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

  getActor(uid: string): Observable<Actor | undefined> {
  // getActor(uid: string): Observable<Actor > {
    // TODO: send the message _after_ fetching the actor
    // this.messageService.add(`ActorService: fetched actor id=${id}`);
    return of(ACTORS.find(actor => actor.uid === uid));
  }
}
