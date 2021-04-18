import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Actor } from './actor';
import { MessageService } from './message.service';
import { baseUrl } from './base-url';

@Injectable({
  providedIn: 'root'
})
export class ActorService {
  private actorsUrl = baseUrl +'/actors';
  private actorUrl = baseUrl + '/actor';
  private newActorUrl = baseUrl + '/create_actor';

  constructor(private http: HttpClient,
    private messageService: MessageService) { }


  getActors(): Observable<Actor[]> {
    return this.http.get<Actor[]>(this.actorsUrl)
  }
  
  getActor(uid: string, known:string, coactorQueryString: string, childrenKnown:string): Observable<Actor > {

    if(known == "false" || childrenKnown == "false"){

      this.newActorNotifyDelay();
      let url = `${this.newActorUrl}?uid=${uid}`;
      return this.http.get<Actor>(url)

    }
    else {

      let url = `${this.actorUrl}/${uid}`;
      if (coactorQueryString){
        url += `?ca=${coactorQueryString}`
      }

      return this.http.get<Actor>(url)
    }
  }

  newActorNotifyDelay(): void {
    
    this.messageService.add("This actor's relationships were not in the database. Please wait monetarily while it gets updated.");
     
  }
}
