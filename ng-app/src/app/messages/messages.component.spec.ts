import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MessagesComponent } from './messages.component';
import { MessageService } from '../message.service';

class MockMessageService { }

describe('MessagesComponent', () => {
  let component: MessagesComponent;
  let fixture: ComponentFixture<MessagesComponent>;
  let messageService: MessageService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MessagesComponent ],
      providers: [
        MessagesComponent,
        { provide: MessageService, useClass: MockMessageService },
        // { provide: HttpClient, useClass: MockHttpClient }
      ]
    })
    .compileComponents();
  });

  
  
  beforeEach(() => {
    fixture = TestBed.createComponent(MessagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    // messageService = TestBed.inject(MessageService);
  });
  
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  
  it('should display messages', () => {
    let messageService = new MessageService();
    messageService.add("Hello there");
    // component = new MessagesComponent();
    // displayableMessages = messageService.messages
    expect(messageService.messages).toContain("Hello there");

  });

});
