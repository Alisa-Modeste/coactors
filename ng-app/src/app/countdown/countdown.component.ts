import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription, interval } from "rxjs";

@Component({
  selector: 'app-countdown',
  templateUrl: './countdown.component.html',
  styleUrls: ['./countdown.component.css']
})
export class CountdownComponent implements OnInit, OnDestroy {
    private subscription!: Subscription;
    private dateNow = new Date().getTime();
    private counterStart:number = 90;
    public secondsLeft:number = this.counterStart;

    constructor() { }

    ngOnInit() {
        this.subscription = interval(1000)
            .subscribe(x => { this.counter(); });
     }
 
    ngOnDestroy() {
       this.subscription.unsubscribe();
    }

    private counter() {
        let secondsPassed:number = Math.floor((new Date().getTime() - this.dateNow)/1000);
        this.secondsLeft =  this.counterStart - secondsPassed;
    }

}
