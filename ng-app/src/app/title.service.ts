import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Title } from './title';
import { MessageService } from './message.service';
import { baseUrl } from './base-url';

@Injectable({
  providedIn: 'root'
})
export class TitleService {
  // private actorsUrl = '/actors';
  // private actorUrl = '/actor';
  private titlesUrl = baseUrl + '/titles';
  private titleUrl = baseUrl + '/title';
  private titleChildrenUrl = baseUrl + '/title_children_known';
  private newTitleUrl = baseUrl + '/create_title';

  constructor(private http: HttpClient,
    // ,private messageService: MessageService) { }
    private messageService: MessageService) { }

  // getActors(): Actor[] {
  //   return ACTORS;
  // }

  getTitles(): Observable<Title[]> {
    // const actors = of(ACTORS);
    // return actors;
    
    return this.http.get<Title[]>(this.titlesUrl)
  }
  
  // getActor(uid: string): Observable<Actor | undefined> {
  getTitle(uid: string, known:string, titleType: string, childrenKnown:string): Observable<Title > {
      // TODO: send the message _after_ fetching the actor
      // this.messageService.add(`ActorService: fetched actor id=${id}`);
      // return of(ACTORS.find(actor => actor.uid === uid));
      console.log("uid: "+ uid+"known: "+known+"titleType: "+titleType+"childrenKnown: "+childrenKnown)
      if(known == "false" || childrenKnown == "false"){
      console.log("if statement")
      this.newTitleNotifyDelay();
      let url = `${this.newTitleUrl}?uid=${uid}&title_type=${titleType}`;
      return this.http.get<Title>(url)//.pipe(

    }
    else {
      console.log("else statement")
      // warn if there will be a delay
      let childrenStatus = this.childrenKnown(uid);
      this.notifyDelay(childrenStatus);

      let url = `${this.titleUrl}/${uid}`;

      console.log('url'+url)
      return this.http.get<Title>(url)//.pipe(
      // tap(_ => this.log(`fetched hero uid=${uid}`)),
      // catchError(this.handleError<Actor>(`getActor uid=${uid}`))
    // );
    }
  }

  childrenKnown(uid: string): Observable<string> {
    let url = `${this.titleChildrenUrl}/${uid}`;
    return this.http.get<string>(url)
  }

  notifyDelay(response: Observable<string>): void {
    //
    response
      .subscribe(response => {

        if(response == "0"){
          this.messageService.add("This title's relationships were not in the database. Please wait monetarily while it gets updated. Thank you");
        }
  });
}

  newTitleNotifyDelay(): void {
    
    this.messageService.add("This title's relationships were not in the database. Please wait monetarily while it gets updated. Thank you");
     
  }
}
