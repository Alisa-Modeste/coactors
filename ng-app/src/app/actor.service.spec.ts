import { TestBed } from '@angular/core/testing';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { Actor } from './actor';
import { ActorService } from './actor.service';
import { MessageService } from './message.service';
import { ACTORS } from './mock-data';


class MockHttpClient {}

class MockActorService extends ActorService {
  getActors(): Observable<Actor[]> {
    const actors = of(ACTORS);
    return actors;

  }

  getActor(uid: string, queryString: string = ""): Observable<Actor> {

      return of(ACTORS[1]);

  }

  childrenKnown(uid: string): Observable<string> {
    if (uid == "1"){
      return of("true");

    }
    else {
      return of("false");

    }
  }
}

describe('ActorService', () => {
  let service: ActorService;
  let httpClient: HttpClient;
  let messageService: MessageService;


  beforeEach(() => {
    TestBed.configureTestingModule({
      // provide the component-under-test and dependent service
      providers: [
        // ActorsComponent,
        { provide: ActorService, useClass: MockActorService },
        { provide: HttpClient, useClass: MockHttpClient }
      ]
    });
    service = TestBed.inject(ActorService);
  });
  
  it('should be created', () => {
    expect(service).toBeTruthy();
    
  });
  
  it('should be an identity', () => {
    expect(service).toEqual(service);
    
  });
  
  it('should contain sent message', () => {
    messageService = TestBed.inject(MessageService);
    service.notifyDelay( service.childrenKnown("0") );
    console.log(messageService.messages[0] );
    expect(messageService.messages[0]).toContain("not in the database");
  });

  it('should not contain any messages', () => {
    messageService = TestBed.inject(MessageService);
    service.notifyDelay( service.childrenKnown("1") );

    expect(messageService.messages).toEqual([]);
  });

});
