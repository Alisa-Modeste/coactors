import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { SearchResultComponent } from './search-result.component';

class MockActivatedRoute {}
class MockRouter {
  routeReuseStrategy = {};
}
class MockHttpClient {}

describe('SearchResultComponent', () => {
  let component: SearchResultComponent;
  let fixture: ComponentFixture<SearchResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchResultComponent ],
      providers: [
        SearchResultComponent,
        { provide: ActivatedRoute, useClass: MockActivatedRoute },
        { provide: HttpClient, useClass: MockHttpClient },
        { provide: Router, useClass: MockRouter }
      ]
    })
    .compileComponents();

    component = TestBed.inject(SearchResultComponent);

  });

  // beforeEach(() => {
  //   fixture = TestBed.createComponent(SearchResultComponent);
  //   component = fixture.componentInstance;
  //   fixture.detectChanges();
  // });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
