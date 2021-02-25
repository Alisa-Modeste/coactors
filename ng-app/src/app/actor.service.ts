import { Injectable } from '@angular/core';
import { Actor } from './actor';
import { ACTORS } from './mock-data';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ActorService {
  // private actorsUrl = '/actors';
  // private actorUrl = '/actor';
  private actorsUrl = 'http://127.0.0.1:5000/actors';
  private actorUrl = 'http://127.0.0.1:5000/actor';

  constructor(private http: HttpClient
    // ,private messageService: MessageService) { }
    ) { }

  // getActors(): Actor[] {
  //   return ACTORS;
  // }

  getActors(): Observable<Actor[]> {
    // const actors = of(ACTORS);
    // return actors;
    return this.http.get<Actor[]>(this.actorsUrl)
  }

  // getActor(uid: string): Observable<Actor | undefined> {
  getActor(uid: string): Observable<Actor > {
    // TODO: send the message _after_ fetching the actor
    // this.messageService.add(`ActorService: fetched actor id=${id}`);
    // return of(ACTORS.find(actor => actor.uid === uid));
    const url = `${this.actorUrl}/${uid}`;
    return this.http.get<Actor>(url)//.pipe(
    // tap(_ => this.log(`fetched hero uid=${uid}`)),
    // catchError(this.handleError<Actor>(`getActor uid=${uid}`))
  // );
  }
}
