import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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
    private location: Location
  ) {}

  ngOnInit(): void {
    this.getActor();
  }

  getActor(): void {
    const uid = ""+this.route.snapshot.paramMap.get('uid');
    console.log("uid:" + uid)
    console.log( this.route)
    this.actorService.getActor(uid)
      // .subscribe(actor => this.actor = actor);
      .subscribe(actor => {
        this.actor = actor
    console.log("actor:" )
    console.log( actor)
  });
  }

}
