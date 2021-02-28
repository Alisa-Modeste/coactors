import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActorsComponent } from './actors.component';
// import { ActorService } from '../actor.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

// describe('ActorsComponent', () => {
//   let component: ActorsComponent;
//   let fixture: ComponentFixture<ActorsComponent>;

//   beforeEach(async () => {
//     await TestBed.configureTestingModule({
//       declarations: [ ActorsComponent ]
//     })
//     .compileComponents();
//   });

//   beforeEach(() => {
//     fixture = TestBed.createComponent(ActorsComponent);
//     component = fixture.componentInstance;
//     fixture.detectChanges();
//   });

//   // it('should create', () => {
//   //   expect(component).toBeTruthy();
//   // });
// });

class MockActorService {
  isLoggedIn = true;
  user = { name: 'Test User'};
}

class MockHttpClient {
  isLoggedIn = true;
  user = { name: 'Test User'};
}

describe("ActorsComponent", () => {
  let component: ActorsComponent;
  // let actorService: ActorService;
  let httpClient: HttpClient;

  beforeEach(() => {
    TestBed.configureTestingModule({
      // provide the component-under-test and dependent service
      providers: [
        ActorsComponent,
        // { provide: ActorService, useClass: MockActorService },
        { provide: HttpClient, useClass: MockHttpClient }
      ]
    });

    // inject both the component and the dependent service.
    component = TestBed.inject(ActorsComponent);
    // actorService = TestBed.inject(ActorService);
    httpClient = TestBed.inject(HttpClient);
  });

it('should create', () => {
  expect(component).toBeTruthy();
});

it('should not have any actors after construction', () => {
  expect(component.actors).toBeUndefined();
});

});