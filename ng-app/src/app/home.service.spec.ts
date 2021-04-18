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

  describe('ActorService', () => {
    let service: ActorService;
    let httpClient: HttpClient;
    

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
    
    

  });
}