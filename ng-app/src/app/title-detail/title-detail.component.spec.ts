import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { TitleDetailComponent } from './title-detail.component';

class MockActivatedRoute {}
class MockRouter {
  routeReuseStrategy = {};
}

class MockHttpClient {}

describe('TitleDetailComponent', () => {
  let component: TitleDetailComponent;
  let fixture: ComponentFixture<TitleDetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      // provide the component-under-test and dependent service
      providers: [
        TitleDetailComponent,
        { provide: ActivatedRoute, useClass: MockActivatedRoute },
        { provide: HttpClient, useClass: MockHttpClient },
        { provide: Router, useClass: MockRouter }
      ]
    });

    component = TestBed.inject(TitleDetailComponent);

  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
