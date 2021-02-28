import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActorDetailComponent } from './actor-detail.component';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';


class MockActorService {
  isLoggedIn = true;
  user = { name: 'Test User'};
}

class MockActivatedRoute {}
class MockRouter {
  // "routeReuseStrategy": {};
  routeReuseStrategy = {};
}

class MockHttpClient {
  isLoggedIn = true;
  user = { name: 'Test User'};
}

describe('ActorDetailComponent', () => {
  let component: ActorDetailComponent;
  let activatedRoute: ActivatedRoute;
  let httpClient: HttpClient;
  let router: Router;
  
  beforeEach(() => {
    TestBed.configureTestingModule({
      // provide the component-under-test and dependent service
      providers: [
        ActorDetailComponent,
        { provide: ActivatedRoute, useClass: MockActivatedRoute },
        { provide: HttpClient, useClass: MockHttpClient },
        { provide: Router, useClass: MockRouter }
      ]
    });

    // inject both the component and the dependent service.
    console.log("in before each")
    component = TestBed.inject(ActorDetailComponent);
    console.log(component)
    activatedRoute = TestBed.inject(ActivatedRoute);
    httpClient = TestBed.inject(HttpClient);
    router = TestBed.inject(Router);
  });

  it('should create', () => {
    console.log("act det comp")
    console.log(ActorDetailComponent)
    console.log(component)
    expect(component).toBeTruthy();
  });
});
