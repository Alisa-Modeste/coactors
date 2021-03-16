import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { TitlesComponent } from './titles.component'; 

class MockHttpClient {}

describe('TitlesComponent', () => {
  let component: TitlesComponent;
  let fixture: ComponentFixture<TitlesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      // provide the component-under-test and dependent service
      providers: [
        TitlesComponent,
        { provide: HttpClient, useClass: MockHttpClient },
      ]
    });

    component = TestBed.inject(TitlesComponent);

  });

  // beforeEach(() => {
  //   fixture = TestBed.createComponent(TitlesComponent);
  //   component = fixture.componentInstance;
  //   fixture.detectChanges();
  // });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
