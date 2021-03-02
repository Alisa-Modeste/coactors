import { TestBed } from '@angular/core/testing';

import { MessageService } from './message.service';

describe('MessageService', () => {
  let service: MessageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MessageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should have an empty message array', () => {
    expect(service.messages).toEqual([]);
  });

  it('should display message', () => {
    service.add("My first message");
    expect(service.messages[0]).toEqual("My first message");
  });
});
