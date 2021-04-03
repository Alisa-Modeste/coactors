import { Injectable } from '@angular/core';
// import { ACTORS } from './mock-data';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Actor } from './actor';
import { MessageService } from './message.service';
import { baseUrl } from './base-url';

@Injectable({
  providedIn: 'root'
})
export class ActorService {
  // private actorsUrl = '/actors';
  // private actorUrl = '/actor';
  private actorsUrl = baseUrl +'/actors';
  private actorUrl = baseUrl + '/actor';
  private actorChildrenUrl = baseUrl + '/actor_children_known';
  private newActorUrl = baseUrl + '/create_actor';

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
  getActor(uid: string, known:string, coactorQueryString: string, childrenKnown:string): Observable<Actor > {
      // TODO: send the message _after_ fetching the actor
      // this.messageService.add(`ActorService: fetched actor id=${id}`);
      // return of(ACTORS.find(actor => actor.uid === uid));
      console.log("uid: "+ uid+"known: "+known+"queryString: "+coactorQueryString)
      console.log("known: "+known+"childrenKnown: "+childrenKnown)
    if(known == "false" || childrenKnown == "false"){
      console.log("if statement")
      this.newActorNotifyDelay();
      let url = `${this.newActorUrl}?uid=${uid}`;
      return this.http.get<Actor>(url)//.pipe(

    }
    else {
      console.log("else statement")
      // warn if there will be a delay
      // let childrenStatus = this.childrenKnown(uid);
      // this.notifyDelay(childrenStatus);

      let url = `${this.actorUrl}/${uid}`;
      if (coactorQueryString){
        url += `?ca=${coactorQueryString}`
      }

      console.log('url'+url)
      return this.http.get<Actor>(url)//.pipe(
      // tap(_ => this.log(`fetched hero uid=${uid}`)),
      // catchError(this.handleError<Actor>(`getActor uid=${uid}`))
    // );
    }
  }

//   childrenKnown(uid: string): Observable<string> {
//     let url = `${this.actorChildrenUrl}/${uid}`;
//     return this.http.get<string>(url)
//   }

//   notifyDelay(response: Observable<string>): void {
//     //
//     response
//       // .subscribe(actor => this.actor = actor);
//       .subscribe(response => {

//           // if(response != "true"){
//           console.log("this.childrenKnow")
//           console.log(response)
//           if(response == "0"){
//           this.messageService.add("This actor's relationships were not in the database. Please wait monetarily while it gets updated. Thank you");
//         }
//   });
// }

  newActorNotifyDelay(): void {
    
    this.messageService.add("This actor's relationships were not in the database. Please wait monetarily while it gets updated. Thank you");
     
  }
}
