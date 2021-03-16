import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { HttpClient, HttpHeaders } from '@angular/common/http';

class MockHttpClient {}

describe('AppComponent', () => {
  
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
      declarations: [
        AppComponent
      ],
      providers: [
        AppComponent,
        { provide: HttpClient, useClass: MockHttpClient },
        // { provide: HttpClient, useClass: MockHttpClient }
      ]
    }).compileComponents();
  });
  
  it('should create the app', () => {
    let httpClient: HttpClient;
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Have We Worked Together?'`, () => {
    let httpClient: HttpClient;
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('Have We Worked Together?');
  });

  // it('should render title', () => {
  //   const fixture = TestBed.createComponent(AppComponent);
  //   fixture.detectChanges();
  //   const compiled = fixture.nativeElement;
  //   expect(compiled.querySelector('.content span').textContent).toContain('my-app app is running!');
  // });
});
