import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';

import { Actor } from '../actor'
import { ActorService } from '../actor.service';

@Component({
  selector: 'app-actor-detail',
  templateUrl: './actor-detail.component.html',
  styleUrls: ['./actor-detail.component.css']
})
export class ActorDetailComponent implements OnInit {
  @Input() actor?: Actor;

  constructor(
    private route: ActivatedRoute,
    private actorService: ActorService,
    private location: Location,
    private router: Router
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
    console.log("uid:" + uid)
    console.log( this.route)
    this.actorService.getActor(uid, ca)
      // .subscribe(actor => this.actor = actor);
      .subscribe(actor => {
        this.actor = actor
    console.log("actor:" )
    console.log( actor)
  });

  console.log(this.route.snapshot.routeConfig!.path)
  console.log(this.route.snapshot.params)
  console.log(this.route.snapshot.queryParams)
  console.log("k param")
  console.log(this.route.snapshot.queryParams['k'])
  console.log(this.route.snapshot.queryParams.k)
  console.log("s param")
  console.log(this.route.snapshot.queryParams['ca'])
}

}
