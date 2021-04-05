import { Component, OnInit, Input, OnChanges } from '@angular/core';
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
export class ActorDetailComponent implements OnInit, OnChanges {
  @Input() actor?: Actor;
  queryString:string = "";
  page:number = 1;
  numPerPage:number = 25;
  searchTerm: string = "";
  groupButton: string = "";

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
    const coactors = this.route.snapshot.queryParams['ca']
    // const unknown = this.route.snapshot.queryParams['unknown']
    const known = this.route.snapshot.queryParams['k']
    const childrenKnown = this.route.snapshot.queryParams['ck']

    this.actorService.getActor(uid, known, coactors, childrenKnown)
      // .subscribe(actor => this.actor = actor);
      .subscribe(actor => {
        this.actor = actor
        console.log(actor)
        if (this.route.snapshot.queryParams['ca']){
          this.queryString = (this.route.snapshot.queryParams['ca']) + ","
        }

        this.messageService.clear();

        this.groupButton = actor.group_members.length > 0 ? "Make a Group With" : "Add to Group";

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
