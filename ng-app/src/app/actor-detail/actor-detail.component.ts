import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
// import {MatTabsModule} from '@angular/material/tabs';

import { Actor } from '../actor'
import { ActorService } from '../actor.service';
import { MessageService } from '../message.service';

@Component({
  selector: 'app-actor-detail',
  templateUrl: './actor-detail.component.html',
  styleUrls: ['./actor-detail.component.css']
})
export class ActorDetailComponent implements OnInit {
  @Input() actor?: Actor;
  queryString:string = "";
  page:number = 1;
  searchTerm: string = "";

  constructor(
    private route: ActivatedRoute,
    private actorService: ActorService,
    private location: Location,
    private router: Router,
    private messageService: MessageService
  ) {

    // so components can be updated when a different param is used
    this.router.routeReuseStrategy.shouldReuseRoute = function () {
      return false;
    };

  }


  ngOnInit(): void {
    this.getActor();
  }

  ngOnChanges(): void {
    this.getActor();
  }

  getActor(): void {
    const uid = ""+this.route.snapshot.paramMap.get('uid');
    const ca = this.route.snapshot.queryParams['ca']
    const unknown = this.route.snapshot.queryParams['unknown']

    this.actorService.getActor(uid, unknown, ca)
      // .subscribe(actor => this.actor = actor);
      .subscribe(actor => {
        this.actor = actor
        
        if (this.route.snapshot.queryParams['ca']){
          this.queryString = (this.route.snapshot.queryParams['ca']) + ","
        }

        this.messageService.clear();

  });

  // console.log(this.route.snapshot.routeConfig!.path)
  // console.log(this.route.snapshot.params)
  // console.log(this.route.snapshot.queryParams)
  // console.log("k param")
  // console.log(this.route.snapshot.queryParams['k'])
  // console.log(this.route.snapshot.queryParams.k)
  // console.log("s param")
  console.log(this.route.snapshot.queryParams['ca'])
}

}
