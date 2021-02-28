import { TestBed } from '@angular/core/testing';

import { ActorService } from './actor.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

class MockHttpClient {
  isLoggedIn = true;
  user = { name: 'Test User'};
}

describe('ActorService', () => {
  let service: ActorService;
  let httpClient: HttpClient;


  beforeEach(() => {
    TestBed.configureTestingModule({
      // provide the component-under-test and dependent service
      providers: [
        // ActorsComponent,
        // { provide: ActorService, useClass: MockActorService },
        { provide: HttpClient, useClass: MockHttpClient }
      ]
    });
    service = TestBed.inject(ActorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
