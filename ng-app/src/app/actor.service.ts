import { Injectable } from '@angular/core';
// import { ACTORS } from './mock-data';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Actor } from './actor';
import { MessageService } from './message.service';

@Injectable({
  providedIn: 'root'
})
export class ActorService {
  // private actorsUrl = '/actors';
  // private actorUrl = '/actor';
  private actorsUrl = 'http://127.0.0.1:5000/actors';
  private actorUrl = 'http://127.0.0.1:5000/actor';
  private actorExistUrl = 'http://127.0.0.1:5000/actor_exist';

  constructor(private http: HttpClient,
    // ,private messageService: MessageService) { }
    private messageService: MessageService) { }

  // getActors(): Actor[] {
  //   return ACTORS;
  // }

  getActors(): Observable<Actor[]> {
    // const actors = of(ACTORS);
    // return actors;
    return this.http.get<Actor[]>(this.actorsUrl)
  }

  // getActor(uid: string): Observable<Actor | undefined> {
  getActor(uid: string, queryString: string = ""): Observable<Actor > {
    // TODO: send the message _after_ fetching the actor
    // this.messageService.add(`ActorService: fetched actor id=${id}`);
    // return of(ACTORS.find(actor => actor.uid === uid));

    // warn if there will be a delay
    let childrenStatus = this.childrenKnown(uid);
    this.notifyDelay(childrenStatus);

    let url = `${this.actorUrl}/${uid}`;
    if (queryString){
      url += `?ca=${queryString}`
    }

    console.log('url'+url)
    return this.http.get<Actor>(url)//.pipe(
    // tap(_ => this.log(`fetched hero uid=${uid}`)),
    // catchError(this.handleError<Actor>(`getActor uid=${uid}`))
  // );
  }

  childrenKnown(uid: string): Observable<string> {
    let url = `${this.actorExistUrl}/${uid}`;
    return this.http.get<string>(url)
  }

  notifyDelay(response: Observable<string>): void {
    //
    response
      // .subscribe(actor => this.actor = actor);
      .subscribe(response => {

          if(response != "true"){
          this.messageService.add("This actor's relationships were not in the database. Please wait monetarily while it gets updated. Thank you");
        }
  });
  }
}
