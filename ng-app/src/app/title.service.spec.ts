import { TestBed } from '@angular/core/testing';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { TitleService } from './title.service';

class MockHttpClient {}

describe('TitleService', () => {
  let service: TitleService;
  let httpClient: HttpClient;

  beforeEach(() => {
    TestBed.configureTestingModule({
      // provide the component-under-test and dependent service
      providers: [
        { provide: HttpClient, useClass: MockHttpClient }
      ]
    });
    service = TestBed.inject(TitleService);
    httpClient = TestBed.inject(HttpClient);
  });


  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
