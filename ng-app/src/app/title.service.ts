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
  private titlesUrl = baseUrl + '/titles';
  private titleUrl = baseUrl + '/title';
  private newTitleUrl = baseUrl + '/create_title';

  constructor(private http: HttpClient,
    private messageService: MessageService) { }


  getTitles(): Observable<Title[]> {
    return this.http.get<Title[]>(this.titlesUrl)
  }
  
  getTitle(uid: string, known:string, titleType: string, childrenKnown:string): Observable<Title > {

      if(known == "false" || childrenKnown == "false"){

      this.newTitleNotifyDelay();
      let url = `${this.newTitleUrl}?uid=${uid}&title_type=${titleType}`;
      return this.http.get<Title>(url)

    }
    else {
      // warn if there will be a delay
      let url = `${this.titleUrl}/${uid}`;

      return this.http.get<Title>(url)
    }
  }

  notifyDelay(response: Observable<string>): void {
    //
    response
      .subscribe(response => {

        if(response == "0"){
          this.messageService.add("This title's relationships were not in the database. Please wait monetarily while it gets updated.");
        }
  });
}

  newTitleNotifyDelay(): void {
    
    this.messageService.add("This title's relationships were not in the database. Please wait monetarily while it gets updated.");
     
  }
}
